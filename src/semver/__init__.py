"""
semver package major release 3.

A Python module for semantic versioning. Simplifies comparing versions.
"""

from ._deprecated import (
    bump_build,
    bump_major,
    bump_minor,
    bump_patch,
    bump_prerelease,
    compare,
    finalize_version,
    format_version,
    match,
    max_ver,
    min_ver,
    parse,
    parse_version_info,
    replace,
    cmd_bump,
    cmd_compare,
    cmd_nextver,
    cmd_check,
    createparser,
    process,
    main,
)
from .version import Version, VersionInfo
from .__about__ import (
    __version__,
    __author__,
    __maintainer__,
    __author_email__,
    __description__,
    __maintainer_email__,
    SEMVER_SPEC_VERSION,
)
