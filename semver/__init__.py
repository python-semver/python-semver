"""
Python helper for Semantic Versioning (http://semver.org/)
"""
from semver.core import (
    VersionInfo, bump_major, bump_minor, bump_patch, bump_prerelease,
    bump_build, compare, format_version, match, max_ver, min_ver, parse
)

__version__ = '2.7.8'
__author__ = 'Kostiantyn Rybnikov'
__author_email__ = 'k-bx@k-bx.com'
