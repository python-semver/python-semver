##########
Change Log
##########

Changes for the upcoming release can be found in
the `"changelog.d" directory <https://github.com/python-semver/python-semver/tree/master/changelog.d>`_
in our repository.

..
   Do *NOT* add changelog entries here!

   This changelog is managed by towncrier and is compiled at release time.

   See https://python-semver.rtd.io/en/latest/development.html#changelog
   for details.

.. towncrier release notes start

Version 3.0.0-dev.2
===================

:Released: 2020-11-04
:Maintainer:


Improved Documentation
----------------------

* :gh:`312`: Rework "Usage" section.

  * Mention the rename of :class:`~semver.version.VersionInfo` to
    :class:`~semver.version.Version` class
  * Remove semver. prefix in doctests to make examples shorter
  * Correct some references to dunder methods like
    :func:`~.semver.version.Version.__getitem__`,
    :func:`~.semver.version.Version.__gt__` etc.
  * Remove inconsistencies and mention module level function as
    deprecated and discouraged from using
  * Make empty :py:func:`super` call in :file:`semverwithvprefix.py` example



----


Version 3.0.0-dev.2
===================

:Released: 2020-11-04
:Maintainer:


Improved Documentation
----------------------

* :gh:`312`: Rework "Usage" section.

  * Mention the rename of :class:`~semver.version.VersionInfo` to
    :class:`~semver.version.Version` class
  * Remove semver. prefix in doctests to make examples shorter
  * Correct some references to dunder methods like :func:`__getitem__`,
    :func:`__gt__` etc.
  * Remove inconsistencies and mention module level function as
    deprecated and discouraged from using
  * Make empty :py:func:`super` call in :file:`semverwithvprefix.py` example



----


Version 3.0.0-dev.2
===================

:Released: 2020-11-01
:Maintainer: Tom Schraitle


Deprecations
------------

* :gh:`169`: Deprecate CLI functions not imported from ``semver.cli``.



Features
--------

* :gh:`169`: Create semver package and split code among different modules in the packages.

  * Remove :file:`semver.py`
  * Create :file:`src/semver/__init__.py`
  * Create :file:`src/semver/cli.py` for all CLI methods
  * Create :file:`src/semver/_deprecated.py` for the ``deprecated`` decorator and other deprecated functions
  * Create :file:`src/semver/__main__.py` to allow calling the CLI using :command:`python -m semver`
  * Create :file:`src/semver/_types.py` to hold type aliases
  * Create :file:`src/semver/version.py` to hold the :class:`Version` class (old name :class:`VersionInfo`) and its utility functions
  * Create :file:`src/semver/__about__.py` for all the metadata variables

* :gh:`305`: Rename :class:`VersionInfo` to :class:`Version` but keep an alias for compatibility



Improved Documentation
----------------------

* :gh:`304`: Several improvements in documentation:

  * Reorganize API documentation.
  * Add migration chapter from semver2 to semver3.
  * Distinguish between changlog for version 2 and 3

* :gh:`305`: Add note about :class:`Version` rename.



Trivial/Internal Changes
------------------------

* :gh:`169`: Adapted infrastructure code to the new project layout.

  * Replace :file:`setup.py` with :file:`setup.cfg` because the :file:`setup.cfg` is easier to use
  * Adapt documentation code snippets where needed
  * Adapt tests
  * Changed the ``deprecated`` to hardcode the ``semver`` package name in the warning.

  Increase coverage to 100% for all non-deprecated APIs

* :gh:`304`: Support PEP-561 :file:`py.typed`.

  According to the mentioned PEP:

    "Package maintainers who wish to support type checking
    of their code MUST add a marker file named :file:`py.typed`
    to their package supporting typing."

  Add package_data to :file:`setup.cfg` to include this marker in dist
  and whl file.



----


Version 3.0.0-dev.1
===================

:Released: 2020-10-26
:Maintainer: Tom Schraitle


Deprecations
------------

* :pr:`290`: For semver 3.0.0-alpha0:

  * Remove anything related to Python2
  * In :file:`tox.ini` and :file:`.travis.yml`
    Remove targets py27, py34, py35, and pypy.
    Add py38, py39, and nightly (allow to fail)
  * In :file:`setup.py` simplified file and remove
    ``Tox`` and ``Clean`` classes
  * Remove old Python versions (2.7, 3.4, 3.5, and pypy)
    from Travis

* :gh:`234`: In :file:`setup.py` simplified file and remove
  ``Tox`` and ``Clean`` classes



Features
--------

* :pr:`290`: Create semver 3.0.0-alpha0

  * Update :file:`README.rst`, mention maintenance
    branch ``maint/v2``.
  * Remove old code mainly used for Python2 compatibility,
    adjusted code to support Python3 features.
  * Split test suite into separate files under :file:`tests/`
    directory
  * Adjust and update :file:`setup.py`. Requires Python >=3.6.*
    Extract metadata directly from source (affects all the ``__version__``,
    ``__author__`` etc. variables)

* :gh:`270`: Configure Towncrier (:pr:`273`:)

  * Add :file:`changelog.d/.gitignore` to keep this directory
  * Create :file:`changelog.d/README.rst` with some descriptions
  * Add :file:`changelog.d/_template.rst` as Towncrier template
  * Add ``[tool.towncrier]`` section in :file:`pyproject.toml`
  * Add "changelog" target into :file:`tox.ini`. Use it like
    :command:`tox -e changelog -- CMD` whereas ``CMD`` is a
    Towncrier command. The default :command:`tox -e changelog`
    calls Towncrier to create a draft of the changelog file
    and output it to stdout.
  * Update documentation and add include a new section
    "Changelog" included from :file:`changelog.d/README.rst`.

* :gh:`276`: Document how to create a sublass from :class:`VersionInfo` class

* :gh:`213`: Add typing information


Bug Fixes
---------

* :gh:`291`: Disallow negative numbers in VersionInfo arguments
  for ``major``, ``minor``, and ``patch``.



Improved Documentation
----------------------

* :pr:`290`: Several improvements in the documentation:

  * New layout to distinguish from the semver2 development line.
  * Create new logo.
  * Remove any occurances of Python2.
  * Describe changelog process with Towncrier.
  * Update the release process.



Trivial/Internal Changes
------------------------

* :pr:`290`: Add supported Python versions to :command:`black`.


..
    Local variables:
    coding: utf-8
    mode: text
    mode: rst
    End:
    vim: fileencoding=utf-8 filetype=rst :
