
#############################
Changelog semver3 development
#############################

This site contains all the changes during the development phase.

.. _semver-3.0.0-dev.4:

Version 3.0.0-dev.4
===================

:Released: 2022-12-18
:Maintainer:


.. _semver-3.0.0-dev.4-bugfixes:

Bug Fixes
---------

* :gh:`374`: Correct Towncrier's config entries in the :file:`pyproject.toml` file.
  The old entries ``[[tool.towncrier.type]]`` are deprecated and need
  to be replaced by ``[tool.towncrier.fragment.<TYPE>]``.



.. _semver-3.0.0-dev.4-deprecations:

Deprecations
------------

* :gh:`372`: Deprecate support for Python 3.6.

  Python 3.6 reached its end of life and isn't supported anymore.
  At the time of writing (Dec 2022), the lowest version is 3.7.

  Although the `poll <https://github.com/python-semver/python-semver/discussions/371>`_
  didn't cast many votes, the majority agree to remove support for
  Python 3.6.


.. _semver-3.0.0-dev.4-doc:

Improved Documentation
----------------------

* :gh:`335`: Add new section "Converting versions between PyPI and semver" the limitations
  and possible use cases to convert from one into the other versioning scheme.

* :gh:`340`: Describe how to get version from a file

* :gh:`343`: Describe combining Pydantic with semver in the "Advanced topic"
  section.

* :gh:`350`: Restructure usage section. Create subdirectory "usage/" and splitted
  all section into different files.

* :gh:`351`: Introduce new topics for:

  * "Migration to semver3"
  * "Advanced topics"


.. _semver-3.0.0-dev.4-features:

Features
--------

* :pr:`359`: Add optional parameter ``optional_minor_and_patch`` in :meth:`.Version.parse`  to allow optional
  minor and patch parts.

* :pr:`362`: Make :meth:`.Version.match` accept a bare version string as match expression, defaulting to
  equality testing.

* :gh:`364`: Enhance :file:`pyproject.toml` to make it possible to use the
  :command:`pyproject-build` command from the build module.
  For more information, see :ref:`build-semver`.

* :gh:`365`: Improve :file:`pyproject.toml`.

  * Use setuptools, add metadata. Taken approach from
    `A Practical Guide to Setuptools and Pyproject.toml
    <https://godatadriven.com/blog/a-practical-guide-to-setuptools-and-pyproject-toml/>`_.
  * Doc: Describe building of semver
  * Remove :file:`.travis.yml` in :file:`MANIFEST.in`
    (not needed anymore)
  * Distinguish between Python 3.6 and others in :file:`tox.ini`
  * Add skip_missing_interpreters option for :file:`tox.ini`
  * GH Action: Upgrade setuptools and setuptools-scm and test
    against 3.11.0-rc.2


.. _semver-3.0.0-dev.4-internal:

Trivial/Internal Changes
------------------------

* :gh:`378`: Fix some typos in Towncrier configuration



----

.. _semver-3.0.0-dev.3:

Version 3.0.0-dev.3
===================

:Released: 2022-01-19
:Maintainer: Tom Schraitle


.. _semver-3.0.0-dev.3-bugfixes:

Bug Fixes
---------

* :gh:`310`: Rework API documentation.
  Follow a more "semi-manual" attempt and add auto directives
  into :file:`docs/api.rst`.


.. _semver-3.0.0-dev.3-docs:

Improved Documentation
----------------------

* :gh:`312`: Rework "Usage" section.

  * Mention the rename of :class:`~semver.version.VersionInfo` to
    :class:`~semver.version.Version` class
  * Remove semver. prefix in doctests to make examples shorter
  * Correct some references to dunder methods like
    :func:`~semver.version.Version.__getitem__`,
    :func:`~semver.version.Version.__gt__` etc.
  * Remove inconsistencies and mention module level function as
    deprecated and discouraged from using
  * Make empty :py:class:`python:super` call in :file:`semverwithvprefix.py` example

* :gh:`315`: Improve release procedure text


.. _semver-3.0.0-dev.3-trivial:

Trivial/Internal Changes
------------------------

* :gh:`309`: Some (private) functions from the :mod:`semver.version`
  module has been changed.

  The following functions got renamed:

  * function :func:`semver.version.comparator` got renamed to
    :func:`semver.version._comparator` as it is only useful
    inside the :class:`~semver.version.Version` class.
  * function :func:`semver.version.cmp` got renamed to
    :func:`semver.version._cmp` as it is only useful
    inside the :class:`~semver.version.Version` class.

  The following functions got integrated into the
  :class:`~semver.version.Version` class:

  * function :func:`semver.version._nat_cmd` as a classmethod
  * function :func:`semver.version.ensure_str`

* :gh:`313`: Correct :file:`tox.ini` for ``changelog`` entry to skip
  installation for semver. This should speed up the execution
  of towncrier.

* :gh:`316`: Comparisons of :class:`~semver.version.Version` class and other
  types return now a :py:data:`python:NotImplemented` constant instead
  of a :py:exc:`python:TypeError` exception.

  In the Python documentation, :py:data:`python:NotImplemented` recommends
  returning this constant when comparing with :py:meth:`__gt__ <python:object.__gt__>`, :py:meth:`__lt__ <python:object.__lt__>`,
  and other comparison operators "to indicate that the operation is
  not implemented with respect to the other type".

* :gh:`319`: Introduce stages in :file:`.travis.yml`
  The config file contains now two stages: check and test. If
  check fails, the test stage won't be executed. This could
  speed up things when some checks fails.

* :gh:`322`: Switch from Travis CI to GitHub Actions.

* :gh:`347`: Support Python 3.10 in GitHub Action and other config files.



----

.. _semver-3.0.0-dev.2:

Version 3.0.0-dev.2
===================

:Released: 2020-11-01
:Maintainer: Tom Schraitle


.. _semver-3.0.0-dev.2-deprecations:

Deprecations
------------

* :gh:`169`: Deprecate CLI functions not imported from :mod:`semver.cli`.


.. _semver-3.0.0-dev.2-features:

Features
--------

* :gh:`169`: Create semver package and split code among different modules in the packages.

  * Remove :file:`semver.py`
  * Create :file:`src/semver/__init__.py`
  * Create :file:`src/semver/cli.py` for all CLI methods
  * Create :file:`src/semver/_deprecated.py` for the ``deprecated`` decorator and other deprecated functions
  * Create :file:`src/semver/__main__.py` to allow calling the CLI using :command:`python -m semver`
  * Create :file:`src/semver/_types.py` to hold type aliases
  * Create :file:`src/semver/version.py` to hold the :class:`~semver.version.Version` class (old name :class:`~semver.version.VersionInfo`) and its utility functions
  * Create :file:`src/semver/__about__.py` for all the metadata variables

* :gh:`305`: Rename :class:`~semver.version.VersionInfo` to :class:`~semver.version.Version` but keep an alias for compatibility


.. _semver-3.0.0-dev.2-docs:

Improved Documentation
----------------------

* :gh:`304`: Several improvements in documentation:

  * Reorganize API documentation.
  * Add migration chapter from semver2 to semver3.
  * Distinguish between changlog for version 2 and 3

* :gh:`305`: Add note about :class:`~semver.version.Version` rename.


.. _semver-3.0.0-dev.2-trivial:

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

.. _semver-3.0.0-dev.1:

Version 3.0.0-dev.1
===================

:Released: 2020-10-26
:Maintainer: Tom Schraitle


.. _semver-3.0.0-dev.1-deprecations:

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


.. _semver-3.0.0-dev.1-features:

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
    Extract metadata directly from source (affects all the :data:`~semver.__about__.__version__`,
    :data:`~semver.__about__.__author__` etc. variables)

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

* :gh:`276`: Document how to create a sublass from :class:`~semver.version.VersionInfo` class

* :gh:`213`: Add typing information


.. _semver-3.0.0-dev.1-bugfixes:

Bug Fixes
---------

* :gh:`291`: Disallow negative numbers in VersionInfo arguments
  for ``major``, ``minor``, and ``patch``.


.. _semver-3.0.0-dev.1-docs:

Improved Documentation
----------------------

* :pr:`290`: Several improvements in the documentation:

  * New layout to distinguish from the semver2 development line.
  * Create new logo.
  * Remove any occurances of Python2.
  * Describe changelog process with Towncrier.
  * Update the release process.


.. _semver-3.0.0-dev.1-trivial:

Trivial/Internal Changes
------------------------

* :pr:`290`: Add supported Python versions to :command:`black`.
