#!/usr/bin/env python
"""cmd.py is a command-line utility that helps with local TCP ports management.

It finds 'good' unused TCP localhost port and remembers the association.

Usage:
    port-for <NAME>
    port-for --bind <NAME>
    port-for --bind <NAME> --port <NUMBER>
    port-for <NAME> --port <NUMBER>
    port-for --unbind <NAME>
    port-for --list
    port-for --version
    port-for --help

Options:
  -h --help             Show this screen.
  -v, --version         Show version.
  -b FOO, --bind FOO    Find and return a port for FOO; this is an alias for
                        'port-for FOO'.
  -p PORT, --port PORT  (Optional) specific port number for the --bind command.
  -u FOO, --unbind FOO  Remove association for FOO.
  -l, --list            List all associated ports.
"""

import sys
from typing import Optional

import port_for
from port_for import PortStore
from port_for.docopt import docopt


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
    store = PortStore()
    args = docopt(
        __doc__,
        version="port-for %s" % port_for.__version__,
    )  # type: ignore[no-untyped-call]
    if args["<NAME>"]:
        _bind(store, args["<NAME>"], args["--port"])
    elif args["--bind"]:
        _bind(store, args["--bind"], args["--port"])
    elif args["--list"]:
        _list(store)
    elif args["--unbind"]:
        _unbind(store, args["--unbind"])


if __name__ == "__main__":
    main()
