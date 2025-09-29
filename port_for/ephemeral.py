# -*- coding: utf-8 -*-
"""Module provide utilities to find ephemeral port ranges for the current OS.

See http://www.ncftp.com/ncftpd/doc/misc/ephemeral_ports.html for more info
about ephemeral port ranges.

Currently only Linux and BSD (including OS X) are supported.
"""

import subprocess

DEFAULT_EPHEMERAL_PORT_RANGE = (32768, 65535)


def port_ranges() -> list[tuple[int, int]]:
    """Return a list of ephemeral port ranges for current machine."""
    try:
        return _linux_ranges()
    except (OSError, IOError):  # not linux, try BSD
        try:
            ranges = _bsd_ranges()
            if ranges:
                return ranges
        except (OSError, IOError):
            pass

    # fallback
    return [DEFAULT_EPHEMERAL_PORT_RANGE]


def _linux_ranges() -> list[tuple[int, int]]:
    with open("/proc/sys/net/ipv4/ip_local_port_range") as f:
        # use readline() instead of read() for linux + musl
        low, high = f.readline().split()
        return [(int(low), int(high))]


def _bsd_ranges() -> list[tuple[int, int]]:
    pp = subprocess.Popen(["sysctl", "net.inet.ip.portrange"], stdout=subprocess.PIPE)
    stdout, stderr = pp.communicate()
    lines = stdout.decode("ascii").split("\n")
    out: dict[str, str] = dict(
        [[x.strip().rsplit(".")[-1] for x in line.split(":")] for line in lines if line]
    )

    ranges = [
        # FreeBSD & Mac
        ("first", "last"),
        ("lowfirst", "lowlast"),
        ("hifirst", "hilast"),
        # OpenBSD
        ("portfirst", "portlast"),
        ("porthifirst", "porthilast"),
    ]

    res = []
    for rng in ranges:
        try:
            low, high = int(out[rng[0]]), int(out[rng[1]])
            if low <= high:
                res.append((low, high))
        except KeyError:
            pass
    return res
