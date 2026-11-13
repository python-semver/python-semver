Determining Version Equality
============================

.. meta::
   :description lang=en:
      Determining verison equality

Version equality means for semver, that major, minor, patch, and prerelease
parts are equal in both versions you compare. The build part is ignored.
For example:

.. code-block:: pycon

    >>> v = Version.parse("1.2.3-rc4+1e4664d")
    >>> v == "1.2.3-rc4+dedbeef"
    True

In semver 3, equality comparisons between a :class:`~semver.version.Version` and
a string, bytes, tuple, or list issue a :exc:`DeprecationWarning`. This
cross-type equality will be removed in semver 4. Convert strings with
:meth:`Version.parse
<semver.version.Version.parse>` and tuples with ``Version(*parts)`` instead.

To suppress only this warning, add a matching filter during application startup.
The message pattern identifies this semver warning; other
:exc:`DeprecationWarning` messages remain visible. A module filter is not
reliable here because the warning is reported at the comparison's call site:

.. code-block:: python

   import warnings

   warnings.filterwarnings(
      "ignore",
      message=r"Equality comparisons between Version and strings, tuples or lists.*",
      category=DeprecationWarning,
   )

.. warning::

   Keep dictionary keys and set elements to one type. Although :class:`~semver.version.Version`
   remains hashable in semver 3, a :class:`~semver.version.Version` can compare equal to a string,
   bytes, tuple, or list with a different hash, so mixing these types as keys or elements can
   produce failed lookups. Convert values to :class:`~semver.version.Version`
   objects before using them as keys.

This also applies when a :class:`~semver.version.Version` is a member of a set, or a
dictionary key:

.. code-block:: pycon

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
