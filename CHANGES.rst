CHANGELOG
=========

.. towncrier release notes start

0.6.3 (2022-12-15)
==================

Features
--------

- Add python 3.11 to the list of supported python versions. (`#111 <https://https://github.com/kmike/port-for/issues/111>`_)


Miscellaneus
------------

- Use towncrier as a changelog management tool. (`#107 <https://https://github.com/kmike/port-for/issues/107>`_)
- Moved development dependencies to be managed by pipenv.
  All development process can be managed  with it - which means automatic isolation. (`#108 <https://https://github.com/kmike/port-for/issues/108>`_)
- Migrate versioning tool to tbump, and move package definition to pyproject.toml (`#109 <https://https://github.com/kmike/port-for/issues/109>`_)
- Moved as much of the setup.cfg settings into the pyproject.toml as possible.
  Dropped pydocstyle support. (`#112 <https://https://github.com/kmike/port-for/issues/112>`_)


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
