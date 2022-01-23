.. _sec_max_min:

Getting Minimum and Maximum of Multiple Versions
================================================

.. versionchanged:: 2.10.2
   The functions :func:`semver.max_ver` and :func:`semver.min_ver` are deprecated in
   favor of their builtin counterparts :func:`max` and :func:`min`.

Since :class:`Version <semver.version.Version>` implements
:func:`__gt__ <semver.version.Version.__gt__>` and
:func:`__lt__ <semver.version.Version.__lt__>`, it can be used with builtins requiring:

.. code-block:: python

    >>> max([Version(0, 1, 0), Version(0, 2, 0), Version(0, 1, 3)])
    Version(major=0, minor=2, patch=0, prerelease=None, build=None)
    >>> min([Version(0, 1, 0), Version(0, 2, 0), Version(0, 1, 3)])
    Version(major=0, minor=1, patch=0, prerelease=None, build=None)

Incidentally, using :func:`map`, you can get the min or max version of any number of versions of the same type
(convertible to :class:`Version <semver.version.Version>`).

For example, here are the maximum and minimum versions of a list of version strings:

.. code-block:: python

    >>> max(['1.1.0', '1.2.0', '2.1.0', '0.5.10', '0.4.99'], key=Version.parse)
    '2.1.0'
    >>> min(['1.1.0', '1.2.0', '2.1.0', '0.5.10', '0.4.99'], key=Version.parse)
    '0.4.99'

And the same can be done with tuples:

.. code-block:: python

    >>> max(map(lambda v: Version(*v), [(1, 1, 0), (1, 2, 0), (2, 1, 0), (0, 5, 10), (0, 4, 99)])).to_tuple()
    (2, 1, 0, None, None)
    >>> min(map(lambda v: Version(*v), [(1, 1, 0), (1, 2, 0), (2, 1, 0), (0, 5, 10), (0, 4, 99)])).to_tuple()
    (0, 4, 99, None, None)

For dictionaries, it is very similar to finding the max version tuple: see :ref:`sec.convert.versions`.

The "old way" with :func:`semver.max_ver` or :func:`semver.min_ver` is still available, but not recommended:

.. code-block:: python

    >>> semver.max_ver("1.0.0", "2.0.0")
    '2.0.0'
    >>> semver.min_ver("1.0.0", "2.0.0")
    '1.0.0'
