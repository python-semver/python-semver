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



----


Version 2.13.0
==============

:Released: 2020-10-20
:Maintainer: Tom Schraitle


Features
--------

* :pr:`287`: Document how to create subclass from ``VersionInfo``


Bug Fixes
---------

* :pr:`283`: Ensure equal versions have equal hashes.
  Version equality means for semver, that ``major``,
  ``minor``, ``patch``, and ``prerelease`` parts are
  equal in both versions you compare. The ``build`` part
  is ignored.


Additions
---------

n/a


Deprecations
------------

n/a


----


Version 2.12.0
==============

:Released: 2020-10-19
:Maintainer: Tom Schraitle


Bug Fixes
---------

* :gh:`291` (:pr:`292`): Disallow negative numbers of
  ``major``, ``minor``, and ``patch`` for :class:`semver.VersionInfo`


----


Version 2.11.0
==============

:Released: 2020-10-17
:Maintainer: Tom Schraitle


Bug Fixes
---------

* :gh:`276` (:pr:`277`): ``VersionInfo.parse`` should be a class method
   Also add authors and update changelog in :gh:`286`
* :gh:`274` (:pr:`275`): Py2 vs. Py3 incompatibility TypeError


----


Version 2.10.2
==============

:Released: 2020-06-15
:Maintainer: Tom Schraitle

Features
--------

:gh:`268`: Increase coverage


Bug Fixes
---------

* :gh:`260` (:pr:`261`): Fixed ``__getitem__`` returning None on wrong parts
* :pr:`263`: Doc: Add missing "install" subcommand for openSUSE


Deprecations
------------

* :gh:`160` (:pr:`264`):
    * :func:`semver.max_ver`
    * :func:`semver.min_ver`


----


Version 2.10.1
==============

:Released: 2020-05-13
:Maintainer: Tom Schraitle


Features
--------

* :pr:`249`: Added release policy and version restriction in documentation to
  help our users which would like to stay on the major 2 release.
* :pr:`250`: Simplified installation semver on openSUSE with ``obs://``.
* :pr:`256`: Made docstrings consistent



Bug Fixes
---------

* :gh:`251` (:pr:`254`): Fixed return type of ``semver.VersionInfo.next_version``
  to always return a ``VersionInfo`` instance.


----



Version 2.10.0
==============

:Released: 2020-05-05
:Maintainer: Tom Schraitle

Features
--------

* :pr:`138`: Added ``__getitem__`` magic method to ``semver.VersionInfo`` class.
  Allows to access a version like ``version[1]``.
* :pr:`235`: Improved documentation and shift focus on ``semver.VersionInfo`` instead of advertising
  the old and deprecated module-level functions.
* :pr:`230`: Add version information in some functions:

  * Use ``.. versionadded::`` RST directive in docstrings to
    make it more visible when something was added
  * Minor wording fix in docstrings (versions -> version strings)


Bug Fixes
---------

* :gh:`224` (:pr:`226`): In ``setup.py``, replaced in class ``clean``,
  ``super(CleanCommand, self).run()`` with ``CleanCommand.run(self)``
* :gh:`244` (:pr:`245`): Allow comparison with ``VersionInfo``, tuple/list, dict, and string.


Additions
---------

* :pr:`228`: Added better doctest integration


Deprecations
------------
* :gh:`225` (:pr:`229`): Output a DeprecationWarning for the following functions:

  - ``semver.parse``
  - ``semver.parse_version_info``
  - ``semver.format_version``
  - ``semver.bump_{major,minor,patch,prerelease,build}``
  - ``semver.finalize_version``
  - ``semver.replace``
  - ``semver.VersionInfo._asdict`` (use the new, public available
    function ``semver.VersionInfo.to_dict()``)
  - ``semver.VersionInfo._astuple`` (use the new, public available
    function ``semver.VersionInfo.to_tuple()``)

  These deprecated functions will be removed in semver 3.


----


Version 2.9.1
=============
:Released: 2020-02-16
:Maintainer: Tom Schraitle

Features
--------

* :gh:`177` (:pr:`178`): Fixed repository and CI links (moved https://github.com/k-bx/python-semver/ repository to https://github.com/python-semver/python-semver/)
* :pr:`179`: Added note about moving this project to the new python-semver organization on GitHub
* :gh:`187` (:pr:`188`): Added logo for python-semver organization and documentation
* :gh:`191` (:pr:`194`): Created manpage for pysemver
* :gh:`196` (:pr:`197`): Added distribution specific installation instructions
* :gh:`201` (:pr:`202`): Reformatted source code with black
* :gh:`208` (:pr:`209`): Introduce new function :func:`semver.VersionInfo.isvalid`
  and extend :command:`pysemver` with :command:`check` subcommand
* :gh:`210` (:pr:`215`): Document how to deal with invalid versions
* :pr:`212`: Improve docstrings according to PEP257

Bug Fixes
---------

* :gh:`192` (:pr:`193`): Fixed "pysemver" and "pysemver bump" when called without arguments


----

Version 2.9.0
=============
:Released: 2019-10-30
:Maintainer: Sébastien Celles <s.celles@gmail.com>

Features
--------

* :gh:`59` (:pr:`164`): Implemented a command line interface
* :gh:`85` (:pr:`147`, :pr:`154`): Improved contribution section
* :gh:`104` (:pr:`125`): Added iterator to :func:`semver.VersionInfo`
* :gh:`112`, :gh:`113`: Added Python 3.7 support
* :pr:`120`: Improved test_immutable function with properties
* :pr:`125`: Created :file:`setup.cfg` for pytest and tox
* :gh:`126` (:pr:`127`): Added target for documentation in :file:`tox.ini`
* :gh:`142` (:pr:`143`): Improved usage section
* :gh:`144` (:pr:`156`): Added :func:`semver.replace` and :func:`semver.VersionInfo.replace`
  functions
* :gh:`145` (:pr:`146`): Added posargs in :file:`tox.ini`
* :pr:`157`: Introduce :file:`conftest.py` to improve doctests
* :pr:`165`: Improved code coverage
* :pr:`166`: Reworked :file:`.gitignore` file
* :gh:`167` (:pr:`168`): Introduced global constant :data:`SEMVER_SPEC_VERSION`

Bug Fixes
---------

* :gh:`102`: Fixed comparison between VersionInfo and tuple
* :gh:`103`: Disallow comparison between VersionInfo and string (and int)
* :gh:`121` (:pr:`122`): Use python3 instead of python3.4 in :file:`tox.ini`
* :pr:`123`: Improved :func:`__repr__` and derive class name from :func:`type`
* :gh:`128` (:pr:`129`): Fixed wrong datatypes in docstring for :func:`semver.format_version`
* :gh:`135` (:pr:`140`): Converted prerelease and build to string
* :gh:`136` (:pr:`151`): Added testsuite to tarball
* :gh:`154` (:pr:`155`): Improved README description

Removals
--------

* :gh:`111` (:pr:`110`): Dropped Python 3.3
* :gh:`148` (:pr:`149`): Removed and replaced ``python setup.py test``


----

Version 2.8.2
=============
:Released: 2019-05-19
:Maintainer: Sébastien Celles <s.celles@gmail.com>

Skipped, not released.

----

Version 2.8.1
=============
:Released: 2018-07-09
:Maintainer: Sébastien Celles <s.celles@gmail.com>

Features
--------

* :gh:`40` (:pr:`88`): Added a static parse method to VersionInfo
* :gh:`77` (:pr:`47`): Converted multiple tests into pytest.mark.parametrize
* :gh:`87`, :gh:`94` (:pr:`93`): Removed named tuple inheritance.
* :gh:`89` (:pr:`90`): Added doctests.

Bug Fixes
---------

* :gh:`98` (:pr:`99`): Set prerelease and build to None by default
* :gh:`96` (:pr:`97`): Made VersionInfo immutable


----

Version 2.8.0
=============
:Released: 2018-05-16
:Maintainer: Sébastien Celles <s.celles@gmail.com>


Changes
-------

* :gh:`82` (:pr:`83`): Renamed :file:`test.py` to :file:`test_semver.py` so 
  py.test can autodiscover test file

Additions
---------

* :gh:`79` (:pr:`81`, :pr:`84`): Defined and improve a release procedure file
* :gh:`72`, :gh:`73` (:pr:`75`): Implemented :func:`__str__` and :func:`__hash__`

Removals
--------

* :gh:`76` (:pr:`80`): Removed Python 2.6 compatibility


..
    Local variables:
    coding: utf-8
    mode: text
    mode: rst
    End:
    vim: fileencoding=utf-8 filetype=rst :
