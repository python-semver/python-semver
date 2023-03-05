.. _sec_replace_deprecated_functions:

Replacing Deprecated Functions
==============================

.. versionchanged:: 2.10.0
   The development team of semver has decided to deprecate certain functions on
   the module level. The preferred way of using semver is through the
   :class:`~semver.version.Version` class.

The deprecated functions can still be used in version 2.10.0 and above. In version 3 of
semver, the deprecated functions will be removed.

The following list shows the deprecated functions and how you can replace
them with code which is compatible for future versions:


* :func:`semver.bump_major`, :func:`semver.bump_minor`, :func:`semver.bump_patch`, :func:`semver.bump_prerelease`, :func:`semver.bump_build`

  Replace them with the respective methods of the :class:`~semver.version.Version`
  class.
  For example, the function :func:`semver.bump_major` is replaced by
  :meth:`~semver.version.Version.bump_major` and calling the ``str(versionobject)``:

  .. code-block:: python

     >>> s1 = semver.bump_major("3.4.5")
     >>> s2 = str(Version.parse("3.4.5").bump_major())
     >>> s1 == s2
     True

  Likewise with the other module level functions.

* :func:`semver.Version.isvalid`

   Replace it with :meth:`semver.version.Version.is_valid`:


* :func:`semver.finalize_version`

  Replace it with :func:`semver.version.Version.finalize_version`:

  .. code-block:: python

     >>> s1 = semver.finalize_version('1.2.3-rc.5')
     >>> s2 = str(semver.Version.parse('1.2.3-rc.5').finalize_version())
     >>> s1 == s2
     True

* :func:`semver.format_version`

  Replace it with ``str(versionobject)``:

  .. code-block:: python

     >>> s1 = semver.format_version(5, 4, 3, 'pre.2', 'build.1')
     >>> s2 = str(Version(5, 4, 3, 'pre.2', 'build.1'))
     >>> s1 == s2
     True

* :func:`semver.max_ver`

  Replace it with ``max(version1, version2, ...)`` or ``max([version1, version2, ...])`` and a ``key``:

  .. code-block:: python

     >>> s1 = semver.max_ver("1.2.3", "1.2.4")
     >>> s2 = max("1.2.3", "1.2.4", key=Version.parse)
     >>> s1 == s2
     True

* :func:`semver.min_ver`

  Replace it with ``min(version1, version2, ...)`` or ``min([version1, version2, ...])``:

  .. code-block:: python

     >>> s1 = semver.min_ver("1.2.3", "1.2.4")
     >>> s2 = min("1.2.3", "1.2.4", key=Version.parse)
     >>> s1 == s2
     True

* :func:`semver.parse`

  Replace it with :meth:`semver.version.Version.parse` and call
  :meth:`semver.version.Version.to_dict`:

  .. code-block:: python

     >>> v1 = semver.parse("1.2.3")
     >>> v2 = Version.parse("1.2.3").to_dict()
     >>> v1 == v2
     True

* :func:`semver.parse_version_info`

  Replace it with :meth:`semver.version.Version.parse`:

  .. code-block:: python

     >>> v1 = semver.parse_version_info("3.4.5")
     >>> v2 = Version.parse("3.4.5")
     >>> v1 == v2
     True

* :func:`semver.replace`

  Replace it with :meth:`semver.version.Version.replace`:

  .. code-block:: python

     >>> s1 = semver.replace("1.2.3", major=2, patch=10)
     >>> s2 = str(Version.parse('1.2.3').replace(major=2, patch=10))
     >>> s1 == s2
     True
