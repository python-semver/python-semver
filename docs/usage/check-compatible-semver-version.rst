Checking for a Compatible Semver Version
========================================

.. meta::
   :description lang=en:
      Check for a compatible semver version

To check if a *change* from a semver version ``a`` to a semver
version ``b`` is *compatible* according to semver rule, use the method
:meth:`~semver.version.Version.is_compatible`.

The expression ``a.is_compatible(b) is True`` if one of the following
statements is true:

* both versions are equal, or
* both majors are equal and higher than 0. The same applies for both
  minor parts. Both pre-releases are equal, or
* both majors are equal and higher than 0. The minor of ``b``'s
  minor version is higher then ``a``'s. Both pre-releases are equal.

In all other cases, the result is false.

Keep in mind, the method *does not* check patches!


* Two different majors:

  .. code-block:: python

      >>> a = Version(1, 1, 1)
      >>> b = Version(2, 0, 0)
      >>> a.is_compatible(b)
      False
      >>> b.is_compatible(a)
      False

* Two different minors:

  .. code-block:: python

      >>> a = Version(1, 1, 0) 
      >>> b = Version(1, 0, 0)
      >>> a.is_compatible(b)
      False
      >>> b.is_compatible(a)
      True

* The same two majors and minors:

  .. code-block:: python

      >>> a = Version(1, 1, 1) 
      >>> b = Version(1, 1, 0) 
      >>> a.is_compatible(b)
      True
      >>> b.is_compatible(a)
      True

* Release and pre-release:

  .. code-block:: python

      >>> a = Version(1, 1, 1)
      >>> b = Version(1, 0, 0,'rc1')
      >>> a.is_compatible(b)
      False
      >>> b.is_compatible(a)
      False

* Different pre-releases:

  .. code-block:: python

      >>> a = Version(1, 0, 0, 'rc1')
      >>> b = Version(1, 0, 0, 'rc2')
      >>> a.is_compatible(b)
      False
      >>> b.is_compatible(a)
      False

* Identical pre-releases:

  .. code-block:: python

      >>> a = Version(1, 0, 0,'rc1')
      >>> b = Version(1, 0, 0,'rc1')
      >>> a.is_compatible(b)
      True

* All major zero versions are incompatible with anything but itself:

  .. code-block:: python

      >>> Version(0, 1, 0).is_compatible(Version(0, 1, 1))
      False

      # Only identical versions are compatible for major zero versions:
      >>> Version(0, 1, 0).is_compatible(Version(0, 1, 0))
      True
