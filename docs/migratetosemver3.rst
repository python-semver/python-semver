.. _semver2-to-3:

Migrating from semver2 to semver3
=================================

This chapter describes the visible differences for
the users and how your code stays compatible for semver3.


Use Version instead of VersionInfo
----------------------------------

The :class:`VersionInfo` has been renamed to :class:`Version`.
An alias has been created to preserve compatibility but the
use of the old name has been deprecated.

