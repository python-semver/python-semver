.. _sec.replace.parts:

Replacing Parts of a Version
============================

If you want to replace different parts of a version, but leave other parts
unmodified, use the function :func:`replace <semver.version.Version.replace>`:

* From a :class:`Version <semver.version.Version>` instance::

   >>> version = semver.Version.parse("1.4.5-pre.1+build.6")
   >>> version.replace(major=2, minor=2)
   Version(major=2, minor=2, patch=5, prerelease='pre.1', build='build.6')

* From a version string::

   >>> semver.replace("1.4.5-pre.1+build.6", major=2)
   '2.4.5-pre.1+build.6'

If you pass invalid keys you get an exception::

   >>> semver.replace("1.2.3", invalidkey=2)
   Traceback (most recent call last):
   ...
   TypeError: replace() got 1 unexpected keyword argument(s): invalidkey
   >>> version = semver.Version.parse("1.4.5-pre.1+build.6")
   >>> version.replace(invalidkey=2)
   Traceback (most recent call last):
   ...
   TypeError: replace() got 1 unexpected keyword argument(s): invalidkey
