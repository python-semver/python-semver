Raising Parts of a Version
==========================

.. note::

   Keep in mind, by default, "raising" the pre-release for a version without an existing
   prerelease part, only will make your complete version *lower* than before.

   For example, having version ``1.0.0`` and raising the pre-release
   will lead to ``1.0.0-rc.1``, but ``1.0.0-rc.1`` is smaller than ``1.0.0``.

   To avoid this, set `bump_when_empty=True` in the
   :meth:`~semver.version.Version.bump_prerelease` method, or by using the
   method :meth:`~semver.version.Version.next_version`
   in section :ref:`increase-parts-of-a-version`.


The ``semver`` module contains the following functions to raise parts of
a version:

* :meth:`~semver.version.Version.bump_major`: raises the major part and set all other parts to
  zero. Set ``prerelease`` and ``build`` to ``None``.
* :meth:`~semver.version.Version.bump_minor`: raises the minor part and sets ``patch`` to zero.
  Set ``prerelease`` and ``build`` to ``None``.
* :meth:`~semver.version.Version.bump_patch`: raises the patch part. Set ``prerelease`` and
  ``build`` to ``None``.
* :meth:`~semver.version.Version.bump_prerelease`: raises the prerelease part and set
  ``build`` to ``None``.
* :meth:`~semver.version.Version.bump_build`: raises the build part.


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

For the methods :meth:`~semver.version.Version.bump_prerelease`
and :meth:`~semver.version.Version.bump_build` it's possible to pass an empty string or ``None``.
However, it gives different results:

.. code-block:: python

    >>> str(Version.parse("3.4.5").bump_prerelease(''))
    '3.4.5-1'
    >>> str(Version.parse("3.4.5").bump_prerelease(None))
    '3.4.5-rc.1'

An empty string removes any prefix whereas ``None`` is the same as calling
the method without any argument.

If you already have a prerelease, the argument for the method
is not taken into account:

.. code-block:: python

    >>> str(Version.parse("3.4.5-rc.1").bump_prerelease(None))
    '3.4.5-rc.2'
    >>> str(Version.parse("3.4.5-rc.1").bump_prerelease(''))
    '3.4.5-rc.2'

To ensure correct ordering, we append `.0` to the last prerelease identifier
if it's not numeric. This prevents cases where `rc9` would incorrectly sort
lower than `rc10` (non-numeric identifiers are compared alphabetically):

.. code-block:: python

    >>> str(Version.parse("3.4.5-rc9").bump_prerelease())
    '3.4.5-rc9.0'
    >>> str(Version.parse("3.4.5-rc.9").bump_prerelease())
    '3.4.5-rc.10'

