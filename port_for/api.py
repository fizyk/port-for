# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, with_statement
import contextlib
import socket
import errno
import random
from itertools import chain
from port_for import ephemeral, utils
from ._ranges import UNASSIGNED_RANGES
from .exceptions import PortForException

SYSTEM_PORT_RANGE = (0, 1024)

def select_random(ports=None, exclude_ports=None):
    """
    Returns random unused port number.
    """
    if ports is None:
        ports = available_good_ports()

    if exclude_ports is None:
        exclude_ports = set()

    ports.difference_update(set(exclude_ports))

    for port in random.sample(ports, min(len(ports), 100)):
        if not port_is_used(port):
            return port
    raise PortForException("Can't select a port")

def is_available(port):
    """
    Returns if port is good to choose.
    """
    return port in available_ports() and not port_is_used(port)

def available_ports(low=1024, high=65535, exclude_ranges=None):
    """
    Returns a set of possible ports (excluding system,
    ephemeral and well-known ports).
    Pass ``high`` and/or ``low`` to limit the port range.
    """
    if exclude_ranges is None:
        exclude_ranges = []
    available = utils.ranges_to_set(UNASSIGNED_RANGES)
    exclude = utils.ranges_to_set(
        ephemeral.port_ranges() + exclude_ranges +
        [
            SYSTEM_PORT_RANGE,
            (SYSTEM_PORT_RANGE[1], low),
            (high, 65536)
        ]
    )
    return available.difference(exclude)

def good_port_ranges(ports=None, min_range_len=20, border=3):
    """
    Returns a list of 'good' port ranges.
    Such ranges are large and don't contain ephemeral or well-known ports.
    Ranges borders are also excluded.
    """
    min_range_len += border*2
    if ports is None:
        ports = available_ports()
    ranges = utils.to_ranges(list(ports))
    lenghts = sorted([(r[1]-r[0], r) for r in ranges], reverse=True)
    long_ranges = [l[1] for l in lenghts if l[0] >= min_range_len]
    without_borders = [(low+border, high-border) for low, high in long_ranges]
    return without_borders

def available_good_ports(min_range_len=20, border=3):
    return utils.ranges_to_set(
        good_port_ranges(min_range_len=min_range_len, border=border)
    )


def port_is_used(port, host='127.0.0.1'):
    """
    Returns if port is used. Port is considered used if the current process
    can't bind to it or the port doesn't refuse connections.
    """
    unused = _can_bind(port, host) and _refuses_connection(port, host)
    return not unused


def _can_bind(port, host):
    sock = socket.socket()
    with contextlib.closing(sock):
        try:
            sock.bind((host, port))
        except socket.error:
            return False
    return True

def _refuses_connection(port, host):
    sock = socket.socket()
    with contextlib.closing(sock):
        sock.settimeout(1)
        err = sock.connect_ex((host, port))
        return err == errno.ECONNREFUSED


def filter_by_type(lst, type_of):
    """Returns a list of elements with given type."""
    return [e for e in lst if isinstance(e, type_of)]


def get_port(ports):
    """
    Retuns a random available port. If there's only one port passed
    (e.g. 5000 or '5000') function does not check if port is available.
    If there's -1 passed as an argument, function returns None.

    :param str|int|tuple|set|list ports:
        exact port (e.g. '8000', 8000)
        randomly selected port (None) - any random available port
        [(2000,3000)] or (2000,3000) - random available port from a given range
        [{4002,4003}] or {4002,4003} - random of 4002 or 4003 ports
        [(2000,3000), {4002,4003}] -random of given orange and set
    :returns: a random free port
    :raises: ValueError
    """
    if ports == -1:
        return None
    elif not ports:
        return select_random(None)

    try:
        return int(ports)
    except TypeError:
        pass

    ports_set = set()

    try:
        if not isinstance(ports, list):
            ports = [ports]
        ranges = utils.ranges_to_set(filter_by_type(ports, tuple))
        nums = set(filter_by_type(ports, int))
        sets = set(chain(*filter_by_type(ports, (set, frozenset))))
        ports_set = ports_set.union(ranges, sets, nums)
    except ValueError:
        raise PortForException(
            'Unknown format of ports: %s.\n'
            'You should provide a ports range "[(4000,5000)]"'
            'or "(4000,5000)" or a comma-separated ports set'
            '"[{4000,5000,6000}]" or list of ints "[400,5000,6000,8000]"'
            'or all of them "[(20000, 30000), {48889, 50121}, 4000, 4004]"'
            % ports)

    return select_random(ports_set)
