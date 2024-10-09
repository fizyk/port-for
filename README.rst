========
port-for
========

.. image:: https://img.shields.io/pypi/v/port-for.svg
    :target: https://pypi.python.org/pypi/port-for/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/wheel/port-for.svg
    :target: https://pypi.python.org/pypi/port-for/
    :alt: Wheel Status

.. image:: https://img.shields.io/pypi/pyversions/port-for.svg
    :target: https://pypi.python.org/pypi/port-for/
    :alt: Supported Python Versions

.. image:: https://img.shields.io/pypi/l/port-for.svg
    :target: https://pypi.python.org/pypi/port-for/
    :alt: License



``port-for`` is a command-line utility and a python library that
helps with local TCP ports management.

It can find an unused TCP localhost port and remember the association::

    $ sudo port-for foo
    37987

This can be useful when you are installing a stack of software
with multiple parts needing port numbers.

.. note::

    If you're looking for a temporary port then ``socket.bind((host, 0))``
    is your best bet::

        >>> import socket
        >>> s = socket.socket()
        >>> s.bind(("", 0))
        >>> s.getsockname()
        ('0.0.0.0', 54485)

    ``port-for`` is necessary when you need *persistent* free local port number.

    ``port-for`` is the exact opposite of ``s.bind((host, 0))``
    in the sense that it shouldn't return ports that ``s.bind((host, 0))``
    may return (because such ports are likely to be temporary used by OS).


There are several rules ``port-for`` is trying to follow to find and
return a new unused port:

1) Port must be unused: ``port-for`` checks this by trying to connect
   to the port and to bind to it.

2) Port must be IANA unassigned and otherwise not well-known:
   this is acheived by maintaining unassigned ports list
   (parsed from IANA and Wikipedia).

3) Port shouldn't be inside ephemeral port range.
   This is important because ports from ephemeral port range can
   be assigned temporary by OS (e.g. by machine's IP stack) and
   this may prevent service restart in some circumstances.
   ``port-for`` doesn't return ports from ephemeral port ranges
   configured at the current machine.

4) Other heuristics are also applied: ``port-for`` tries to return
   a port from larger port ranges; it also doesn't return ports that are
   too close to well-known ports.

Installation
============

System-wide using easy_install (something like ``python-setuptools``
should be installed)::

    sudo pip install port-for

or::

    sudo easy_install port-for

or inside a virtualenv::

    pip install port-for

Script usage
============

``port-for <foo>`` script finds an unused port and associates
it with ``<foo>``. Subsequent calls return the same port number.

This utility doesn't actually bind the port or otherwise prevents the
port from being taken by another software. It tries to select
a port that is less likely to be used by another software
(and that is unused at the time of calling of course). Utility also makes
sure that ``port-for bar`` won't return the same port as ``port-for foo``
on the same machine.

::

    $ sudo port-for foo
    37987

    $ port-for foo
    37987

You may want to develop some naming conventions (e.g. prefix your app names)
in order to enable multiple sites on the same server::

    $ sudo port-for example.com/apache
    35456

Please note that ``port-for`` script requires read and write access
to ``/etc/port-for.conf``. This usually means regular users can read
port values but sudo is required to associate a new port.

List all associated ports::

    $ port-for --list
    foo: 37987
    example.com/apache: 35456

Remove an association::

    $ sudo port-for --unbind foo
    $ port-for --list
    example.com/apache: 35456


Library usage
=============

::

    >>> import port_for
    >>> port_for.select_random()
    37774

    >>> port_for.select_random()
    48324

    >>> 80 in port_for.available_good_ports()
    False

    >>> port_for.get_port()
    34455

    >>> port_for.get_port("1234")
    1234

    >>> port_for.get_port((2000, 3000))
    2345

    >>> port_for.get_port({4001, 4003, 4005})
    4005

    >>> port_for.get_port([{4000, 4001}, (4100, 4200)])
    4111

Dig into source code for more.

Contributing
============

Development happens at github: https://github.com/kmike/port-for/

Issue tracker: https://github.com/kmike/port-for/issues/new

Release
=======

Install pipenv and --dev dependencies first, Then run:

.. code-block::

    pipenv run tbump [NEW_VERSION]
