.. _api:

API Reference
=============

.. meta::
   :description lang=en:
      API reference about Python semver

.. currentmodule:: semver


Metadata :mod:`semver.__about__`
--------------------------------

.. automodule:: semver.__about__


Deprecated Functions in :mod:`semver._deprecated`
-------------------------------------------------

.. automodule:: semver._deprecated

.. autofunction:: semver._deprecated.compare

.. autofunction:: semver._deprecated.bump_build

.. autofunction:: semver._deprecated.bump_major

.. autofunction:: semver._deprecated.bump_minor

.. autofunction:: semver._deprecated.bump_patch

.. autofunction:: semver._deprecated.bump_prerelease

.. autofunction:: semver._deprecated.deprecated

.. autofunction:: semver._deprecated.finalize_version

.. autofunction:: semver._deprecated.format_version

.. autofunction:: semver._deprecated.match

.. autofunction:: semver._deprecated.max_ver

.. autofunction:: semver._deprecated.min_ver

.. autofunction:: semver._deprecated.parse

.. autofunction:: semver._deprecated.parse_version_info

.. autofunction:: semver._deprecated.replace



CLI Parsing :mod:`semver.cli`
-----------------------------

.. automodule:: semver.cli

.. autofunction:: semver.cli.cmd_bump

.. autofunction:: semver.cli.cmd_check

.. autofunction:: semver.cli.cmd_compare

.. autofunction:: semver.cli.createparser

.. autofunction:: semver.cli.main

.. autofunction:: semver.cli.process


Entry point :mod:`semver.__main__`
----------------------------------

.. automodule:: semver.__main__



Version Handling :mod:`semver.version`
--------------------------------------

.. automodule:: semver.version

.. autoclass:: semver.version.VersionInfo

.. autoclass:: semver.version.Version
   :members:
   :special-members: __iter__, __eq__, __ne__, __lt__, __le__, __gt__, __ge__, __getitem__, __hash__, __repr__, __str__
