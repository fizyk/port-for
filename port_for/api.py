"""main port-for functionality."""

import random
import socket
from itertools import chain
from typing import Iterable, Optional, Type, TypeVar, Union

from port_for import ephemeral, utils

from ._ranges import UNASSIGNED_RANGES
from .exceptions import PortForException

SYSTEM_PORT_RANGE = (0, 1024)


def select_random(
    ports: Optional[set[int]] = None,
    exclude_ports: Optional[Iterable[int]] = None,
) -> int:
    """Return random unused port number."""
    if ports is None:
        ports = available_good_ports()

    if exclude_ports is None:
        exclude_ports = set()

    ports.difference_update(set(exclude_ports))

    for port in random.sample(tuple(ports), min(len(ports), 100)):
        if not port_is_used(port):
            return port
    raise PortForException("Can't select a port")


def is_available(port: int) -> bool:
    """Return if port is good to choose."""
    return port in available_ports() and not port_is_used(port)


def available_ports(
    low: int = 1024,
    high: int = 65535,
    exclude_ranges: Optional[list[tuple[int, int]]] = None,
) -> set[int]:
    """Return a set of possible ports.

    .. note::

        Excluding system, ephemeral and well-known ports.

    Pass ``high`` and/or ``low`` to limit the port range.
    """
    if exclude_ranges is None:
        exclude_ranges = []
    available = utils.ranges_to_set(UNASSIGNED_RANGES)
    exclude = utils.ranges_to_set(
        # Motivation behind excluding ephemeral port ranges:
        # let's say you decided to use an ephemeral local port
        # as a persistent port, and "reserve" it to your software.
        # OS won't know about it, and still can try to use this port.
        # This is not a problem if your service is always running and occupying
        # this port (OS would pick next one). But if the service is temporarily
        # not using the port (because of restart of other reason),
        # OS might reuse the same port,
        # which might prevent the service from starting.
        ephemeral.port_ranges()
        + exclude_ranges
        + [SYSTEM_PORT_RANGE, (SYSTEM_PORT_RANGE[1], low), (high, 65536)]
    )
    return available.difference(exclude)


def good_port_ranges(
    ports: Optional[set[int]] = None, min_range_len: int = 20, border: int = 3
) -> list[tuple[int, int]]:
    """Return a list of 'good' port ranges.

    Such ranges are large and don't contain ephemeral or well-known ports.
    Ranges borders are also excluded.
    """
    min_range_len += border * 2
    if ports is None:
        ports = available_ports()
    ranges = utils.to_ranges(list(ports))
    lenghts = sorted([(r[1] - r[0], r) for r in ranges], reverse=True)
    long_ranges = [
        length[1] for length in lenghts if length[0] >= min_range_len
    ]
    without_borders = [
        (low + border, high - border) for low, high in long_ranges
    ]
    return without_borders


def available_good_ports(min_range_len: int = 20, border: int = 3) -> set[int]:
    """List available good ports."""
    return utils.ranges_to_set(
        good_port_ranges(min_range_len=min_range_len, border=border)
    )


def port_is_used(port: int, host: str = "127.0.0.1") -> bool:
    """Return if port is used.

    If we can connect to the port or we cannot bind to it, it's used.
    """
    # Used if something is listening on the port, and we can connect to it
    if _accepts_connection(port, host):
        return True
    # Used if we cannot bind to the port.
    if not _can_bind(port, host):
        return True
    return False


def _can_bind(port: int, host: str) -> bool:
    """Try binding on common addresses to detect if the port is free.

    Some platforms (notably Windows) allow binding to 127.0.0.1 even when the
    port is already bound on INADDR_ANY (0.0.0.0). To reliably detect usage, we
    attempt to bind on both the requested host and INADDR_ANY. If either bind
    fails, consider the port as used.
    """
    hosts_to_try = []
    # Always try the requested host first
    hosts_to_try.append(host)
    # Also try INADDR_ANY for IPv4 to catch cases where 0.0.0.0 is occupied
    if host not in ("", "0.0.0.0"):
        hosts_to_try.append("")
        hosts_to_try.append("0.0.0.0")

    for h in hosts_to_try:
        with socket.socket() as sock:
            try:
                sock.bind((h, port))
            except socket.error:
                return False
    return True


def _accepts_connection(port: int, host: str) -> bool:
    """Return True if connect_ex succeeds (service is listening).

    Works reliably across platforms, including Windows.
    """
    with socket.socket() as sock:
        sock.settimeout(1)
        sock.setblocking(True)
        err = sock.connect_ex((host, port))
        # Relying on ECONNREFUSED does not produce reliable results on windows,
        # which could result in
        # either ECONREFUSED (Mapped in windows to `WSAECONNREFUSED`),
        # timeout or return any other error.
        return err == 0


T = TypeVar("T")


def filter_by_type(lst: Iterable, type_of: Type[T]) -> list[T]:
    """Return a list of elements with given type."""
    return [e for e in lst if isinstance(e, type_of)]


PortType = Union[
    str,
    int,
    tuple[int, int],
    set[int],
    list[str],
    list[int],
    list[tuple[int, int]],
    list[set[int]],
    list[Union[set[int], tuple[int, int]]],
    list[Union[str, int, tuple[int, int], set[int]]],
]


def get_port(
    ports: Optional[PortType],
    exclude_ports: Optional[Iterable[int]] = None,
) -> Optional[int]:
    """Retun a random available port.

    If there's only one port passed (e.g. 5000 or '5000') function
    does not check if port is available.
    If there's -1 passed as an argument, function returns None.

    :param ports:
        exact port (e.g. '8000', 8000)
        randomly selected port (None) - any random available port
        [(2000,3000)] or (2000,3000) - random available port from a given range
        [{4002,4003}] or {4002,4003} - random of 4002 or 4003 ports
        [(2000,3000), {4002,4003}] -random of given range and set
    :param exclude_ports: A set of known ports that can not be selected.
    :returns: a random free port
    :raises: ValueError
    """
    if ports == -1:
        return None
    elif not ports:
        return select_random(None, exclude_ports)

    try:
        return int(ports)  # type: ignore[arg-type]
    except TypeError:
        pass

    ports_set: set[int] = set()

    try:
        if not isinstance(ports, list):
            ports = [ports]
        ranges: set[int] = utils.ranges_to_set(filter_by_type(ports, tuple))
        nums: set[int] = set(filter_by_type(ports, int))
        sets: set[int] = set(
            chain(
                *filter_by_type(
                    ports,
                    (set, frozenset),  # type: ignore[arg-type]
                )
            )
        )
        ports_set = ports_set.union(ranges, sets, nums)
    except ValueError:
        raise PortForException(
            "Unknown format of ports: %s.\n"
            'You should provide a ports range "[(4000,5000)]"'
            'or "(4000,5000)" or a comma-separated ports set'
            '"[{4000,5000,6000}]" or list of ints "[400,5000,6000,8000]"'
            'or all of them "[(20000, 30000), {48889, 50121}, 4000, 4004]"'
            % (ports,)
        )

    return select_random(ports_set, exclude_ports)
