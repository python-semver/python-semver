import pytest

from semver import Version


@pytest.mark.parametrize(
    "left,right,expected",
    [
        ("1.2.3-alpha+one", "2.3.4-beta+two", "major"),
        ("1.2.3-alpha+one", "1.3.4-beta+two", "minor"),
        ("1.2.3-alpha+one", "1.2.4-beta+two", "patch"),
        ("1.2.3-alpha+one", "1.2.3-beta+two", "prerelease"),
        ("1.2.3-alpha", "1.2.3", "prerelease"),
        ("1.2.3+one", "1.2.3+two", "build"),
        ("1.2.3", "1.2.3+one", "build"),
        ("1.2.3", "1.2.3", None),
        ("1.2.3-alpha+one", "1.2.3-alpha+one", None),
    ],
)
def test_diff(left, right, expected):
    left, right = Version.parse(left), Version.parse(right)
    assert left.diff(right) == expected
    assert right.diff(left) == expected


@pytest.mark.parametrize(
    "other", [None, 1, "1.2.3", b"1.2.3", (1, 2, 3), [1, 2, 3], {"major": 1}]
)
def test_diff_requires_version(other):
    with pytest.raises(TypeError, match="Expected Version instance"):
        Version(1, 2, 3).diff(other)


def test_diff_accepts_subclass():
    class DerivedVersion(Version):
        pass

    assert Version(1).diff(DerivedVersion(2)) == "major"
    assert DerivedVersion(1).diff(Version(2)) == "major"


def test_build_diff_does_not_change_precedence():
    left, right = Version.parse("1.2.3+one"), Version.parse("1.2.3+two")
    assert left == right
    assert left.diff(right) == "build"
