""""""

# from ast import Str
from functools import wraps
import re
from typing import (
    Callable,
    List,
    Optional,
    Union,
    cast,
)

from .versionregex import VersionRegex
from .version import Version
from ._types import String

Int_or_Str = Union[int, str]


class InvalidSpecifier(ValueError):
    """
    Raised when attempting to create a :class:`Spec <semver.spec.Spec>` with an
    invalid specifier string.

    >>> Spec("lolwat")
    Traceback (most recent call last):
        ...
    semver.spec.InvalidSpecifier: Invalid specifier: 'lolwat'
    """


# These types are required here because of circular imports
SpecComparable = Union[Version, str, bytes, dict, tuple, list]
SpecComparator = Callable[["Spec", SpecComparable], bool]


def preparecomparison(operator: SpecComparator) -> SpecComparator:
    """Wrap a Spec binary operator method in a type-check."""

    @wraps(operator)
    def wrapper(self: "Spec", other: SpecComparable) -> bool:
        comparable_types = (*SpecComparable.__args__,)  # type: ignore
        if not isinstance(other, comparable_types):
            return NotImplemented
        # For compatible types, convert them to Version instance:
        if isinstance(other, String.__args__):    # type: ignore
            other = Version.parse(cast(String, other))
        if isinstance(other, dict):
            other = Version(**other)
        if isinstance(other, (tuple, list)):
            other = Version(*other)

        # For the time being, we restrict the version to
        # major, minor, patch only
        other = cast(Version, other).to_tuple()[:3]
        # TODO: attach index variable to the function somehow
        # index = self.__get_index()

        return operator(cast("Spec", self), other)

    return wrapper


class Spec(VersionRegex):
    """
    Handles version specifiers.

    Contains a comparator which specifies a version.
    A comparator is composed of an *optional operator* and a
    *version specifier*.

    Valid operators are:

    * ``<`` smaller than
    * ``>`` greater than
    * ``>=`` greater or equal than
    * ``<=`` smaller or equal than
    * ``==`` equal
    * ``!=`` not equal
    * ``~`` for tilde ranges, see :ref:`tilde_expressions`
    * ``^`` for caret ranges, see :ref:`caret_expressions`

    Valid *version specifiers* follows the syntax ``major[.minor[.patch]]``,
    whereas the minor and patch parts are optional. Additionally,
    the minor and patch parts can contain placeholders.

    For example, the comparator ``>=1.2.3`` match the versions
    ``1.2.3``, ``1.2.4``, ``1.2.5`` and so on, but not the versions
    ``1.2.2``, ``1.2.0``, or ``1.1.0``.

    Version specifiers with *missing parts* are "normalized".
    For example, the comparator ``>=1`` is normalized internally to
    ``>=1.0.0`` and ``>=1.2`` is normalized to ``>=1.2.0``.

    Version specifiers with *placeholders* are amended with other
    placeholders to the right. For example, the comparator ``>=1.*``
    is internally rewritten to ``>=1.*.*``. The characters ``x``,
    ``X``, or ``*`` can be used interchangeably. If you print this
    class however, only ``*`` is used regardless what you used before.

    It is not allowed to use forms like ``>=1.*.3``, this will raise
    :class:`InvalidSpecifier <semver.spec.InvalidSpecifier>`.
    """

    #: the allowed operators
    _operator_regex_str = r"""
        (?P<operator><=|>=|==|!=|[<]|[>]|[~]|\^)
    """

    #: the allowed characters as a placeholder
    _version_any = r"\*|x"

    #: the spec regular expression
    _version_regex_str = rf"""
        (?P<version>
            {VersionRegex._MAJOR}
            (?:
                \.
                (?P<minor>{VersionRegex._RE_NUMBER}|{_version_any})
                (?:
                    \.
                    (?P<patch>{VersionRegex._RE_NUMBER}|{_version_any})
                )?
            )?
            (?:-{VersionRegex._PRERELEASE})?
        )
        $
    """

    _regex = re.compile(
        rf"{_operator_regex_str}?\s*{_version_regex_str}",
        re.VERBOSE | re.IGNORECASE
    )

    _regex_version_any = re.compile(_version_any, re.VERBOSE | re.IGNORECASE)

    _regex_operator_regex_str = re.compile(_operator_regex_str, re.VERBOSE)

    def __init__(self, spec: Union[str, bytes]) -> None:
        """
        Initialize a Spec instance.

        :param spec: String representation of a specifier which
            will be parsed and normalized before use.

            Every specifier contains:

            * an optional operator (if omitted, "==" is used)
            * a version identifier (can contain "*" or "x" as placeholders)

            Valid operators are:
              ``<``   smaller than
              ``>``   greater than
              ``>=``  greator or equal than
              ``<=``  smaller or equal than
              ``==``  equal
              ``!=``  not equal
              ``~``   compatible release clause ("tilde ranges")
              ``^``   compatible with version
        """
        cls = type(self)

        if not spec:
            raise InvalidSpecifier(
                "Invalid specifier: argument should contain an non-empty string"
            )

        # Convert bytes -> str
        if isinstance(spec, bytes):
            spec = spec.decode("utf-8")

        # Save the match
        match = cls._regex.match(spec)
        if not match:
            # TODO: improve error message
            # distinguish between bad operator or
            # bad version string
            raise InvalidSpecifier(f"Invalid specifier: '{spec}'")

        self._raw = match.groups()
        # If operator was omitted, it's equivalent to "=="
        self._operator = "==" if match["operator"] is None else match["operator"]

        major, minor, patch = match["major"], match["minor"], match["patch"]

        placeholders = ("x", "X", "*")
        # Check if we have an invalid "1.x.2" version specifier:
        if (minor in placeholders) and (patch not in (*placeholders, None)):
            raise InvalidSpecifier(
                "invalid specifier: you can't have minor as placeholder "
                "and patch as a number."
            )

        self.real_version_tuple: Union[list, tuple] = [
            cls.normalize(major),
            cls.normalize(minor),
            cls.normalize(patch),
            # cls.normalize(prerelease),  # really?
        ]

        # This is the special case for 1 -> 1.0.0
        if (minor is None and patch is None):
            self.real_version_tuple[1:3] = (0, 0)
        elif (minor not in placeholders) and (patch is None):
            self.real_version_tuple[2] = 0
        elif (minor in placeholders) and (patch is None):
            self.real_version_tuple[2] = "*"

        self.real_version_tuple = tuple(self.real_version_tuple)

        # Contains a (partial) version string
        self._realversion: str = ".".join(
            str(item) for item in self.real_version_tuple if item is not None
        )

    @staticmethod
    def normalize(value: Optional[str]) -> Union[str, int]:
        """
        Normalize a version part.

        :param value: the value to normalize
        :return: the normalized value

        * Convert None -> ``*``
        * Unify any "*", "x", or "X" to "*"
        * Convert digits
        """
        if value is None:
            return "*"
        value = value.lower().replace("x", "*")
        try:
            return int(value)
        except ValueError:
            return value

    @property
    def operator(self) -> str:
        """
        The operator of this specifier.

        >>> Spec("==1.2.3").operator
        '=='
        >>> Spec("1.2.3").operator
        '=='
        """
        return self._operator

    @property
    def realversion(self) -> str:
        """
        The real version of this specifier.

        Versions that contain "*", "x", or "X" are unified and these
        characters are replaced by "*".

        >>> Spec("1").realversion
        '1.0.0'
        >>> Spec("1.2").realversion
        '1.2.*'
        >>> Spec("1.2.3").realversion
        '1.2.3'
        >>> Spec("1.*").realversion
        '1.*.*'
        """
        return self._realversion

    @property
    def spec(self) -> str:
        """
        The specifier (operator and version string)

        >>> Spec(">=1.2.3").spec
        '>=1.2.3'
        >>> Spec(">=1.2.x").spec
        '>=1.2.*'
        """
        return f"{self._operator}{self._realversion}"

    def __repr__(self) -> str:
        """
        A representation of the specifier that shows all internal state.

        >>> Spec('>=1.0.0')
        Spec('>=1.0.0')
        """
        return f"{self.__class__.__name__}({str(self)!r})"

    def __str__(self) -> str:
        """
        A string representation of the specifier that can be round-tripped.

        >>> str(Spec('>=1.0.0'))
        '>=1.0.0'
        """
        return self.spec

    def __get_index(self) -> Optional[int]:
        try:
            index = self.real_version_tuple.index("*")
        except ValueError:
            # With None, any array[:None] will produce the complete array
            index = None

        return index

    @preparecomparison
    def __eq__(self, other: SpecComparable) -> bool:  # type: ignore
        """self == other."""
        # Find the position of the first "*"
        index = self.__get_index()
        version = tuple([
            int(cast(int, item))
            for item in self.real_version_tuple[:index]
        ])

        return cast(Version, other[:index]) == version

    @preparecomparison
    def __ne__(self, other: SpecComparable) -> bool:  # type: ignore
        """self != other."""
        index = self.__get_index()
        version = tuple([
            int(cast(int, item))
            for item in self.real_version_tuple[:index]
        ])
        return cast(Version, other[:index]) != version

    @preparecomparison
    def __lt__(self, other: SpecComparable) -> bool:
        """self < other."""
        index: Optional[int] = self.__get_index()
        version = tuple([
            int(cast(int, item))
            for item in self.real_version_tuple[:index]
        ])
        return cast(Version, other[:index]) < version

    @preparecomparison
    def __gt__(self, other: SpecComparable) -> bool:
        """self > other."""
        index = self.__get_index()
        version = tuple([
            int(cast(int, item))
            for item in self.real_version_tuple[:index]
        ])
        return cast(Version, other[:index]) > version

    @preparecomparison
    def __le__(self, other: SpecComparable) -> bool:
        """self <= other."""
        index = self.__get_index()
        version = tuple([
            int(cast(int, item))
            for item in self.real_version_tuple[:index]
        ])
        return cast(Version, other[:index]) <= version

    @preparecomparison
    def __ge__(self, other: SpecComparable) -> bool:
        """self >= other."""
        index = self.__get_index()
        version = tuple([
            int(cast(int, item))
            for item in self.real_version_tuple[:index]
        ])
        return cast(Version, other[:index]) >= version

    # @preparecomparison
    def _tilde(self, other: SpecComparable) -> bool:
        """
        Allows patch-level changes if a minor version is specified.

        :param other: the version that should match the spec
        :return: True, if the version is between the tilde
          range, otherwise False

        .. code-block::

           ~1.2.3 =  >=1.2.3 <1.(2+1).0 := >=1.2.3 <1.3.0
           ~1.2   =  >=1.2.0 <1.(2+1).0 := >=1.2.0 <1.3.0
           ~1     =  >=1.0.0 <(1+1).0.0 := >=1.0.0 <2.0.0
        """
        major, minor = cast(List[str], self.real_version_tuple[0:2])

        # Look for major, minor, patch only
        length = len([i for i in self._raw[2:-1] if i is not None])

        u_version = ".".join(
            [
                str(int(major) + 1 if length == 1 else major),
                str(int(minor) + 1 if length >= 2 else minor),
                "0",
            ])
        # print("> tilde", length, u_version)

        # Delegate it to other
        lowerversion: Spec = Spec(f">={self._realversion}")
        upperversion: Spec = Spec(f"<{u_version}")
        # print(">>", lowerversion, upperversion)
        return lowerversion.match(other) and upperversion.match(other)

    # @preparecomparison
    def _caret(self, other: SpecComparable) -> bool:
        """

        :param other: the version that should match the spec
        :return: True, if the version is between the caret
          range, otherwise False

        .. code-block::

           ^1.2.3 =  >=1.2.3 <2.0.0
           ^0.2.3 =  >=0.2.3 <0.3.0
           ^0.0.3 =  >=0.0.3 <0.0.4

           ^2, ^2.x, ^2.x.x =  >=2.0.0 <3.0.0
           ^1.2.x =  >=1.2.0 <2.0.0
           ^1.x   =  >=1.0.0 <2.0.0
           ^0.0.x =  >=0.0.0 <0.1.0
           ^0.x   =  >=0.0.0 <1.0.0
        """
        major, minor, patch = cast(List[int], self.real_version_tuple[0:3])

        # Distinguish between star versions and "real" versions
        if "*" in self._realversion:
            # version = [i if i != "*" else 0 for i in self.real_version_tuple]

            if int(major) > 0:
                u_version = [
                    str(int(major) + 1),
                    "0",
                    "0",
                ]
            else:
                u_version = ["0", "0" if minor else str(int(minor) + 1), "0"]

        else:
            if self.real_version_tuple == (0, 0, 0):
                u_version = ["0", "1", "0"]
            elif self.real_version_tuple[0] == 0:
                u_version = [
                    str(self.real_version_tuple[0]),
                    "0" if not minor else str(int(minor) + 1),
                    "0" if minor else str(int(patch) + 1),
                ]
            else:
                u_version = [str(int(major) + 1), "0", "0"]

        # Delegate the comparison
        lowerversion = Spec(f">={self._realversion}")
        upperversion = Spec(f"<{'.'.join(u_version)}")
        return lowerversion.match(other) and upperversion.match(other)

    def match(self, other: SpecComparable) -> bool:
        """
        Compare a match expression with another version.

        :param other: the other version to match with our expression
        :return: True if the expression matches the version, otherwise False
        """
        operation_table = {
            "==": self.__eq__,
            "!=": self.__ne__,
            "<": self.__lt__,
            ">": self.__gt__,
            "<=": self.__le__,
            ">=": self.__ge__,
            "~": self._tilde,
            "^": self._caret,
        }
        comparisonfunc = operation_table[self._operator]
        return comparisonfunc(other)
