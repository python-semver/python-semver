Creating a Version
==================

.. meta::
   :description lang=en:
      Creating a version using different methods

.. versionchanged:: 3.0.0

  The former :class:`~semver.version.VersionInfo` class
  has been renamed to :class:`~semver.version.Version`.

The preferred way to create a new version is with the class
:class:`~semver.version.Version`.

.. note::

   In the previous major release semver 2 it was possible to
   create a version with module level functions.
   However, module level functions are marked as *deprecated*
   since version 2.x.y now.
   These functions will be removed.
   For details, see the sections :ref:`sec_replace_deprecated_functions`
   and :ref:`sec_display_deprecation_warnings`.

A :class:`~semver.version.Version` instance can be created in different ways:

* From a Unicode string::

    >>> from semver.version import Version
    >>> Version.parse("3.4.5-pre.2+build.4")
    Version(major=3, minor=4, patch=5, prerelease='pre.2', build='build.4')
    >>> Version.parse(u"5.3.1")
    Version(major=5, minor=3, patch=1, prerelease=None, build=None)

* From a byte string::

    >>> Version.parse(b"2.3.4")
    Version(major=2, minor=3, patch=4, prerelease=None, build=None)

* From individual parts by a dictionary::

    >>> d = {'major': 3, 'minor': 4, 'patch': 5,  'prerelease': 'pre.2', 'build': 'build.4'}
    >>> Version(**d)
    Version(major=3, minor=4, patch=5, prerelease='pre.2', build='build.4')

  Keep in mind, the ``major``, ``minor``, ``patch`` parts has to
  be positive integers or strings, otherwise a :py:exc:`python:ValueError` is raised:

      >>> d = {'major': -3, 'minor': 4, 'patch': 5,  'prerelease': 'pre.2', 'build': 'build.4'}
      >>> Version(**d)
      Traceback (most recent call last):
      ...
      ValueError: 'major' is negative. A version can only be positive.

  As a minimum requirement, your dictionary needs at least the ``major``
  key, others can be omitted. You get a :py:exc:`python:TypeError` if your
  dictionary contains invalid keys.
  Only the keys ``major``, ``minor``, ``patch``, ``prerelease``, and ``build``
  are allowed.

* From a tuple::

    >>> t = (3, 5, 6)
    >>> Version(*t)
    Version(major=3, minor=5, patch=6, prerelease=None, build=None)

  You can pass either an integer or a string for ``major``, ``minor``, or
  ``patch``::

    >>> Version("3", "5", 6)
    Version(major=3, minor=5, patch=6, prerelease=None, build=None)

The old, deprecated module level functions are still available but
using them are discoraged. They are available to convert old code
to semver3.

If you need them, they return different builtin objects (string and dictionary).
Keep in mind, once you have converted a version into a string or dictionary,
it's an ordinary builtin object. It's not a special version object like
the :class:`~semver.version.Version` class anymore.

Depending on your use case, the following methods are available:

* From individual version parts into a string

  In some cases you only need a string from your version data::

    >>> semver.format_version(3, 4, 5, 'pre.2', 'build.4')
    '3.4.5-pre.2+build.4'

* From a string into a dictionary

  To access individual parts, you can use the function :func:`~semver._deprecated.parse`::

    >>> semver.parse("3.4.5-pre.2+build.4")
    {'major': 3, 'minor': 4, 'patch': 5, 'prerelease': 'pre.2', 'build': 'build.4'}

  If you pass an invalid version string you will get a :py:exc:`python:ValueError`::

    >>> semver.parse("1.2")
    Traceback (most recent call last):
    ...
    ValueError: 1.2 is not valid SemVer string
