##########
Change Log
##########


All notable changes to this code base will be documented in this file,
in every released version.


Version 2.9.0 (WIP)
===================
:Released: 20yy-mm-dd
:Maintainer: Sébastien Celles <s.celles@gmail.com>

Features
--------

* :gh:`85` (:pr:`147`, :pr:`154`): Improved contribution section
* :gh:`104` (:pr:`125`): Added iterator to :func:`semver.VersionInfo`
* :gh:`112`, :gh:`113`: Added Python 3.7 support
* :pr:`120`: Improved test_immutable function with properties
* :pr:`125`: Created :file:`setup.cfg` for pytest and tox
* :gh:`126` (:pr:`127`): Added target for documentation in :file:`tox.ini`
* :gh:`142` (:pr:`143`): Improved usage section
* :gh:`145` (:pr:`146`): Added posargs in :file:`tox.ini`
* :pr:`157`: Introduce :file:`conftest.py` to improve doctests

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

* :gh:`111` (:pr:`110`): Droped Python 3.3
* :gh:`148` (:pr:`149`): Removed and replaced ``python setup.py test``


Version 2.8.2
=============
:Released: 2019-05-19
:Maintainer: Sébastien Celles <s.celles@gmail.com>

Skipped, not released.


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


Version 2.7.9
=============

:Released: 2017-09-23
:Maintainer: Kostiantyn Rybnikov <k-bx@k-bx.com>


Additions
---------

* :gh:`65` (:pr:`66`): Added :func:`semver.finalize_version` function.


Version 2.7.8
=============

:Released: 2017-08-25
:Maintainer: Kostiantyn Rybnikov <k-bx@k-bx.com>

* :gh:`62`: Support custom default names for pre and build


Version 2.7.7
=============

:Released: 2017-05-25
:Maintainer: Kostiantyn Rybnikov <k-bx@k-bx.com>

* :gh:`54` (:pr:`55`): Added comparision between VersionInfo objects
* :pr:`56`: Added support for Python 3.6


Version 2.7.2
=============

:Released: 2016-11-08
:Maintainer: Kostiantyn Rybnikov <k-bx@k-bx.com>

Additions
---------

* Added :func:`semver.parse_version_info` to parse a version string to a
  version info tuple.

Bug Fixes
---------

* :gh:`37`: Removed trailing zeros from prelease doesn't allow to
  parse 0 pre-release version

* Refine parsing to conform more strictly to SemVer 2.0.0.

  SemVer 2.0.0 specification §9 forbids leading zero on identifiers in
  the prerelease version.


Version 2.6.0
=============

:Released: 2016-06-08
:Maintainer: Kostiantyn Rybnikov <k-bx@k-bx.com>

Removals
--------

* Remove comparison of build component.

  SemVer 2.0.0 specification recommends that build component is
  ignored in comparisons.


Version 2.5.0
=============

:Released: 2016-05-25
:Maintainer: Kostiantyn Rybnikov <k-bx@k-bx.com>

Additions
---------

* Support matching 'not equal' with “!=”.

Changes
-------

* Made separate builds for tests on Travis CI.


Version 2.4.2
=============

:Released: 2016-05-16
:Maintainer: Kostiantyn Rybnikov <k-bx@k-bx.com>

Changes
-------

* Migrated README document to reStructuredText format.

* Used Setuptools for distribution management.

* Migrated test cases to Py.test.

* Added configuration for Tox test runner.


Version 2.4.1
=============

:Released: 2016-03-04
:Maintainer: Kostiantyn Rybnikov <k-bx@k-bx.com>

Additions
---------

* :gh:`23`: Compared build component of a version.


Version 2.4.0
=============

:Released: 2016-02-12
:Maintainer: Kostiantyn Rybnikov <k-bx@k-bx.com>

Bug Fixes
---------

* :gh:`21`: Compared alphanumeric components correctly.


Version 2.3.1
=============

:Released: 2016-01-30
:Maintainer: Kostiantyn Rybnikov <k-bx@k-bx.com>

Additions
---------

* Declared granted license name in distribution metadata.


Version 2.3.0
=============

:Released: 2016-01-29
:Maintainer: Kostiantyn Rybnikov <k-bx@k-bx.com>

Additions
---------

* Added functions to increment prerelease and build components in a
  version.


Version 2.2.1
=============

:Released: 2015-08-04
:Maintainer: Kostiantyn Rybnikov <k-bx@k-bx.com>

Bug Fixes
---------

* Corrected comparison when any component includes zero.


Version 2.2.0
=============

:Released: 2015-06-21
:Maintainer: Kostiantyn Rybnikov <k-bx@k-bx.com>

Additions
---------

* Add functions to determined minimum and maximum version.

* Add code examples for recently-added functions.


Version 2.1.2
=============

:Released: 2015-05-23
:Maintainer: Kostiantyn Rybnikov <k-bx@k-bx.com>

Bug Fixes
---------

* Restored current README document to distribution manifest.


Version 2.1.1
=============

:Released: 2015-05-23
:Maintainer: Kostiantyn Rybnikov <k-bx@k-bx.com>

Bug Fixes
---------

* Removed absent document from distribution manifest.


Version 2.1.0
=============

:Released: 2015-05-22
:Maintainer: Kostiantyn Rybnikov <k-bx@k-bx.com>

Additions
---------

* Documented installation instructions.

* Documented project home page.

* Added function to format a version string from components.

* Added functions to increment specific components in a version.

Changes
-------

* Migrated README document to Markdown format.

Bug Fixes
---------

* Corrected code examples in README document.


Version 2.0.2
=============

:Released: 2015-04-14
:Maintainer: Konstantine Rybnikov <k-bx@k-bx.com>

Additions
---------

* Added configuration for Travis continuous integration.

* Explicitly declared supported Python versions.


Version 2.0.1
=============

:Released: 2014-09-24
:Maintainer: Konstantine Rybnikov <k-bx@k-bx.com>

Bug Fixes
---------

* :gh:`9`: Fixed comparison of equal version strings.


Version 2.0.0
=============

:Released: 2014-05-24
:Maintainer: Konstantine Rybnikov <k-bx@k-bx.com>

Additions
---------

* Grant license in this code base under BSD 3-clause license terms.

Changes
-------

* Update parser to SemVer standard 2.0.0.

* Ignore build component for comparison.


Version 0.0.2
=============

:Released: 2012-05-10
:Maintainer: Konstantine Rybnikov <k-bx@k-bx.com>

Changes
-------

* Use standard library Distutils for distribution management.


Version 0.0.1
=============

:Released: 2012-04-28
:Maintainer: Konstantine Rybnikov <kost-bebix@yandex.ru>

* Initial release.


..
    Local variables:
    coding: utf-8
    mode: text
    mode: rst
    End:
    vim: fileencoding=utf-8 filetype=rst :
