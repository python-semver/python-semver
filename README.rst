=================================================
 Semver -- python module for semantic versioning 
=================================================

Simple module for comparing versions as noted at
`semver.org <http://semver.org/>`_.

This module provides just couple of functions, main of which are:

..

    >>> import semver
    >>> semver.compare("1.0.0", "2.0.0")
    1
    >>> semver.compare("2.0.0", "1.0.0")
    -1
    >>> semver.compare("2.0.0", "2.0.0")
    0
    >>> semver.match("2.0.0", ">=1.0.0")
    True
    >>> semver.match("1.0.0", ">1.0.0")
    False
