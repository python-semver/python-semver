"""Defines basic regex constants."""

import re
from typing import ClassVar, Pattern, Tuple


class VersionRegex:
    """
    Base class of regular expressions for semver versions.

    You don't instantiate this class.
    """

    #: a number
    _RE_NUMBER: ClassVar[str] = r"0|[1-9]\d*"

    #:
    _LAST_NUMBER: ClassVar[Pattern[str]]  = re.compile(r"(?:[^\d]*(\d+)[^\d]*)+")

    #: The names of the different parts of a version
    NAMES: ClassVar[Tuple[str, ...]] = ("major", "minor", "patch", "prerelease", "build")

    #: The regex of the major part of a version:
    MAJOR: ClassVar[str] = rf"(?P<major>{_RE_NUMBER})"
    #: The regex of the minor part of a version:
    MINOR: ClassVar[str] = rf"(?P<minor>{_RE_NUMBER})"
    #: The regex of the patch part of a version:
    PATCH: ClassVar[str] = rf"(?P<patch>{_RE_NUMBER})"
    #: The regex of the prerelease part of a version:
    PRERELEASE: ClassVar[str] = rf"""(?P<prerelease>
                (?:{_RE_NUMBER}|\d*[a-zA-Z-][0-9a-zA-Z-]*)
                (?:\.(?:{_RE_NUMBER}|\d*[a-zA-Z-][0-9a-zA-Z-]*))*
                )
    """

    #: The regex of the build part of a version:
    BUILD: ClassVar[str] = r"""(?P<build>
                [0-9a-zA-Z-]+
                (?:\.[0-9a-zA-Z-]+)*
            )"""

    #: Regex template for a semver version
    REGEX_TEMPLATE: ClassVar[str] = rf"""
        ^
        {MAJOR}
        (?:
            \.{MINOR}
            (?:
                \.{PATCH}
            ){{opt_patch}}
        ){{opt_minor}}
        (?:-{PRERELEASE})?
        (?:\+{BUILD})?
        $
    """

    #: Regex for a semver version
    REGEX: ClassVar[Pattern[str]] = re.compile(
        REGEX_TEMPLATE.format(opt_patch="", opt_minor=""),
        re.VERBOSE,
    )

    #: Regex for a semver version that might be shorter
    REGEX_OPTIONAL_MINOR_AND_PATCH: ClassVar[Pattern[str]] = re.compile(
        REGEX_TEMPLATE.format(opt_patch="?", opt_minor="?"),
        re.VERBOSE,
    )
