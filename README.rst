.. warning::

   This is a development version. Do **NOT** use it
   in production before the final 3.0.0 is released.

Quickstart
==========

.. teaser-begin

A Python module for `semantic versioning`_. Simplifies comparing versions.

|build-status| |python-support| |downloads| |license| |docs| |black|

.. teaser-end

.. note::

   This project works for Python 3.6 and greater only. If you are
   looking for a compatible version for Python 2, use the
   maintenance branch |MAINT|_.

   The last version of semver which supports Python 2.7 to 3.5 will be
   2.x.y However, keep in mind, the major 2 release is frozen: no new
   features nor backports will be integrated.

   We recommend to upgrade your workflow to Python 3.x to gain support,
   bugfixes, and new features.

.. |MAINT| replace:: ``maint/v2``
.. _MAINT: https://github.com/python-semver/python-semver/tree/maint/v2


The module follows the ``MAJOR.MINOR.PATCH`` style:

* ``MAJOR`` version when you make incompatible API changes,
* ``MINOR`` version when you add functionality in a backwards compatible manner, and
* ``PATCH`` version when you make backwards compatible bug fixes.

Additional labels for pre-release and build metadata are supported.

To import this library, use:

.. code-block:: python

    >>> import semver

Working with the library is quite straightforward. To turn a version string into the
different parts, use the ``semver.Version.parse`` function:

.. code-block:: python

    >>> ver = semver.Version.parse('1.2.3-pre.2+build.4')
    >>> ver.major
    1
    >>> ver.minor
    2
    >>> ver.patch
    3
    >>> ver.prerelease
    'pre.2'
    >>> ver.build
    'build.4'

To raise parts of a version, there are a couple of functions available for
you. The function ``semver.Version.bump_major`` leaves the original object untouched, but
returns a new ``semver.Version`` instance with the raised major part:

.. code-block:: python

    >>> ver = semver.Version.parse("3.4.5")
    >>> ver.bump_major()
    Version(major=4, minor=0, patch=0, prerelease=None, build=None)

It is allowed to concatenate different "bump functions":

.. code-block:: python

    >>> ver.bump_major().bump_minor()
    Version(major=4, minor=1, patch=0, prerelease=None, build=None)

To compare two versions, semver provides the ``semver.compare`` function.
The return value indicates the relationship between the first and second
version:

.. code-block:: python

    >>> semver.compare("1.0.0", "2.0.0")
    -1
    >>> semver.compare("2.0.0", "1.0.0")
    1
    >>> semver.compare("2.0.0", "2.0.0")
    0


There are other functions to discover. Read on!


.. |latest-version| image:: https://img.shields.io/pypi/v/semver.svg
   :alt: Latest version on PyPI
   :target: https://pypi.org/project/semver
.. |build-status| image:: https://travis-ci.com/python-semver/python-semver.svg?branch=master
   :alt: Build status
   :target: https://travis-ci.com/python-semver/python-semver
.. |python-support| image:: https://img.shields.io/pypi/pyversions/semver.svg
   :target: https://pypi.org/project/semver
   :alt: Python versions
.. |downloads| image:: https://img.shields.io/pypi/dm/semver.svg
   :alt: Monthly downloads from PyPI
   :target: https://pypi.org/project/semver
.. |license| image:: https://img.shields.io/pypi/l/semver.svg
   :alt: Software license
   :target: https://github.com/python-semver/python-semver/blob/master/LICENSE.txt
.. |docs| image:: https://readthedocs.org/projects/python-semver/badge/?version=latest
   :target: http://python-semver.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. _semantic versioning: http://semver.org/
.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Black Formatter
