##########
Change Log
##########

Changes for the upcoming release can be found in
the `"changelog.d" directory <https://github.com/python-semver/python-semver/tree/master/changelog.d>`_
in our repository.

This section covers the changes between major version 2 and version 3.

..
   Do *NOT* add changelog entries here!

   This changelog is managed by towncrier and is compiled at release time.

   See https://python-semver.rtd.io/en/latest/development.html#changelog
   for details.

.. towncrier release notes start

Version 3.0.4
=============

:Released: 2025-01-24
:Maintainer: Tom Schraitle


Bug Fixes
---------

* :gh:`459`: Fix 3.0.3:

  * :pr:`457`: Re-enable Trove license identifier
  * :pr:`456`: Fix source dist file


----


Version 3.0.3
=============

:Released: 2025-01-18
:Maintainer: Tom Schraitle


Bug Fixes
---------

* :pr:`453`: The check in ``_comparator`` does not match the check in :meth:`Version.compare`. 
  This breaks comparision with subclasses.



Improved Documentation
----------------------

* :pr:`435`: Several small improvements for documentation:

  * Add meta description to improve SEO
  * Use canonicals on ReadTheDocs (commit 87f639f)
  * Pin versions for reproducable doc builds (commit 03fb990)
  * Add missing :file:`.readthedocs.yaml` file (commit ec9348a)
  * Correct some smaller issues when building (commit f65feab)

* :pr:`436`: Move search box more at the top. This makes it easier for
  users as if the TOC is long, the search box isn't visible
  anymore.



Features
--------

* :pr:`439`: Improve type hints to fix TODOs



Internal Changes
----------------

* :pr:`440`: Update workflow file

* :pr:`446`: Add Python 3.13 to GitHub Actions

* :pr:`447`: Modernize project configs with :file:`pyproject.toml` and
  use Astral's uv command.

  * In :file:`pyproject.toml`:

    * Move all project related data from :file:`setup.cfg` to :file:`pyproject.toml`
    * Use new dependency group from :pep:`735`
    * Consolidate flake8, isort, pycodestyle with ruff
    * Split towncrier config type "trivial" into "trivial" and "internal"

  * Create config file for ruff (:file:`.ruff.toml`)
  * Create config file for pytest (:file:`.pytest.ini`)
  * Simplify :file:`tox.ini` and remove old stuff
  * Document installation with new :command:`uv` command
  * Simplify Sphinx config with :func:`find_version()`
  * Update the authors
  * Use :command:`uv` in GitHub Action :file:`python-testing.yml` workflow

* Update :file:`release-procedure.md`.

* :pr:`451`: Turn our Markdown issue templates into YAML


Trivial Changes
---------------

* :pr:`438`: Replace organization placeholder in license

* :pr:`445`: Improve private :func:`_nat_cmp` method:

  * Remove obsolete else.
  * Find a better way to identify digits without the :mod:`re` module.
  * Fix docstring in :meth:`Version.compare`



----


Version 3.0.2
=============

:Released: 2023-10-09
:Maintainer: Tom Schraitle


Bug Fixes
---------

* :pr:`418`: Replace :class:`~collection.OrderedDict` with :class:`dict`.

  The dict datatype is ordered since Python 3.7. As we do not support
  Python 3.6 anymore, it can be considered safe to avoid :class:`~collection.OrderedDict`.
  Related to :gh:`419`.

* :pr:`426`: Fix :meth:`~semver.version.Version.replace` method to use the derived class
  of an instance instead of :class:`~semver.version.Version` class.



Improved Documentation
----------------------

* :pr:`431`: Clarify version policy for the different semver versions (v2, v3, >v3)
  and the supported Python versions.

* :gh:`432`: Improve external doc links to Python and Pydantic.



Features
--------

* :pr:`417`: Amend GitHub Actions to check against MacOS.



Trivial/Internal Changes
------------------------

* :pr:`420`: Introduce :py:class:`~typing.ClassVar` for some :class:`~semver.version.Version`
  class variables, mainly :data:`~semver.version.Version.NAMES` and some private.

* :pr:`421`: Insert mypy configuration into :file:`pyproject.toml` and remove
  config options from :file:`tox.ini`.



----


Version 3.0.1
=============

:Released: 2023-06-14
:Maintainer: Tom Schraitle


Bug Fixes
---------

* :gh:`410`: Export functions properly using ``__all__`` in ``__init__.py``.



----


Version 3.0.0
=============

:Released: 2023-04-02
:Maintainer: Tom Schraitle


Bug Fixes
---------

* :gh:`291`: Disallow negative numbers in VersionInfo arguments
  for ``major``, ``minor``, and ``patch``.

* :gh:`310`: Rework API documentation.
  Follow a more "semi-manual" attempt and add auto directives
  into :file:`docs/api.rst`.

* :gh:`344`: Allow empty string, a string with a prefix, or ``None``
  as token in
  :meth:`~semver.version.Version.bump_build` and
  :meth:`~semver.version.Version.bump_prerelease`.

* :gh:`374`: Correct Towncrier's config entries in the :file:`pyproject.toml` file.
  The old entries ``[[tool.towncrier.type]]`` are deprecated and need
  to be replaced by ``[tool.towncrier.fragment.<TYPE>]``.

* :pr:`384`: General cleanup, reformat files:

  * Reformat source code with black again as some config options
    did accidentely exclude the semver source code.
    Mostly remove some includes/excludes in the black config.
  * Integrate concurrency in GH Action
  * Ignore Python files on project dirs in .gitignore
  * Remove unused patterns in MANIFEST.in
  * Use ``extend-exclude`` for flake in :file:`setup.cfg`` and adapt list.
  * Use ``skip_install=True`` in :file:`tox.ini` for black

* :pr:`393`: Fix command :command:`python -m semver` to avoid the error "invalid choice"

* :pr:`396`: Calling :meth:`~semver.version.Version.parse` on a derived class will show correct type of derived class.


Deprecations
------------

* :gh:`169`: Deprecate CLI functions not imported from ``semver.cli``.

* :gh:`234`: In :file:`setup.py` simplified file and remove
  ``Tox`` and ``Clean`` classes

* :gh:`284`: Deprecate the use of :meth:`~Version.isvalid`.

  Rename :meth:`~semver.version.Version.isvalid`
  to :meth:`~semver.version.Version.is_valid`
  for consistency reasons with :meth:`~semver.version.Version.is_compatible`.


* :pr:`290`: For semver 3.0.0-alpha0 deprecated:

  * Remove anything related to Python2
  * In :file:`tox.ini` and :file:`.travis.yml`
    Remove targets py27, py34, py35, and pypy.
    Add py38, py39, and nightly (allow to fail)
  * In :file:`setup.py` simplified file and remove
    ``Tox`` and ``Clean`` classes
  * Remove old Python versions (2.7, 3.4, 3.5, and pypy)
    from Travis

* :gh:`372`: Deprecate support for Python 3.6.

  Python 3.6 reached its end of life and isn't supported anymore.
  At the time of writing (Dec 2022), the lowest version is 3.7.

  Although the `poll <https://github.com/python-semver/python-semver/discussions/371>`_
  didn't cast many votes, the majority agreed to remove support for
  Python 3.6.

* :pr:`402`: Keep :func:`semver.compare <semver._deprecated.compare>`.
   Although it breaks consistency with module level functions, it seems it's
   a much needed/used function. It's still unclear if we should deprecate
   this function or not (that's why we use :py:exc:`PendingDeprecationWarning`).

   As we don't have a uniform initializer yet, this function stays in the
   :file:`_deprecated.py` file for the time being until we find a better solution. See :gh:`258` for details.


Features
--------

* :gh:`169`: Create semver package and split code among different modules in the packages:

  * Remove :file:`semver.py`
  * Create :file:`src/semver/__init__.py`
  * Create :file:`src/semver/cli.py` for all CLI methods
  * Create :file:`src/semver/_deprecated.py` for the ``deprecated`` decorator and other deprecated functions
  * Create :file:`src/semver/__main__.py` to allow calling the CLI using :command:`python -m semver`
  * Create :file:`src/semver/_types.py` to hold type aliases
  * Create :file:`src/semver/version.py` to hold the :class:`Version` class (old name :class:`VersionInfo`) and its utility functions
  * Create :file:`src/semver/__about__.py` for all the metadata variables

* :gh:`213`: Add typing information

* :gh:`284`: Implement :meth:`~semver.version.Version.is_compatible` to make "is self compatible with X".

* :gh:`305`: Rename :class:`~semver.version.VersionInfo` to :class:`~semver.version.Version` but keep an alias for compatibility

* :pr:`359`: Add optional parameter ``optional_minor_and_patch`` in :meth:`~semver.version.Version.parse`  to allow optional
  minor and patch parts.

* :pr:`362`: Make :meth:`~semver.version.Version.match` accept a bare version string as match expression, defaulting to equality testing.

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



Improved Documentation
----------------------

* :gh:`276`: Document how to create a sublass from :class:`~semver.version.VersionInfo` class

* :gh:`284`: Document deprecation of :meth:`~semver.version.Version.isvalid`.

* :pr:`290`: Several improvements in the documentation:

  * New layout to distinguish from the semver2 development line.
  * Create new logo.
  * Remove any occurances of Python2.
  * Describe changelog process with Towncrier.
  * Update the release process.

* :gh:`304`: Several improvements in documentation:

  * Reorganize API documentation.
  * Add migration chapter from semver2 to semver3.
  * Distinguish between changlog for version 2 and 3

* :gh:`305`: Add note about :class:`~semver.version.Version` rename.

* :gh:`312`: Rework "Usage" section.

  * Mention the rename of :class:`~semver.version.VersionInfo` to
    :class:`~semver.version.Version` class
  * Remove semver. prefix in doctests to make examples shorter
  * Correct some references to dunder methods like
    :func:`~semver.version.Version.__getitem__`,
    :func:`~semver.version.Version.__gt__` etc.
  * Remove inconsistencies and mention module level function as
    deprecated and discouraged from using
  * Make empty :py:func:`super` call in :file:`semverwithvprefix.py` example

* :gh:`315`: Improve release procedure text

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

* :pr:`392`: Fix the example in the documentation for combining semver and pydantic.


Trivial/Internal Changes
------------------------

* :gh:`169`: Adapted infrastructure code to the new project layout.

  * Replace :file:`setup.py` with :file:`setup.cfg` because the :file:`setup.cfg` is easier to use
  * Adapt documentation code snippets where needed
  * Adapt tests
  * Changed the ``deprecated`` to hardcode the ``semver`` package name in the warning.

  Increase coverage to 100% for all non-deprecated APIs

* :pr:`290`: Add supported Python versions to :command:`black`.

* :gh:`304`: Support PEP-561 :file:`py.typed`.

  According to the mentioned PEP:

    "Package maintainers who wish to support type checking
    of their code MUST add a marker file named :file:`py.typed`
    to their package supporting typing."

  Add package_data to :file:`setup.cfg` to include this marker in dist
  and whl file.

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
  types return now a :py:const:`NotImplemented` constant instead
  of a :py:exc:`TypeError` exception.

  The `NotImplemented`_ section of the Python documentation recommends
  returning this constant when comparing with ``__gt__``, ``__lt__``,
  and other comparison operators to "to indicate that the operation is
  not implemented with respect to the other type".

  .. _NotImplemented: https://docs.python.org/3/library/constants.html#NotImplemented

* :gh:`319`: Introduce stages in :file:`.travis.yml`
  The config file contains now two stages: check and test. If
  check fails, the test stage won't be executed. This could
  speed up things when some checks fails.

* :gh:`322`: Switch from Travis CI to GitHub Actions.

* :gh:`347`: Support Python 3.10 in GitHub Action and other config files.

* :gh:`378`: Fix some typos in Towncrier configuration

* :gh:`388`: For pytest, switch to the more modern :mod:`importlib` approach
  as it doesn't require to modify :data:`sys.path`:
  https://docs.pytest.org/en/7.2.x/explanation/pythonpath.html

* :pr:`389`: Add public class variable :data:`Version.NAMES <semver.version.Version.NAMES>`.

  This class variable contains a tuple of strings that contains the names of
  all attributes of a Version (like ``"major"``, ``"minor"`` etc).

  In cases we need to have dynamical values, this makes it easier to iterate.



..
    Local variables:
    coding: utf-8
    mode: text
    mode: rst
    End:
    vim: fileencoding=utf-8 filetype=rst :
