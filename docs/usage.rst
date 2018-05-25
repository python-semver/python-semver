Usage
-----

This module provides just couple of functions, main of which are:

.. code-block:: python

    >>> import semver
    >>> semver.compare("1.0.0", "2.0.0")
    -1
    >>> semver.compare("2.0.0", "1.0.0")
    1
    >>> semver.compare("2.0.0", "2.0.0")
    0
    >>> semver.match("2.0.0", ">=1.0.0")
    True
    >>> semver.match("1.0.0", ">1.0.0")
    False
    >>> semver.format_version(3, 4, 5, 'pre.2', 'build.4')
    '3.4.5-pre.2+build.4'
    >>> version_parts = semver.parse("3.4.5-pre.2+build.4")
    >>> version_parts == {
    ...     'major': 3, 'minor': 4, 'patch': 5,
    ...     'prerelease': 'pre.2', 'build': 'build.4'}
    True
    >>> version_info = semver.parse_version_info("3.4.5-pre.2+build.4")
    >>> # or using static method parse
    >>> from semver import VersionInfo
    >>> version_info = VersionInfo.parse("3.4.5-pre.2+build.4")
    >>> version_info
    VersionInfo(major=3, minor=4, patch=5, prerelease='pre.2', build='build.4')
    >>> version_info.major
    3
    >>> version_info > (1, 0)
    True
    >>> version_info < (3, 5)
    True
    >>> semver.bump_major("3.4.5")
    '4.0.0'
    >>> semver.bump_minor("3.4.5")
    '3.5.0'
    >>> semver.bump_patch("3.4.5")
    '3.4.6'
    >>> semver.max_ver("1.0.0", "2.0.0")
    '2.0.0'
    >>> semver.min_ver("1.0.0", "2.0.0")
    '1.0.0'
