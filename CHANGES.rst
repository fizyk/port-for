CHANGELOG
=========

.. towncrier release notes start

0.7.2 (2023-10-10)
==================

Breaking changes
----------------

- Drop support for python 3.7 (`#155 <https://github.com/kmike/port-for/issues/155>`__)


Features
--------

- Support Python 3.12 (`#169 <https://github.com/kmike/port-for/issues/169>`__)


Miscellaneus
------------

- `#152 <https://github.com/kmike/port-for/issues/152>`__, `#166 <https://github.com/kmike/port-for/issues/166>`__, `#170 <https://github.com/kmike/port-for/issues/170>`__


0.7.1 (2023-07-14)
==================

Features
--------

- Add `PortType` type alias for easier typing related code (`#149 <https://github.com/kmike/port-for/issues/149>`_)


0.7.0 (2023-06-15)
==================

Features
--------

- get_port will now allow passing additional exclude_ports parameter - these ports will not be chosen. (`#143 <https://github.com/kmike/port-for/issues/143>`_)


0.6.3 (2022-12-15)
==================

Features
--------

- Add python 3.11 to the list of supported python versions. (`#111 <https://github.com/kmike/port-for/issues/111>`_)


Miscellaneus
------------

- Use towncrier as a changelog management tool. (`#107 <https://github.com/kmike/port-for/issues/107>`_)
- Moved development dependencies to be managed by pipenv.
  All development process can be managed  with it - which means automatic isolation. (`#108 <https://github.com/kmike/port-for/issues/108>`_)
- Migrate versioning tool to tbump, and move package definition to pyproject.toml (`#109 <https://github.com/kmike/port-for/issues/109>`_)
- Moved as much of the setup.cfg settings into the pyproject.toml as possible.
  Dropped pydocstyle support. (`#112 <https://github.com/kmike/port-for/issues/112>`_)


0.6.2
----------

Misc
++++

- Added Python 3.10 to trove classifiers and to CI

0.6.1
----------

Bugfix
++++++

- Fixed typing definition for get_port function

0.6.0
----------

Feature
+++++++

- Added `get_port` helper that can randomly select open port out of given set, or range-tuple
- Added type annotations and compatibility with PEP 561
- Support only python 3.7 and up
