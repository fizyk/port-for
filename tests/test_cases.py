"""Test cases."""

import socket
import sys
from typing import Union

import pytest

import port_for
from port_for.api import get_port
from port_for.utils import ranges_to_set


def test_common_ports() -> None:
    """Check common ports (not available)."""
    assert not port_for.is_available(80)
    assert not port_for.is_available(11211)


def test_good_port_ranges() -> None:
    """Select good ranges of ports aout of provided."""
    ranges = [
        (10, 15),  # too short
        (100, 200),  # good
        (220, 245),  # a bit short
        (300, 330),  # good
        (440, 495),  # also good
    ]

    ports = ranges_to_set(ranges)
    good_ranges = port_for.good_port_ranges(ports, 20, 3)
    assert good_ranges == [(103, 197), (443, 492), (303, 327)], good_ranges


def test_something_works() -> None:
    """Test default behaviour of good_port_ranges and available_good_ports."""
    assert len(port_for.good_port_ranges()) > 10
    assert len(port_for.available_good_ports()) > 1000


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Windows runner seems to allow binding low ports.",
)
def test_binding() -> None:
    """Low ports are not available (for user without root privileges)."""
    assert port_for.port_is_used(10)


def test_binding_high() -> None:
    """Test ports that are not used."""
    with socket.socket() as s:
        s.bind(("", 1025))
        port = s.getsockname()[1]
        assert port_for.port_is_used(port)
    assert not port_for.port_is_used(port)


def test_get_port_random() -> None:
    """Test case allowing get port to randomly select any port."""
    assert get_port(None)


def test_get_port_none() -> None:
    """Test special case for get_port to return None."""
    assert not get_port(-1)


def test_get_port_exclude() -> None:
    """Only one port is available at that range."""
    assert 8002 == get_port(
        (8000, 8010),
        [8000, 8001, 8003, 8004, 8005, 8006, 8007, 8008, 8009, 8010],
    )


@pytest.mark.parametrize("port", (1234, "1234"))
def test_get_port_specific(port: Union[str, int]) -> None:
    """Test special case for get_port to return same value."""
    assert get_port(port) == 1234


@pytest.mark.parametrize(
    "port_range",
    (
        [(2000, 3000)],
        (2000, 3000),
    ),
)
def test_get_port_from_range(
    port_range: Union[list[tuple[int, int]], tuple[int, int]],
) -> None:
    """Test getting random port from given range."""
    assert get_port(port_range) in list(range(2000, 3000 + 1))


@pytest.mark.parametrize(
    "port_set",
    (
        [{4001, 4002, 4003}],
        {4001, 4002, 4003},
    ),
)
def test_get_port_from_set(port_set: Union[list[set[int]], set[int]]) -> None:
    """Test getting random port from given set."""
    assert get_port(port_set) in {4001, 4002, 4003}


def test_port_mix() -> None:
    """Test getting random port from given set and range."""
    sets_and_ranges: list[Union[tuple[int, int], set[int]]] = [
        (2000, 3000),
        {4001, 4002, 4003},
    ]
    want_set = set(range(2000, 3000 + 1)) | {
        4001,
        4002,
        4003,
    }
    assert get_port(sets_and_ranges) in want_set
