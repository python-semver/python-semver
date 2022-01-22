Raising Parts of a Version
==========================

The ``semver`` module contains the following functions to raise parts of
a version:

* :func:`Version.bump_major <semver.version.Version.bump_major>`: raises the major part and set all other parts to
  zero. Set ``prerelease`` and ``build`` to ``None``.
* :func:`Version.bump_minor <semver.version.Version.bump_minor>`: raises the minor part and sets ``patch`` to zero.
  Set ``prerelease`` and ``build`` to ``None``.
* :func:`Version.bump_patch <semver.version.Version.bump_patch>`: raises the patch part. Set ``prerelease`` and
  ``build`` to ``None``.
* :func:`Version.bump_prerelease <semver.version.Version.bump_prerelease>`: raises the prerelease part and set
  ``build`` to ``None``.
* :func:`Version.bump_build <semver.version.Version.bump_build>`: raises the build part.

.. code-block:: python

    >>> str(Version.parse("3.4.5-pre.2+build.4").bump_major())
    '4.0.0'
    >>> str(Version.parse("3.4.5-pre.2+build.4").bump_minor())
    '3.5.0'
    >>> str(Version.parse("3.4.5-pre.2+build.4").bump_patch())
    '3.4.6'
    >>> str(Version.parse("3.4.5-pre.2+build.4").bump_prerelease())
    '3.4.5-pre.3'
    >>> str(Version.parse("3.4.5-pre.2+build.4").bump_build())
    '3.4.5-pre.2+build.5'

Likewise the module level functions :func:`semver.bump_major`.
