"""Version handling."""

import collections
import re
from functools import wraps
from typing import (
    Any,
    Callable,
    Collection,
    Dict,
    Iterable,
    List,
    Optional,
    SupportsInt,
    Tuple,
    Union,
    cast,
)

from ._types import (
    String,
    StringOrInt,
    VersionDict,
    VersionIterator,
    VersionPart,
    VersionTuple,
)

# These types are required here because of circular imports
Comparable = Union["Version", Dict[str, VersionPart], Collection[VersionPart], str]
Comparator = Callable[["Version", Comparable], bool]

T = TypeVar("T", bound="Version")


def _comparator(operator: Comparator) -> Comparator:
    """Wrap a Version binary op method in a type-check."""

    @wraps(operator)
    def wrapper(self: "Version", other: Comparable) -> bool:
        comparable_types = (
            Version,
            dict,
            tuple,
            list,
            *String.__args__,  # type: ignore
        )
        if not isinstance(other, comparable_types):
            return NotImplemented
        return operator(self, other)

    return wrapper


def _cmp(a, b):  # TODO: type hints
    """Return negative if a<b, zero if a==b, positive if a>b."""
    return (a > b) - (a < b)


class Version:
    """
    A semver compatible version class.

    :param args: a tuple with version information. It can consist of:

        * a maximum length of 5 items that comprehend the major,
          minor, patch, prerelease, or build parts.
        * a str or bytes string that contains a valid semver
          version string.
    :param major: version when you make incompatible API changes.
    :param minor: version when you add functionality in
                  a backwards-compatible manner.
    :param patch: version when you make backwards-compatible bug fixes.
    :param prerelease: an optional prerelease string
    :param build: an optional build string

    This gives you some options to call the :class:`Version` class.
    Precedence has the keyword arguments over the positional arguments.

    >>> Version(1, 2, 3)
    Version(major=1, minor=2, patch=3, prerelease=None, build=None)
    >>> Version("2.3.4-pre.2")
    Version(major=2, minor=3, patch=4, prerelease="pre.2", build=None)
    >>> Version(major=2, minor=3, patch=4, build="build.2")
    Version(major=2, minor=3, patch=4, prerelease=None, build="build.2")
    """

    __slots__ = ("_major", "_minor", "_patch", "_prerelease", "_build")

    #: The names of the different parts of a version
    NAMES = tuple([item[1:] for item in __slots__])

    #: Regex for number in a prerelease
    _LAST_NUMBER = re.compile(r"(?:[^\d]*(\d+)[^\d]*)+")
    #: Regex template for a semver version
    _REGEX_TEMPLATE = r"""
            ^
            (?P<major>0|[1-9]\d*)
            (?:
                \.
                (?P<minor>0|[1-9]\d*)
                (?:
                    \.
                    (?P<patch>0|[1-9]\d*)
                ){opt_patch}
            ){opt_minor}
            (?:-(?P<prerelease>
                (?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)
                (?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*
            ))?
            (?:\+(?P<build>
                [0-9a-zA-Z-]+
                (?:\.[0-9a-zA-Z-]+)*
            ))?
            $
        """
    #: Regex for a semver version
    _REGEX = re.compile(
        _REGEX_TEMPLATE.format(opt_patch="", opt_minor=""),
        re.VERBOSE,
    )
    #: Regex for a semver version that might be shorter
    _REGEX_OPTIONAL_MINOR_AND_PATCH = re.compile(
        _REGEX_TEMPLATE.format(opt_patch="?", opt_minor="?"),
        re.VERBOSE,
    )

    def __init__(
        self,
        *args: Tuple[
            StringOrInt,  # major
            Optional[StringOrInt],  # minor
            Optional[StringOrInt],  # patch
            Optional[StringOrInt],  # prerelease
            Optional[StringOrInt],  # build
        ],
        major: SupportsInt = 0,
        minor: SupportsInt = 0,
        patch: SupportsInt = 0,
        prerelease: Optional[Union[String, int]] = None,
        build: Optional[Union[String, int]] = None,
    ):
        def _check_types(*args):
            if args and len(args) > 5:
                raise ValueError("You cannot pass more than 5 arguments to Version")
            elif len(args) > 1 and "." in str(args[0]):
                raise ValueError(
                    "You cannot pass a string and additional positional arguments"
                )
            allowed_types_in_args = (
                (int, str, bytes),  # major
                (int, str, bytes),  # minor
                (int, str, bytes),  # patch
                (str, bytes, int, type(None)),  # prerelease
                (str, bytes, int, type(None)),  # build
            )
            return [
                isinstance(item, allowed_types_in_args[i])
                for i, item in enumerate(args)
            ]

        cls = self.__class__
        verlist: List[Optional[StringOrInt]] = [None, None, None, None, None]

        types_in_args = _check_types(*args)
        if not all(types_in_args):
            pos = types_in_args.index(False)
            raise TypeError(
                "not expecting type in argument position "
                f"{pos} (type: {type(args[pos])})"
            )
        elif args and "." in str(args[0]):
            # we have a version string as first argument
            v = cls._parse(args[0])  # type: ignore
            for idx, key in enumerate(
                ("major", "minor", "patch", "prerelease", "build")
            ):
                verlist[idx] = v[key]
        else:
            for index, item in enumerate(args):
                verlist[index] = args[index]  # type: ignore

        # Build a dictionary of the arguments except prerelease and build
        try:
            version_parts = {
                # Prefer major, minor, and patch arguments over args
                "major": int(major or verlist[0] or 0),
                "minor": int(minor or verlist[1] or 0),
                "patch": int(patch or verlist[2] or 0),
            }
        except ValueError:
            raise ValueError(
                "Expected integer or integer string for major, minor, or patch"
            )

        for name, value in version_parts.items():
            if value < 0:
                raise ValueError(
                    "{!r} is negative. A version can only be positive.".format(name)
                )

        self._major = version_parts["major"]
        self._minor = version_parts["minor"]
        self._patch = version_parts["patch"]
        self._prerelease = cls._enforce_str(prerelease or verlist[3])
        self._build = cls._enforce_str(build or verlist[4])

    @classmethod
    def _nat_cmp(cls, a, b):  # TODO: type hints
        def cmp_prerelease_tag(a, b):
            if isinstance(a, int) and isinstance(b, int):
                return _cmp(a, b)
            elif isinstance(a, int):
                return -1
            elif isinstance(b, int):
                return 1
            else:
                return _cmp(a, b)

        a, b = a or "", b or ""
        a_parts, b_parts = a.split("."), b.split(".")
        a_parts = [int(x) if re.match(r"^\d+$", x) else x for x in a_parts]
        b_parts = [int(x) if re.match(r"^\d+$", x) else x for x in b_parts]
        for sub_a, sub_b in zip(a_parts, b_parts):
            cmp_result = cmp_prerelease_tag(sub_a, sub_b)
            if cmp_result != 0:
                return cmp_result
        else:
            return _cmp(len(a), len(b))

    @classmethod
    def _enforce_str(cls, s: Optional[StringOrInt]) -> Optional[str]:
        """
        Forces input to be string, regardless of int, bytes, or string.

        :param s: a string, integer or None
        :return: a Unicode string (or None)
        """
        if isinstance(s, int):
            return str(s)
        return cls._ensure_str(s)

    @classmethod
    def _ensure_str(cls, s: Optional[String], encoding="UTF-8") -> Optional[str]:
        """
        Ensures string type regardless if argument type is str or bytes.

        :param s: the string (or None)
        :param encoding: the encoding, default to "UTF-8"
        :return: a Unicode string (or None)
        """
        if isinstance(s, bytes):
            return cast(str, s.decode(encoding))
        return s

    @classmethod
    def _parse(cls, version: String) -> Dict:
        """
        Parse version string and return version parts.

        :param version: version string
        :return: a dictionary with version parts
        :raises ValueError: if version is invalid
        :raises TypeError: if version contains unexpected type

        >>> semver.Version.parse('3.4.5-pre.2+build.4')
        Version(major=3, minor=4, patch=5, prerelease='pre.2', build='build.4')
        """
        version = cast(str, cls._ensure_str(version))
        if not isinstance(version, String.__args__):  # type: ignore
            raise TypeError(f"not expecting type {type(version)!r}")
        match = cls._REGEX.match(version)
        if match is None:
            raise ValueError(f"{version!r} is not valid SemVer string")

        return cast(dict, match.groupdict())

    @property
    def major(self) -> int:
        """The major part of a version (read-only)."""
        return self._major

    @major.setter
    def major(self, value):
        raise AttributeError("attribute 'major' is readonly")

    @property
    def minor(self) -> int:
        """The minor part of a version (read-only)."""
        return self._minor

    @minor.setter
    def minor(self, value):
        raise AttributeError("attribute 'minor' is readonly")

    @property
    def patch(self) -> int:
        """The patch part of a version (read-only)."""
        return self._patch

    @patch.setter
    def patch(self, value):
        raise AttributeError("attribute 'patch' is readonly")

    @property
    def prerelease(self) -> Optional[str]:
        """The prerelease part of a version (read-only)."""
        return self._prerelease

    @prerelease.setter
    def prerelease(self, value):
        raise AttributeError("attribute 'prerelease' is readonly")

    @property
    def build(self) -> Optional[str]:
        """The build part of a version (read-only)."""
        return self._build

    @build.setter
    def build(self, value):
        raise AttributeError("attribute 'build' is readonly")

    def to_tuple(self) -> VersionTuple:
        """
        Convert the Version object to a tuple.

        .. versionadded:: 2.10.0
           Renamed ``VersionInfo._astuple`` to ``VersionInfo.to_tuple`` to
           make this function available in the public API.

        :return: a tuple with all the parts

        >>> semver.Version(5, 3, 1).to_tuple()
        (5, 3, 1, None, None)
        """
        return (self.major, self.minor, self.patch, self.prerelease, self.build)

    def to_dict(self) -> VersionDict:
        """
        Convert the Version object to an OrderedDict.

        .. versionadded:: 2.10.0
           Renamed ``VersionInfo._asdict`` to ``VersionInfo.to_dict`` to
           make this function available in the public API.

        :return: an OrderedDict with the keys in the order ``major``, ``minor``,
          ``patch``, ``prerelease``, and ``build``.

        >>> semver.Version(3, 2, 1).to_dict()
        OrderedDict([('major', 3), ('minor', 2), ('patch', 1), ('prerelease', None), ('build', None)])  # noqa: E501
        """
        return collections.OrderedDict(
            (
                ("major", self.major),
                ("minor", self.minor),
                ("patch", self.patch),
                ("prerelease", self.prerelease),
                ("build", self.build),
            )
        )

    def __iter__(self) -> VersionIterator:
        """Return iter(self)."""
        yield from self.to_tuple()

    @staticmethod
    def _increment_string(string: str) -> str:
        """
        Look for the last sequence of number(s) in a string and increment.

        :param string: the string to search for.
        :return: the incremented string

        Source:
        http://code.activestate.com/recipes/442460-increment-numbers-in-a-string/#c1
        """
        match = Version._LAST_NUMBER.search(string)
        if match:
            next_ = str(int(match.group(1)) + 1)
            start, end = match.span(1)
            string = string[: max(end - len(next_), start)] + next_ + string[end:]
        return string

    def bump_major(self) -> "Version":
        """
        Raise the major part of the version, return a new object but leave self
        untouched.

        :return: new object with the raised major part

        >>> semver.Version("3.4.5").bump_major()
        Version(major=4, minor=0, patch=0, prerelease=None, build=None)
        """
        cls = type(self)
        return cls(major=self._major + 1)

    def bump_minor(self) -> "Version":
        """
        Raise the minor part of the version, return a new object but leave self
        untouched.

        :return: new object with the raised minor part

        >>> semver.Version("3.4.5").bump_minor()
        Version(major=3, minor=5, patch=0, prerelease=None, build=None)
        """
        cls = type(self)
        return cls(major=self._major, minor=self._minor + 1)

    def bump_patch(self) -> "Version":
        """
        Raise the patch part of the version, return a new object but leave self
        untouched.

        :return: new object with the raised patch part

        >>> semver.Version("3.4.5").bump_patch()
        Version(major=3, minor=4, patch=6, prerelease=None, build=None)
        """
        cls = type(self)
        return cls(major=self._major, minor=self._minor, patch=self._patch + 1)

    def bump_prerelease(self, token: Optional[str] = "rc") -> "Version":
        """
        Raise the prerelease part of the version, return a new object but leave
        self untouched.

        :param token: defaults to ``'rc'``
        :return: new :class:`Version` object with the raised prerelease part.
            The original object is not modified.

        >>> ver = semver.parse("3.4.5")
        >>> ver.bump_prerelease().prerelease
        'rc.2'
        >>> ver.bump_prerelease('').prerelease
        '1'
        >>> ver.bump_prerelease(None).prerelease
        'rc.1'
        """
        cls = type(self)
        prerelease = cls._increment_string(self._prerelease or (token or "rc") + ".0")
        return cls(
            major=self._major,
            minor=self._minor,
            patch=self._patch,
            prerelease=prerelease,
        )

    def bump_build(self, token: Optional[str] = "build") -> "Version":
        """
        Raise the build part of the version, return a new object but leave self
        untouched.

        :param token: defaults to ``'build'``
        :return: new :class:`Version` object with the raised build part.
            The original object is not modified.

        >>> semver.Version("3.4.5-rc.1+build.9").bump_build()
        Version(major=3, minor=4, patch=5, prerelease='rc.1', build='build.10')  # noqa: E501
        """
        cls = type(self)
        build = cls._increment_string(self._build or (token or "build") + ".0")
        return cls(
            major=self._major,
            minor=self._minor,
            patch=self._patch,
            prerelease=self._prerelease,
            build=build,
        )

    def compare(self, other: Comparable) -> int:
        """
        Compare self with other.

        :param other: the second version
        :return: The return value is negative if ver1 < ver2,
             zero if ver1 == ver2 and strictly positive if ver1 > ver2

        >>> semver.Version("1.0.0").compare("2.0.0")
        -1
        >>> semver.Version("1.0.0").compare("1.0.0")
        0
        >>> semver.Version("1.0.0").compare("0.1.0")
        -1
        >>> semver.Version("2.0.0").compare(dict(major=2, minor=0, patch=0))
        0
        """
        cls = type(self)
        if isinstance(other, String.__args__):  # type: ignore
            other = cls.parse(other)
        elif isinstance(other, dict):
            other = cls(**other)
        elif isinstance(other, (tuple, list)):
            other = cls(*other)
        elif not isinstance(other, cls):
            raise TypeError(
                f"Expected str, bytes, dict, tuple, list, or {cls.__name__} instance, "
                f"but got {type(other)}"
            )

        v1 = self.to_tuple()[:3]
        v2 = other.to_tuple()[:3]
        x = _cmp(v1, v2)
        if x:
            return x

        rc1, rc2 = self.prerelease, other.prerelease
        rccmp = self._nat_cmp(rc1, rc2)

        if not rccmp:
            return 0
        if not rc1:
            return 1
        elif not rc2:
            return -1

        return rccmp

    def next_version(self, part: str, prerelease_token: str = "rc") -> "Version":
        """
        Determines next version, preserving natural order.

        .. versionadded:: 2.10.0

        This function is taking prereleases into account.
        The "major", "minor", and "patch" raises the respective parts like
        the ``bump_*`` functions. The real difference is using the
        "preprelease" part. It gives you the next patch version of the
        prerelease, for example:

        :param part: One of "major", "minor", "patch", or "prerelease"
        :param prerelease_token: prefix string of prerelease, defaults to 'rc'
        :return: new object with the appropriate part raised

        >>> str(semver.Version("0.1.4").next_version("prerelease"))
        '0.1.5-rc.1'
        """
        cls = type(self)
        # "build" is currently not used, that's why we use [:-1]
        validparts = cls.NAMES[:-1]
        if part not in validparts:
            raise ValueError(
                "Invalid part. Expected one of {validparts}, but got {part!r}".format(
                    validparts=validparts, part=part
                )
            )
        version = self
        if (version.prerelease or version.build) and (
            part == "patch"
            or (part == "minor" and version.patch == 0)
            or (part == "major" and version.minor == version.patch == 0)
        ):
            return version.replace(prerelease=None, build=None)

        # Only check the main parts:
        if part in cls.NAMES[:3]:
            return getattr(version, "bump_" + part)()

        if not version.prerelease:
            version = version.bump_patch()
        return version.bump_prerelease(prerelease_token)

    @_comparator
    def __eq__(self, other: Comparable) -> bool:  # type: ignore
        return self.compare(other) == 0

    @_comparator
    def __ne__(self, other: Comparable) -> bool:  # type: ignore
        return self.compare(other) != 0

    @_comparator
    def __lt__(self, other: Comparable) -> bool:
        return self.compare(other) < 0

    @_comparator
    def __le__(self, other: Comparable) -> bool:
        return self.compare(other) <= 0

    @_comparator
    def __gt__(self, other: Comparable) -> bool:
        return self.compare(other) > 0

    @_comparator
    def __ge__(self, other: Comparable) -> bool:
        return self.compare(other) >= 0

    def __getitem__(
        self, index: Union[int, slice]
    ) -> Union[int, Optional[str], Tuple[Union[int, str], ...]]:
        """
        self.__getitem__(index) <==> self[index] Implement getitem.

        If the part  requested is undefined, or a part of the range requested
        is undefined, it will throw an index error.
        Negative indices are not supported.

        :param index: a positive integer indicating the
               offset or a :func:`slice` object
        :raises IndexError: if index is beyond the range or a part is None
        :return: the requested part of the version at position index

        >>> ver = semver.Version("3.4.5")
        >>> ver[0], ver[1], ver[2]
        (3, 4, 5)
        """
        if isinstance(index, int):
            index = slice(index, index + 1)
        index = cast(slice, index)

        if (
            isinstance(index, slice)
            and (index.start is not None and index.start < 0)
            or (index.stop is not None and index.stop < 0)
        ):
            raise IndexError("Version index cannot be negative")

        part = tuple(
            filter(lambda p: p is not None, cast(Iterable, self.to_tuple()[index]))
        )

        if len(part) == 1:
            return part[0]
        elif not part:
            raise IndexError("Version part undefined")
        return part

    def __repr__(self) -> str:
        s = ", ".join("%s=%r" % (key, val) for key, val in self.to_dict().items())
        return "%s(%s)" % (type(self).__name__, s)

    def __str__(self) -> str:
        version = f"{self.major:d}.{self.minor:d}.{self.patch:d}"
        if self.prerelease:
            version += f"-{self.prerelease}"
        if self.build:
            version += f"+{self.build}"
        return version

    def __hash__(self) -> int:
        return hash(self.to_tuple()[:4])

    def finalize_version(self) -> "Version":
        """
        Remove any prerelease and build metadata from the version.

        :return: a new instance with the finalized version string

        >>> str(semver.Version('1.2.3-rc.5').finalize_version())
        '1.2.3'
        """
        cls = type(self)
        return cls(major=self.major, minor=self.minor, patch=self.patch)

    def match(self, match_expr: str) -> bool:
        """
        Compare self to match a match expression.

        :param match_expr: optional operator and version; valid operators are
              ``<```   smaller than
              ``>``   greater than
              ``>=``  greator or equal than
              ``<=``  smaller or equal than
              ``==``  equal
              ``!=``  not equal
        :return: True if the expression matches the version, otherwise False

        >>> semver.Version("2.0.0").match(">=1.0.0")
        True
        >>> semver.Version("1.0.0").match(">1.0.0")
        False
        >>> semver.Version.parse("4.0.4").match("4.0.4")
        True
        """
        prefix = match_expr[:2]
        if prefix in (">=", "<=", "==", "!="):
            match_version = match_expr[2:]
        elif prefix and prefix[0] in (">", "<"):
            prefix = prefix[0]
            match_version = match_expr[1:]
        elif match_expr and match_expr[0] in "0123456789":
            prefix = "=="
            match_version = match_expr
        else:
            raise ValueError(
                "match_expr parameter should be in format <op><ver>, "
                "where <op> is one of "
                "['<', '>', '==', '<=', '>=', '!=']. "
                "You provided: %r" % match_expr
            )

        possibilities_dict = {
            ">": (1,),
            "<": (-1,),
            "==": (0,),
            "!=": (-1, 1),
            ">=": (0, 1),
            "<=": (-1, 0),
        }

        possibilities = possibilities_dict[prefix]
        cmp_res = self.compare(match_version)

        return cmp_res in possibilities

    @classmethod
    def parse(
        cls: Type[T], version: String, optional_minor_and_patch: bool = False
    ) -> T:
        """
        Parse version string to a Version instance.

        .. versionchanged:: 2.11.0
           Changed method from static to classmethod to
           allow subclasses.
        .. versionchanged:: 3.0.0
           Added optional parameter optional_minor_and_patch to allow optional
           minor and patch parts.

        :param version: version string
        :param optional_minor_and_patch: if set to true, the version string to parse \
           can contain optional minor and patch parts. Optional parts are set to zero.
           By default (False), the version string to parse has to follow the semver
           specification.
        :return: a new :class:`Version` instance
        :raises ValueError: if version is invalid
        :raises TypeError: if version contains the wrong type

        >>> semver.Version('3.4.5-pre.2+build.4')
        Version(major=3, minor=4, patch=5, prerelease='pre.2', build='build.4')  # noqa: E501
        """
        if isinstance(version, bytes):
            version = version.decode("UTF-8")
        elif not isinstance(version, String.__args__):  # type: ignore
            raise TypeError("not expecting type '%s'" % type(version))

        if optional_minor_and_patch:
            match = cls._REGEX_OPTIONAL_MINOR_AND_PATCH.match(version)
        else:
            match = cls._REGEX.match(version)
        if match is None:
            raise ValueError(f"{version} is not valid SemVer string")

        matched_version_parts: Dict[str, Any] = match.groupdict()
        if not matched_version_parts["minor"]:
            matched_version_parts["minor"] = 0
        if not matched_version_parts["patch"]:
            matched_version_parts["patch"] = 0

        return cls(**matched_version_parts)

    def replace(self, **parts: Union[int, Optional[str]]) -> "Version":
        """
        Replace one or more parts of a version and return a new
        :class:`Version` object, but leave self untouched

        .. versionadded:: 2.9.0
           Added :func:`Version.replace`

        :param parts: the parts to be updated. Valid keys are:
          ``major``, ``minor``, ``patch``, ``prerelease``, or ``build``
        :return: the new :class:`Version` object with the changed
          parts
        :raises TypeError: if ``parts`` contain invalid keys
        """
        version = self.to_dict()
        version.update(parts)
        try:
            return Version(**version)  # type: ignore
        except TypeError:
            unknownkeys = set(parts) - set(self.to_dict())
            error = "replace() got %d unexpected keyword argument(s): %s" % (
                len(unknownkeys),
                ", ".join(unknownkeys),
            )
            raise TypeError(error)

    @classmethod
    def is_valid(cls, version: str) -> bool:
        """
        Check if the string is a valid semver version.

        .. versionadded:: 2.9.1

        :param version: the version string to check
        :return: True if the version string is a valid semver version, False
                 otherwise.
        """
        try:
            cls.parse(version)
            return True
        except ValueError:
            return False

    def is_compatible(self, other: "Version") -> bool:
        """
        Check if current version is compatible with other version.

        The result is True, if either of the following is true:

        * both versions are equal, or
        * both majors are equal and higher than 0. Same for both minors.
          Both pre-releases are equal, or
        * both majors are equal and higher than 0. The minor of b's
          minor version is higher then a's. Both pre-releases are equal.

        The algorithm does *not* check patches.

        :param other: the version to check for compatibility
        :return: True, if ``other`` is compatible with the old version,
                 otherwise False

        >>> Version(1, 1, 0).is_compatible(Version(1, 0, 0))
        False
        >>> Version(1, 0, 0).is_compatible(Version(1, 1, 0))
        True
        """
        if not isinstance(other, Version):
            raise TypeError(f"Expected a Version type but got {type(other)}")

        # All major-0 versions should be incompatible with anything but itself
        if (0 == self.major == other.major) and (self[:4] != other[:4]):
            return False

        return (
            (self.major == other.major)
            and (other.minor >= self.minor)
            and (self.prerelease == other.prerelease)
        )


#: Keep the VersionInfo name for compatibility
VersionInfo = Version
