"""Defines basic regex constants."""

import re
from typing import ClassVar, Pattern


class VersionRegex:
    """
    Base class of regular expressions for semver versions.

    You don't instantiate this class.
    """
    #: a number
    _RE_NUMBER: ClassVar[str] = r"0|[1-9]\d*"

    #:
    _LAST_NUMBER: ClassVar[Pattern[str]]  = re.compile(r"(?:[^\d]*(\d+)[^\d]*)+")

    #: The regex of the major part of a version:
    _MAJOR: ClassVar[str] = rf"(?P<major>{_RE_NUMBER})"
    #: The regex of the minor part of a version:
    _MINOR: ClassVar[str] = rf"(?P<minor>{_RE_NUMBER})"
    #: The regex of the patch part of a version:
    _PATCH: ClassVar[str] = rf"(?P<patch>{_RE_NUMBER})"
    #: The regex of the prerelease part of a version:
    _PRERELEASE: ClassVar[str] = rf"""(?P<prerelease>
                (?:{_RE_NUMBER}|\d*[a-zA-Z-][0-9a-zA-Z-]*)
                (?:\.(?:{_RE_NUMBER}|\d*[a-zA-Z-][0-9a-zA-Z-]*))*
                )
    """
    #: The regex of the build part of a version:
    _BUILD: ClassVar[str] = r"""(?P<build>
                [0-9a-zA-Z-]+
                (?:\.[0-9a-zA-Z-]+)*
            )"""

    #: Regex template for a semver version
    _REGEX_TEMPLATE: ClassVar[str] = rf"""
        ^
        {_MAJOR}
        (?:
            \.{_MINOR}
            (?:
                \.{_PATCH}
            ){{opt_patch}}
        ){{opt_minor}}
        (?:-{_PRERELEASE})?
        (?:\+{_BUILD})?
        $
    """

    #: Regex for a semver version
    _REGEX: ClassVar[Pattern[str]] = re.compile(
        _REGEX_TEMPLATE.format(opt_patch='', opt_minor=''),
        re.VERBOSE,
    )

    #: Regex for a semver version that might be shorter
    _REGEX_OPTIONAL_MINOR_AND_PATCH: ClassVar[Pattern[str]] = re.compile(
        _REGEX_TEMPLATE.format(opt_patch='?', opt_minor='?'),
        re.VERBOSE,
    )
