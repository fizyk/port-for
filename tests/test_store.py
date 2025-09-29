"""Tests for PortStore."""

from typing import Generator

import pytest
from pytest import TempPathFactory

import port_for
from port_for import PortStore


@pytest.fixture
def port_store(
    tmp_path_factory: TempPathFactory,
) -> Generator[PortStore, None, None]:
    """Create an initialized port store."""
    store_path = tmp_path_factory.mktemp("port_store") / "port_store.cfg"
    yield PortStore(str(store_path))


def test_store(port_store: PortStore) -> None:
    """Test port store."""
    assert port_store.bound_ports() == []

    port = port_store.bind_port("foo")
    assert port
    assert port_store.bound_ports() == [("foo", port)]
    assert port == port_store.bind_port("foo")

    port2 = port_store.bind_port("aar")
    assert port != port2
    assert port_store.bound_ports() == [("foo", port), ("aar", port2)]

    port_store.unbind_port("aar")
    assert port_store.bound_ports() == [("foo", port)]


def test_rebind(port_store: PortStore) -> None:
    """Try to rebind a used port for another app."""
    port = port_store.bind_port("foo")
    with pytest.raises(port_for.PortForException):
        port_store.bind_port("baz", port)


def test_change_port(port_store: PortStore) -> None:
    """Changing app ports is not supported."""
    port = port_store.bind_port("foo")
    another_port = port_for.select_random()
    assert port != another_port
    with pytest.raises(port_for.PortForException):
        port_store.bind_port("foo", another_port)


def test_bind_unavailable(port_store: PortStore) -> None:
    """It is possible to explicitly bind currently unavailable port."""
    port = port_store.bind_port("foo", 80)
    assert port == 80
    assert port_store.bound_ports() == [("foo", 80)]


def test_bind_non_auto(port_store: PortStore) -> None:
    """It is possible to pass a port."""
    port = port_for.select_random()
    res_port = port_store.bind_port("foo", port)
    assert res_port == port
