Determining Version Equality
============================

.. meta::
   :description lang=en:
      Determining verison equality

Version equality means for semver, that major, minor, patch, and prerelease
parts are equal in both versions you compare. The build part is ignored.
For example::

    >>> v = Version.parse("1.2.3-rc4+1e4664d")
    >>> v == "1.2.3-rc4+dedbeef"
    True

This also applies when a :class:`Version <semver.version.Version>` is a member of a set, or a
dictionary key::

    >>> d = {}
    >>> v1 = Version.parse("1.2.3-rc4+1e4664d")
    >>> v2 = Version.parse("1.2.3-rc4+dedbeef")
    >>> d[v1] = 1
    >>> d[v2]
    1
    >>> s = set()
    >>> s.add(v1)
    >>> v2 in s
    True

