.. _sec.properties.parts:

Accessing Parts of a Version Through Names
==========================================

.. meta::
   :description lang=en:
      Accessing parts of a version through names

The :class:`~semver.version.Version` class contains attributes to access the different
parts of a version:

.. code-block:: python

    >>> v = Version.parse("3.4.5-pre.2+build.4")
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

However, the attributes are read-only. You cannot change any of the above attributes.
If you do, you get an :py:exc:`python:AttributeError`::

    >>> v.minor = 5
    Traceback (most recent call last):
    ...
    AttributeError: attribute 'minor' is readonly

If you need to replace different parts of a version, refer to section :ref:`sec.replace.parts`.

In case you need the different parts of a version stepwise, iterate over the :class:`~semver.version.Version` instance::

    >>> for item in Version.parse("3.4.5-pre.2+build.4"):
    ...     print(item)
    3
    4
    5
    pre.2
    build.4
    >>> list(Version.parse("3.4.5-pre.2+build.4"))
    [3, 4, 5, 'pre.2', 'build.4']
