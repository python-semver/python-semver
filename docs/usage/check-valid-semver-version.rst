Checking for a Valid Semver Version
===================================

If you need to check a string if it is a valid semver version, use the
classmethod :func:`Version.isvalid <semver.version.Version.isvalid>`:

.. code-block:: python

    >>> Version.is_valid("1.0.0")
    True
    >>> Version.is_valid("invalid")
    False
