"""
semver package major release 3.

A Python module for semantic versioning. Simplifies comparing versions.
"""

from .__about__ import (SEMVER_SPEC_VERSION, __author__, __author_email__,
                        __description__, __maintainer__, __maintainer_email__,
                        __version__)
from ._deprecated import (bump_build, bump_major, bump_minor, bump_patch,
                          bump_prerelease, cmd_bump, cmd_check, cmd_compare,
                          cmd_nextver, compare, createparser, finalize_version,
                          format_version, main, match, max_ver, min_ver, parse,
                          parse_version_info, process, replace)
from .version import Version, VersionInfo
