"""Regression tests for comparison operators with invalid operand types.

Comparing a :class:`~semver.version.Version` with an operand that cannot be
interpreted as a version must follow the library's documented policy for
invalid comparison operand types (see changelog entry for :gh:`316`):
the comparison operators return :py:const:`NotImplemented` so that Python
falls back to its default behavior, instead of leaking internal
conversion errors from ``Version.__init__``.
"""

import operator

import pytest

from semver import Version

MALFORMED_COLLECTIONS = [
    [],
    (),
    {},
    ["a"],
    (1, "x"),
    (1, 2, 3, 4, 5, 6),
    ["bogus"],
    {"bogus": 1},
    {"major": "a"},
]


@pytest.mark.parametrize("other", MALFORMED_COLLECTIONS)
def test_equality_with_malformed_collection_is_false(other):
    version = Version(1, 0, 0)
    # A malformed collection is not a valid comparison operand, so
    # equality must evaluate to False, not raise an internal error
    # such as "Version.__init__() missing 1 required positional
    # argument: 'major'".
    assert (version == other) is False
    assert version != other
    # Symmetric case: the reflected operation must not raise either.
    assert (other == version) is False
    assert other != version


@pytest.mark.parametrize("other", MALFORMED_COLLECTIONS)
def test_ordering_with_malformed_collection_raises_clean_typeerror(other):
    version = Version(1, 0, 0)
    # Ordering against an operand that is not comparable must raise the
    # standard Python TypeError, not an internal conversion error from
    # Version.__init__ (e.g. about missing/positional/keyword arguments
    # or int() literals).
    with pytest.raises(TypeError) as excinfo:
        operator.lt(version, other)
    assert "Version.__init__()" not in str(excinfo.value)
    assert "invalid literal for int()" not in str(excinfo.value)


def test_valid_collection_operands_still_compare():
    # Guards against over-rejecting: well-formed collections keep
    # comparing as versions.
    version = Version(1, 0, 0)
    assert version == (1, 0, 0)
    assert version == [1, 0, 0]
    assert version == {"major": 1, "minor": 0, "patch": 0}
    assert version < (2, 0, 0)
    assert version < [2, 0, 0]
    assert version < {"major": 2, "minor": 0, "patch": 0}
    assert operator.gt((2, 0, 0), version)
    assert version != (2, 0, 0)
