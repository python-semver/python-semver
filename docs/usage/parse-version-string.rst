Parsing a Version String
========================

"Parsing" in this context means to identify the different parts in a string.
Use the function :func:`Version.parse <semver.version.Version.parse>`::

    >>> Version.parse("3.4.5-pre.2+build.4")
    Version(major=3, minor=4, patch=5, prerelease='pre.2', build='build.4')
