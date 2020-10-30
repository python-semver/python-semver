import re
from semver import Version
from typing import Optional, Tuple


BASEVERSION = re.compile(
    r"""[vV]?
        (?P<major>0|[1-9]\d*)
        (\.
        (?P<minor>0|[1-9]\d*)
        (\.
            (?P<patch>0|[1-9]\d*)
        )?
        )?
    """,
    re.VERBOSE,
)


def coerce(version: str) -> Tuple[Version, Optional[str]]:
    """
    Convert an incomplete version string into a semver-compatible Version
    object

    * Tries to detect a "basic" version string (``major.minor.patch``).
    * If not enough components can be found, missing components are
        set to zero to obtain a valid semver version.

    :param str version: the version string to convert
    :return: a tuple with a :class:`Version` instance (or ``None``
        if it's not a version) and the rest of the string which doesn't
        belong to a basic version.
    :rtype: tuple(:class:`Version` | None, str)
    """
    match = BASEVERSION.search(version)
    if not match:
        return (None, version)

    ver = {
        key: 0 if value is None else value for key, value in match.groupdict().items()
    }
    ver = Version(**ver)
    rest = match.string[match.end() :]  # noqa:E203
    return ver, rest
