Parsing a Version String
========================

"Parsing" in this context means to identify the different parts in a string.
Use the function :meth:`~semver.version.Version.parse`::

    >>> Version.parse("3.4.5-pre.2+build.4")
    Version(major=3, minor=4, patch=5, prerelease='pre.2', build='build.4')

Set the parameter ``optional_minor_and_patch=True`` to allow optional
minor and patch parts. Optional parts are set to zero. By default (False), the
version string to parse has to follow the semver specification::

    >>> Version.parse("1.2", optional_minor_and_patch=True)
    Version(major=1, minor=2, patch=0, prerelease=None, build=None)
