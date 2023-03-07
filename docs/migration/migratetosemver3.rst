.. _semver2-to-3:


Migrating from semver2 to semver3
=================================

This section describes the visible differences for
users and how your code stays compatible for semver3.
Some changes are backward incompatible.

Although the development team tries to make the transition
to semver3 as smooth as possible, at some point change
is inevitable.

For a more detailed overview of all the changes, refer
to our :ref:`change-log`.


Use :class:`Version` instead of :class:`VersionInfo`
----------------------------------------------------

The :class:`VersionInfo` has been renamed to :class:`Version`
to have a more succinct name.
An alias has been created to preserve compatibility but
using the old name has been deprecated.

If you still need the old version, use this line:

.. code-block:: python

   from semver.version import Version as VersionInfo


Use :class:`Version` instead of :meth:`Version.parse`
-----------------------------------------------------

The :class:`~semver.version.Version` class supports now different variants
how a version can be called (see section :ref:`sec_creating_version`
for more details).

It's important to know that you do not need to use
:meth:`Version.parse <semver.version.Version.parse>` anymore. You
can pass a string directly to :class:`~semver.Version`.


Use :mod:`semver.cli` instead of :mod:`semver`
----------------------------------------------

All functions related to CLI parsing are moved to :mod:`semver.cli`.
If you need such functions, like :func:`semver.cmd_bump <semver.cli.cmd_bump>`,
import it from :mod:`semver.cli` in the future:

.. code-block:: python

   from semver.cli import cmd_bump


Use semver.Version.is_valid instead of semver.Version.isvalid
-------------------------------------------------------------

The pull request :pr:`284` introduced the method :meth:`Version.is_compatible <semver.Version.is_compatible>`. To keep consistency, the development team
decided to rename the :meth:`isvalid <semver.Version.isvalid>` to :meth:`is_valid <semver.Version.is_valid>`.
