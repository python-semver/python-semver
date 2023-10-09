.. _semver2-to-3:

Migrating from semver2 to semver3
=================================

.. meta::
   :description lang=en:
      Migrating from semver2 to semver3

This section describes the visible differences for
users and how your code stays compatible for semver3.
Some changes are backward incompatible.

Although the development team tries to make the transition
to semver3 as smooth as possible, at some point change
is inevitable.

For a more detailed overview of all the changes, refer
to our :ref:`change-log`.


Use Version instead of VersionInfo
----------------------------------

The :class:`~semver.version.VersionInfo` has been renamed to
:class:`~semver.version.Version` to have a more succinct name.
An alias has been created to preserve compatibility but
using the old name has been deprecated and will be removed
in future versions.

If you still need the old version, use this line:

.. code-block:: python

   from semver.version import Version as VersionInfo



Use semver.cli instead of semver
--------------------------------

All functions related to CLI parsing are moved to :mod:`semver.cli`.
If you need such functions, like :meth:`~semver.cli.cmd_bump`,
import it from :mod:`semver.cli` in the future:

.. code-block:: python

   from semver.cli import cmd_bump


Use semver.Version.is_valid instead of semver.Version.isvalid
-------------------------------------------------------------

The pull request :pr:`284` introduced the method :meth:`~semver.version.Version.is_compatible`. To keep consistency, the development team
decided to rename the :meth:`~semver.Version.isvalid` to :meth:`~semver.Version.is_valid`.
