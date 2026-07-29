"""Tests for port_for.select_random."""

import pytest
from pytest import MonkeyPatch

import port_for


def test_all_used(monkeypatch: MonkeyPatch) -> None:
    """Check behaviour if there are no ports to use."""
    monkeypatch.setattr(port_for.api, "port_is_used", lambda port: True)
    with pytest.raises(port_for.PortForException):
        port_for.select_random()


def test_random_port(monkeypatch: MonkeyPatch) -> None:
    """Test random ports."""
    ports = {1, 2, 3}
    used = {1: True, 2: False, 3: True}
    monkeypatch.setattr(port_for.api, "port_is_used", lambda port: used[port])

    for x in range(100):
        assert port_for.select_random(ports) == 2
