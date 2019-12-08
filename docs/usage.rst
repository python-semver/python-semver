Using semver
============

The ``semver`` module can store a version in different types:

* as a string.
* as :class:`semver.VersionInfo`, a dedicated class for a version type.
* as a dictionary.

Each type can be converted into the other, if the minimum requirements
are met.


Knowing the Implemented semver.org Version
------------------------------------------

The semver.org is the authorative specification of how semantical versioning is
definied. To know which version of semver.org is implemented in the semver
libary, use the following constant::

   >>> semver.SEMVER_SPEC_VERSION
   '2.0.0'


Creating a Version
------------------

A version can be created in different ways:

* as a complete version string::

    >>> semver.parse_version_info("3.4.5-pre.2+build.4")
    VersionInfo(major=3, minor=4, patch=5, prerelease='pre.2', build='build.4')
    >>> semver.VersionInfo.parse("3.4.5-pre.2+build.4")
    VersionInfo(major=3, minor=4, patch=5, prerelease='pre.2', build='build.4')

* with individual parts::

    >>> semver.format_version(3, 4, 5, 'pre.2', 'build.4')
    '3.4.5-pre.2+build.4'
    >>> semver.VersionInfo(3, 5)
    VersionInfo(major=3, minor=5, patch=0, prerelease=None, build=None)

  You can pass either an integer or a string for ``major``, ``minor``, or
  ``patch``::

    >>> semver.VersionInfo("3", "5")
    VersionInfo(major=3, minor=5, patch=0, prerelease=None, build=None)

  In the simplest form, ``prerelease`` and ``build`` can also be
  integers::

    >>> semver.VersionInfo(1, 2, 3, 4, 5)
    VersionInfo(major=1, minor=2, patch=3, prerelease=4, build=5)

If you pass an invalid version string you will get a ``ValueError``::

    >>> semver.parse("1.2")
    Traceback (most recent call last)
    ...
    ValueError: 1.2 is not valid SemVer string


Parsing a Version String
------------------------

"Parsing" in this context means to identify the different parts in a string.


* With :func:`semver.parse_version_info`::

    >>> semver.parse_version_info("3.4.5-pre.2+build.4")
    VersionInfo(major=3, minor=4, patch=5, prerelease='pre.2', build='build.4')

* With :func:`semver.VersionInfo.parse` (basically the same as
  :func:`semver.parse_version_info`)::

    >>> semver.VersionInfo.parse("3.4.5-pre.2+build.4")
    VersionInfo(major=3, minor=4, patch=5, prerelease='pre.2', build='build.4')

* With :func:`semver.parse`::

    >>> semver.parse("3.4.5-pre.2+build.4")
    {'major': 3, 'minor': 4, 'patch': 5,  'prerelease': 'pre.2', 'build': 'build.4'}


Checking for a Valid Semver Version
-----------------------------------

If you need to check a string if it is a valid semver version, use the
classmethod :func:`semver.VersionInfo.isvalid`:

.. code-block:: python

    >>> VersionInfo.isvalid("1.0.0")
    True
    >>> VersionInfo.isvalid("invalid")
    False


Accessing Parts of a Version
----------------------------

The :class:`semver.VersionInfo` contains attributes to access the different
parts of a version:

.. code-block:: python

    >>> v = VersionInfo.parse("3.4.5-pre.2+build.4")
    >>> v.major
    3
    >>> v.minor
    4
    >>> v.patch
    5
    >>> v.prerelease
    'pre.2'
    >>> v.build
    'build.4'

However, the attributes are read-only. You cannot change an attribute.
If you do, you get an ``AttributeError``::

    >>> v.minor = 5
    Traceback (most recent call last)
    ...
    AttributeError: attribute 'minor' is readonly

In case you need the different parts of a version stepwise, iterate over the :class:`semver.VersionInfo` instance::

    >>> for item in VersionInfo.parse("3.4.5-pre.2+build.4"):
    ...     print(item)
    3
    4
    5
    pre.2
    build.4
    >>> list(VersionInfo.parse("3.4.5-pre.2+build.4"))
    [3, 4, 5, 'pre.2', 'build.4']


Replacing Parts of a Version
----------------------------

If you want to replace different parts of a version, but leave other parts
unmodified, use one of the functions :func:`semver.replace` or
:func:`semver.VersionInfo.replace`:

* From a version string::

   >>> semver.replace("1.4.5-pre.1+build.6", major=2)
   '2.4.5-pre.1+build.6'

* From a :class:`semver.VersionInfo` instance::

   >>> version = semver.VersionInfo.parse("1.4.5-pre.1+build.6")
   >>> version.replace(major=2, minor=2)
   VersionInfo(major=2, minor=2, patch=5, prerelease='pre.1', build='build.6')

If you pass invalid keys you get an exception::

   >>> semver.replace("1.2.3", invalidkey=2)
   Traceback (most recent call last)
   ...
   TypeError: replace() got 1 unexpected keyword argument(s): invalidkey
   >>> version = semver.VersionInfo.parse("1.4.5-pre.1+build.6")
   >>> version.replace(invalidkey=2)
   Traceback (most recent call last)
   ...
   TypeError: replace() got 1 unexpected keyword argument(s): invalidkey


.. _sec.convert.versions:

Converting Different Version Types
----------------------------------

Depending which function you call, you get different types
(as explained in the beginning of this chapter).

* From a string into :class:`semver.VersionInfo`::

    >>> semver.VersionInfo.parse("3.4.5-pre.2+build.4")
    VersionInfo(major=3, minor=4, patch=5, prerelease='pre.2', build='build.4')

* From :class:`semver.VersionInfo` into a string::

    >>> str(semver.VersionInfo.parse("3.4.5-pre.2+build.4"))
    '3.4.5-pre.2+build.4'

* From a dictionary into :class:`semver.VersionInfo`::

    >>> d = {'major': 3, 'minor': 4, 'patch': 5,  'prerelease': 'pre.2', 'build': 'build.4'}
    >>> semver.VersionInfo(**d)
    VersionInfo(major=3, minor=4, patch=5, prerelease='pre.2', build='build.4')

  As a minimum requirement, your dictionary needs at least the ``major``
  key, others can be omitted. You get a ``TypeError`` if your
  dictionary contains invalid keys.
  Only ``major``, ``minor``, ``patch``, ``prerelease``, and ``build``
  are allowed.

* From a tuple into :class:`semver.VersionInfo`::

    >>> t = (3, 5, 6)
    >>> semver.VersionInfo(*t)
    VersionInfo(major=3, minor=5, patch=6, prerelease=None, build=None)

* From a  :class:`semver.VersionInfo` into a dictionary::

    >>> v = semver.VersionInfo(major=3, minor=4, patch=5)
    >>> semver.parse(str(v))
    {'major': 3, 'minor': 4, 'patch': 5, 'prerelease': None, 'build': None}


Parsing Incomplete Versions
---------------------------

If a version is incomplete (some parts are missing) this would lead to an
exception during the parsing process. As such, you cannot get a valid
:class:`semver.VersionInfo` instance.

To avoid such situations, such incomplete version strings can still be parsed
with the :func:`semver.VersionInfo.coerce` function. This function applies
the following rules:

* Tries to detect a "basic" version string (``major.minor.patch``).
* If not enough components can be found, missing components are
  set to zero to obtain a valid semver version.

It expects a version string and returns a tuple. The first item of the tuple
is either a :class:`VersionInfo` instance or ``None`` if the function cannot
extract a version. The second item is the rest of the string:

.. code-block:: python

    >>> semver.VersionInfo.coerce("v1.2")
    (VersionInfo(major=1, minor=2, patch=0, prerelease=None, build=None), '')
    >>> semver.VersionInfo.coerce("v1.2-abc")
    (VersionInfo(major=1, minor=2, patch=0, prerelease=None, build=None), '-abc')
    >>> semver.VersionInfo.coerce("abc")
    (None, 'abc')


Increasing Parts of a Version
-----------------------------

The ``semver`` module contains the following functions to raise parts of
a version:

* :func:`semver.bump_major`: raises the major part and set all other parts to
  zero. Set ``prerelease`` and ``build`` to ``None``.
* :func:`semver.bump_minor`: raises the minor part and sets ``patch`` to zero.
  Set ``prerelease`` and ``build`` to ``None``.
* :func:`semver.bump_patch`: raises the patch part. Set ``prerelease`` and
  ``build`` to ``None``.
* :func:`semver.bump_prerelease`: raises the prerelease part and set
  ``build`` to ``None``.
* :func:`semver.bump_build`: raises the build part.

.. code-block:: python

    >>> semver.bump_major("3.4.5-pre.2+build.4")
    '4.0.0'
    >>> semver.bump_minor("3.4.5-pre.2+build.4")
    '3.5.0'
    >>> semver.bump_patch("3.4.5-pre.2+build.4")
    '3.4.6'
    >>> semver.bump_prerelease("3.4.5-pre.2+build.4")
    '3.4.5-pre.3'
    >>> semver.bump_build("3.4.5-pre.2+build.4")
    '3.4.5-pre.2+build.5'


Comparing Versions
------------------

To compare two versions depends on your type:

* **Two strings**

  Use :func:`semver.compare`::

    >>> semver.compare("1.0.0", "2.0.0")
    -1
    >>> semver.compare("2.0.0", "1.0.0")
    1
    >>> semver.compare("2.0.0", "2.0.0")
    0

  The return value is negative if ``version1 < version2``, zero if
  ``version1 == version2`` and strictly positive if ``version1 > version2``.

* **Two** :class:`semver.VersionInfo` **types**

  Use the specific operator. Currently, the operators ``<``,
  ``<=``, ``>``, ``>=``, ``==``, and ``!=`` are supported::

    >>> v1 = VersionInfo.parse("3.4.5")
    >>> v2 = VersionInfo.parse("3.5.1")
    >>> v1 < v2
    True
    >>> v1 > v2
    False

* **A** :class:`semver.VersionInfo` **type and a** ``tuple``

  Use the operator as with two :class:`semver.VersionInfo` types::

    >>> v = VersionInfo.parse("3.4.5")
    >>> v > (1, 0)
    True
    >>> v < (3, 5)
    True

  The opposite does also work::

    >>> (1, 0) < v
    True
    >>> (3, 5) > v
    True

Other types cannot be compared (like dictionaries, lists etc).

If you need to convert some types into other, refer to :ref:`sec.convert.versions`.



Comparing Versions through an Expression
----------------------------------------

If you need a more fine-grained approach of comparing two versions,
use the :func:`semver.match` function. It expects two arguments:

1. a version string
2. a match expression

Currently, the match expression supports the following operators:

* ``<`` smaller than
* ``>`` greater than
* ``>=`` greater or equal than
* ``<=`` smaller or equal than
* ``==`` equal
* ``!=`` not equal

That gives you the following possibilities to express your condition:

.. code-block:: python

    >>> semver.match("2.0.0", ">=1.0.0")
    True
    >>> semver.match("1.0.0", ">1.0.0")
    False


Getting Minimum and Maximum of two Versions
-------------------------------------------

.. code-block:: python

    >>> semver.max_ver("1.0.0", "2.0.0")
    '2.0.0'
    >>> semver.min_ver("1.0.0", "2.0.0")
    '1.0.0'
