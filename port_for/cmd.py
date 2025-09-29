"""Command-line utility that helps with local TCP ports management.

It finds 'good' unused TCP localhost port and remembers the association.
"""

import sys
from typing import Optional

import port_for
from port_for import PortStore


def _list(store: PortStore) -> None:
    for app, port in store.bound_ports():
        sys.stdout.write("%s: %s\n" % (app, port))


def _bind(store: PortStore, app: str, port: Optional[str] = None) -> None:
    bound_port = store.bind_port(app, port)
    sys.stdout.write("%s\n" % bound_port)


def _unbind(store: PortStore, app: str) -> None:
    store.unbind_port(app)


def main() -> None:
    """port-for executable entrypoint."""
    import argparse

    parser = argparse.ArgumentParser(
        prog="port-for",
        description=("Command-line utility to manage local TCP port associations."),
    )
    parser.add_argument(
        "name",
        nargs="?",
        metavar="NAME",
        help="Application name to bind a port for",
    )
    parser.add_argument(
        "--bind",
        "-b",
        metavar="FOO",
        dest="bind",
        help="Find and return a port for FOO; alias for 'port-for FOO'",
    )
    parser.add_argument(
        "--port",
        "-p",
        metavar="PORT",
        dest="port",
        help="Optional specific port number for the bind command",
    )
    parser.add_argument(
        "--unbind",
        "-u",
        metavar="FOO",
        dest="unbind",
        help="Remove association for FOO",
    )
    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        dest="list_",
        help="List all associated ports",
    )
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"port-for {port_for.__version__}",
    )

    args = parser.parse_args()

    store = PortStore()

    if args.name:
        _bind(store, args.name, args.port)
    elif args.bind:
        _bind(store, args.bind, args.port)
    elif args.list_:
        _list(store)
    elif args.unbind:
        _unbind(store, args.unbind)
