.. _increase-parts-of-a-version:

Increasing Parts of a Version Taking into Account Prereleases
=============================================================

.. versionadded:: 2.10.0
   Added :meth:`~semver.version.Version.next_version`.

If you want to raise your version and take prereleases into account,
the function :meth:`~semver.version.Version.next_version`
would perhaps a better fit.


.. code-block:: python

    >>> v = Version.parse("3.4.5-pre.2+build.4")
    >>> str(v.next_version(part="prerelease"))
    '3.4.5-pre.3'
    >>> str(Version.parse("3.4.5-pre.2+build.4").next_version(part="patch"))
    '3.4.5'
    >>> str(Version.parse("3.4.5+build.4").next_version(part="patch"))
    '3.4.5'
    >>> str(Version.parse("0.1.4").next_version("prerelease"))
    '0.1.5-rc.1'
