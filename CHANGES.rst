CHANGELOG
=========

.. towncrier release notes start

port-for 1.1.0 (2026-09-05)
===========================

Features
--------

- Switch the build backend from ``setuptools`` to ``uv_build``, and build distributions via ``uv build`` in CI.


Miscellaneous
-------------

- Update pytest configuration to toml-native (`#342 <https://github.com/fizyk/port-for/issues/342>`__)
- Do not install mypy on pypy. (`#345 <https://github.com/fizyk/port-for/issues/345>`__)
- Add zizmor to pre-commit and address its findings. (`#441 <https://github.com/fizyk/port-for/issues/441>`__)
- Add release-schedule workflow replacing manual release workflow. (`#448 <https://github.com/fizyk/port-for/issues/448>`__)
- Migrated the Automerge workflow to `fizyk/actions-reuse` version 5.4.1. (`#453 <https://github.com/fizyk/port-for/issues/453>`__)
- Configure Dependabot to update pre-commit dependencies. (`#455 <https://github.com/fizyk/port-for/issues/455>`__)
- Add flake8-boolean-trap (FBT) to the ruff lint ruleset. (`#461 <https://github.com/fizyk/port-for/issues/461>`__)
- Add Python 3.15 to the CI
- Add pypy3.11 to the CI
- Adopt PEP 639 license metadata: use the ``license = "MIT"`` SPDX expression and ``license-files`` field, drop the deprecated ``License :: OSI Approved :: MIT License`` classifier.
- Drop pr template, add coderabbit configuration
- Extend pre-commit with pyproject-fmt to format pyproject.toml
- Extend pre-commit with pyproject-validator
- Migrate development environment and CI to uv
- Migrate package publishing step to trusted publishing.
- Moved mypy configuration to the pyproject.toml
- Reuse the ``build.yml`` workflow in ``pypi.yml`` so the pinned action version and dependency manager live in one place.
- Turn off windows pypy tests
- Use uv ecosystem for python deps


port-for 1.0.0 (2025-09-30)
===========================

Breaking changes
----------------

- Drop support for Python 3.9


Features
--------

- port-for supports Windows.

  Increased code compatibility with Windows (`#4 <https://github.com/fizyk/port-for/issues/4>`__)
- Replaced docopt with argparse.

  Package got a bit smaller as a result. (`#24 <https://github.com/fizyk/port-for/issues/24>`__)
- Added Python 3.14 to the supported Python Versions


Miscellaneus
------------

- Adjust links after repository transfer
- Adjust workflows for actions-reuse 3
- Changed maximum line length to 100 characters.
- Fix test_port_mix again.
- Have all code fully typed.
- Removed global variable from cli module.
- Replace black code formatting tool with ruff-format command.
- Rewritten all tests into pytest style tests.
- Update formatting with black
- Use pre-commit for maintaining code style and linting


0.7.4 (2024-10-09)
==================

Breaking changes
----------------

- Dropped support for Python 3.8 (it has reached EOL)


Features
--------

- Added Python 3.13 to the supported Python Versions


Miscellaneus
------------

- Update  to README's badges
- Update to automerge pipeline
- Updated black installation to not install on python version older than 3.12


0.7.3 (2024-09-02)
==================

Features
--------

- Adds PortType to package __all__


Miscellaneus
------------

- `#184 <https://github.com/fizyk/port-for/issues/184>`__


0.7.2 (2023-10-10)
==================

Breaking changes
----------------

- Drop support for python 3.7 (`#155 <https://github.com/fizyk/port-for/issues/155>`__)


Features
--------

- Support Python 3.12 (`#169 <https://github.com/fizyk/port-for/issues/169>`__)


Miscellaneus
------------

- `#152 <https://github.com/fizyk/port-for/issues/152>`__, `#166 <https://github.com/fizyk/port-for/issues/166>`__, `#170 <https://github.com/fizyk/port-for/issues/170>`__


0.7.1 (2023-07-14)
==================

Features
--------

- Add `PortType` type alias for easier typing related code (`#149 <https://github.com/fizyk/port-for/issues/149>`_)


0.7.0 (2023-06-15)
==================

Features
--------

- get_port will now allow passing additional exclude_ports parameter - these ports will not be chosen. (`#143 <https://github.com/fizyk/port-for/issues/143>`_)


0.6.3 (2022-12-15)
==================

Features
--------

- Add python 3.11 to the list of supported python versions. (`#111 <https://github.com/fizyk/port-for/issues/111>`_)


Miscellaneus
------------

- Use towncrier as a changelog management tool. (`#107 <https://github.com/fizyk/port-for/issues/107>`_)
- Moved development dependencies to be managed by pipenv.
  All development process can be managed  with it - which means automatic isolation. (`#108 <https://github.com/fizyk/port-for/issues/108>`_)
- Migrate versioning tool to tbump, and move package definition to pyproject.toml (`#109 <https://github.com/fizyk/port-for/issues/109>`_)
- Moved as much of the setup.cfg settings into the pyproject.toml as possible.
  Dropped pydocstyle support. (`#112 <https://github.com/fizyk/port-for/issues/112>`_)


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
