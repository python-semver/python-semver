.. _sec.convert.versions:

Converting a Version instance into Different Types
==================================================

Sometimes it is needed to convert a :class:`Version <semver.version.Version>` instance into
a different type. For example, for displaying or to access all parts.

It is possible to convert a :class:`Version <semver.version.Version>` instance:

* Into a string with the builtin function :func:`str`::

    >>> str(Version.parse("3.4.5-pre.2+build.4"))
    '3.4.5-pre.2+build.4'

* Into a dictionary with :func:`to_dict <semver.version.Version.to_dict>`::

    >>> v = Version(major=3, minor=4, patch=5)
    >>> v.to_dict()
    OrderedDict([('major', 3), ('minor', 4), ('patch', 5), ('prerelease', None), ('build', None)])

* Into a tuple with :func:`to_tuple <semver.version.Version.to_tuple>`::

    >>> v = Version(major=5, minor=4, patch=2)
    >>> v.to_tuple()
    (5, 4, 2, None, None)
