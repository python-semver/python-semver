Checking for a Valid Semver Version
===================================

.. meta::
   :description lang=en:
      Checking for a valid semver version

If you need to check a string if it is a valid semver version, use the
classmethod :meth:`~semver.version.Version.is_valid`:

.. code-block:: python

    >>> Version.is_valid("1.0.0")
    True
    >>> Version.is_valid("invalid")
    False
