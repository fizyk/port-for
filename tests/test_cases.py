# -*- coding: utf-8 -*-
import unittest
import tempfile
import mock
import socket
import os
from typing import Union, List, Set, Tuple

import pytest

import port_for
from port_for.api import get_port
from port_for.utils import ranges_to_set


def test_common_ports() -> None:
    assert not port_for.is_available(80)
    assert not port_for.is_available(11211)


def test_good_port_ranges() -> None:
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
    assert len(port_for.good_port_ranges()) > 10
    assert len(port_for.available_good_ports()) > 1000


def test_binding() -> None:
    # low ports are not available
    assert port_for.port_is_used(10)


def test_binding_high() -> None:
    s = socket.socket()
    s.bind(("", 0))
    port = s.getsockname()[1]
    assert port_for.port_is_used(port)
    s.close()
    assert not port_for.port_is_used(port)


def test_get_port_random() -> None:
    """Test case allowing get port to randomly select any port."""
    assert get_port(None)


def test_get_port_none() -> None:
    """Test special case for get_port to return None."""
    assert not get_port(-1)


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
    port_range: Union[List[Tuple[int, int]], Tuple[int, int]]
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
def test_get_port_from_set(port_set: Union[List[Set[int]], Set[int]]) -> None:
    """Test getting random port from given set."""
    assert get_port(port_set) in {4001, 4002, 4003}


def test_port_mix() -> None:
    """Test getting random port from given set and range."""
    sets_and_ranges: List[Union[Tuple[int, int], Set[int]]] = [
        (2000, 3000),
        {4001, 4002, 4003},
    ]
    assert get_port(sets_and_ranges) in set(range(2000, 3000 + 1)) and {
        4001,
        4002,
        4003,
    }


class SelectPortTest(unittest.TestCase):
    @mock.patch("port_for.api.port_is_used")
    def test_all_used(self, port_is_used: mock.MagicMock) -> None:
        port_is_used.return_value = True
        self.assertRaises(port_for.PortForException, port_for.select_random)

    @mock.patch("port_for.api.port_is_used")
    def test_random_port(self, port_is_used: mock.MagicMock) -> None:
        ports = set([1, 2, 3])
        used = {1: True, 2: False, 3: True}
        port_is_used.side_effect = lambda port: used[port]

        for x in range(100):
            self.assertEqual(port_for.select_random(ports), 2)


class StoreTest(unittest.TestCase):
    def setUp(self) -> None:
        fd, self.fname = tempfile.mkstemp()
        self.store = port_for.PortStore(self.fname)

    def tearDown(self) -> None:
        os.remove(self.fname)

    def test_store(self) -> None:
        assert self.store.bound_ports() == []

        port = self.store.bind_port("foo")
        self.assertTrue(port)
        self.assertEqual(self.store.bound_ports(), [("foo", port)])
        self.assertEqual(port, self.store.bind_port("foo"))

        port2 = self.store.bind_port("aar")
        self.assertNotEqual(port, port2)
        self.assertEqual(
            self.store.bound_ports(), [("foo", port), ("aar", port2)]
        )

        self.store.unbind_port("aar")
        self.assertEqual(self.store.bound_ports(), [("foo", port)])

    def test_rebind(self) -> None:
        # try to rebind an used port for an another app
        port = self.store.bind_port("foo")
        self.assertRaises(
            port_for.PortForException, self.store.bind_port, "baz", port
        )

    def test_change_port(self) -> None:
        # changing app ports is not supported.
        port = self.store.bind_port("foo")
        another_port = port_for.select_random()
        assert port != another_port
        self.assertRaises(
            port_for.PortForException, self.store.bind_port, "foo", another_port
        )

    def test_bind_unavailable(self) -> None:
        # it is possible to explicitly bind currently unavailable port
        port = self.store.bind_port("foo", 80)
        self.assertEqual(port, 80)
        self.assertEqual(self.store.bound_ports(), [("foo", 80)])

    def test_bind_non_auto(self) -> None:
        # it is possible to pass a port
        port = port_for.select_random()
        res_port = self.store.bind_port("foo", port)
        self.assertEqual(res_port, port)
