import pytest

import semver
from semver import Version, compare


@pytest.mark.parametrize(
    "left,right",
    [
        ("1.0.0", "2.0.0"),
        ("1.0.0-alpha", "1.0.0-alpha.1"),
        ("1.0.0-alpha.1", "1.0.0-alpha.beta"),
        ("1.0.0-alpha.beta", "1.0.0-beta"),
        ("1.0.0-beta", "1.0.0-beta.2"),
        ("1.0.0-beta.2", "1.0.0-beta.11"),
        ("1.0.0-beta.11", "1.0.0-rc.1"),
        ("1.0.0-rc.1", "1.0.0"),
    ],
)
def test_should_get_less(left, right):
    assert compare(left, right) == -1


@pytest.mark.parametrize(
    "left,right",
    [
        ("2.0.0", "1.0.0"),
        ("1.0.0-alpha.1", "1.0.0-alpha"),
        ("1.0.0-alpha.beta", "1.0.0-alpha.1"),
        ("1.0.0-beta", "1.0.0-alpha.beta"),
        ("1.0.0-beta.2", "1.0.0-beta"),
        ("1.0.0-beta.11", "1.0.0-beta.2"),
        ("1.0.0-rc.1", "1.0.0-beta.11"),
        ("1.0.0", "1.0.0-rc.1"),
    ],
)
def test_should_get_greater(left, right):
    assert compare(left, right) == 1


@pytest.mark.parametrize(
    "left,right", [("foo", "bar"), ("1.0", "1.0.0"), ("1.x", "1.0.0")]
)
def test_should_raise_value_error_for_invalid_value(left, right):
    with pytest.raises(ValueError):
        compare(left, right)


def test_should_follow_specification_comparison():
    """
    produce comparison chain:
    1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-beta.2 < 1.0.0-beta.11
    < 1.0.0-rc.1 < 1.0.0-rc.1+build.1 < 1.0.0 < 1.0.0+0.3.7 < 1.3.7+build
    < 1.3.7+build.2.b8f12d7 < 1.3.7+build.11.e0f985a
    and in backward too.
    """
    chain = [
        "1.0.0-alpha",
        "1.0.0-alpha.1",
        "1.0.0-beta.2",
        "1.0.0-beta.11",
        "1.0.0-rc.1",
        "1.0.0",
        "1.3.7+build",
    ]
    versions = zip(chain[:-1], chain[1:])
    for low_version, high_version in versions:
        assert (
            compare(low_version, high_version) == -1
        ), "%s should be lesser than %s" % (low_version, high_version)
        assert (
            compare(high_version, low_version) == 1
        ), "%s should be higher than %s" % (high_version, low_version)


@pytest.mark.parametrize("left,right", [("1.0.0-beta.2", "1.0.0-beta.11")])
def test_should_compare_rc_builds(left, right):
    assert compare(left, right) == -1


@pytest.mark.parametrize(
    "left,right", [("1.0.0-rc.1", "1.0.0"), ("1.0.0-rc.1+build.1", "1.0.0")]
)
def test_should_compare_release_candidate_with_release(left, right):
    assert compare(left, right) == -1


@pytest.mark.parametrize(
    "left,right",
    [
        ("2.0.0", "2.0.0"),
        ("1.1.9-rc.1", "1.1.9-rc.1"),
        ("1.1.9+build.1", "1.1.9+build.1"),
        ("1.1.9-rc.1+build.1", "1.1.9-rc.1+build.1"),
    ],
)
def test_should_say_equal_versions_are_equal(left, right):
    assert compare(left, right) == 0


@pytest.mark.parametrize(
    "left,right,expected",
    [("1.1.9-rc.1", "1.1.9-rc.1+build.1", 0), ("1.1.9-rc.1", "1.1.9+build.1", -1)],
)
def test_should_compare_versions_with_build_and_release(left, right, expected):
    assert compare(left, right) == expected


@pytest.mark.parametrize(
    "left,right,expected",
    [
        ("1.0.0+build.1", "1.0.0", 0),
        ("1.0.0-alpha.1+build.1", "1.0.0-alpha.1", 0),
        ("1.0.0+build.1", "1.0.0-alpha.1", 1),
        ("1.0.0+build.1", "1.0.0-alpha.1+build.1", 1),
    ],
)
def test_should_ignore_builds_on_compare(left, right, expected):
    assert compare(left, right) == expected


def test_should_get_more_rc1():
    assert compare("1.0.0-rc1", "1.0.0-rc0") == 1


def test_should_compare_prerelease_with_numbers_and_letters():
    v1 = Version(major=1, minor=9, patch=1, prerelease="1unms", build=None)
    v2 = Version(major=1, minor=9, patch=1, prerelease=None, build="1asd")
    assert v1 < v2
    assert compare("1.9.1-1unms", "1.9.1+1") == -1


def test_should_compare_version_info_objects():
    v1 = Version(major=0, minor=10, patch=4)
    v2 = Version(major=0, minor=10, patch=4, prerelease="beta.1", build=None)

    # use `not` to enforce using comparision operators
    assert v1 != v2
    assert v1 > v2
    assert v1 >= v2
    assert not (v1 < v2)
    assert not (v1 <= v2)
    assert not (v1 == v2)

    v3 = Version(major=0, minor=10, patch=4)

    assert not (v1 != v3)
    assert not (v1 > v3)
    assert v1 >= v3
    assert not (v1 < v3)
    assert v1 <= v3
    assert v1 == v3

    v4 = Version(major=0, minor=10, patch=5)
    assert v1 != v4
    assert not (v1 > v4)
    assert not (v1 >= v4)
    assert v1 < v4
    assert v1 <= v4
    assert not (v1 == v4)


def test_should_compare_version_dictionaries():
    v1 = Version(major=0, minor=10, patch=4)
    v2 = dict(major=0, minor=10, patch=4, prerelease="beta.1", build=None)

    assert v1 != v2
    assert v1 > v2
    assert v1 >= v2
    assert not (v1 < v2)
    assert not (v1 <= v2)
    assert not (v1 == v2)

    v3 = dict(major=0, minor=10, patch=4)

    assert not (v1 != v3)
    assert not (v1 > v3)
    assert v1 >= v3
    assert not (v1 < v3)
    assert v1 <= v3
    assert v1 == v3

    v4 = dict(major=0, minor=10, patch=5)
    assert v1 != v4
    assert not (v1 > v4)
    assert not (v1 >= v4)
    assert v1 < v4
    assert v1 <= v4
    assert not (v1 == v4)


@pytest.mark.parametrize(
    "t",  # fmt: off
    (
        (1, 0, 0),
        (1, 0),
        (1,),
        (1, 0, 0, "pre.2"),
        (1, 0, 0, "pre.2", "build.4"),
    ),  # fmt: on
)
def test_should_compare_version_tuples(t):
    v0 = Version(major=0, minor=4, patch=5, prerelease="pre.2", build="build.4")
    v1 = Version(major=3, minor=4, patch=5, prerelease="pre.2", build="build.4")

    assert v0 < t
    assert v0 <= t
    assert v0 != t
    assert not v0 == t
    assert v1 > t
    assert v1 >= t
    # Symmetric
    assert t > v0
    assert t >= v0
    assert t < v1
    assert t <= v1
    assert t != v0
    assert not t == v0


@pytest.mark.parametrize(
    "lst",  # fmt: off
    (
        [1, 0, 0],
        [1, 0],
        [1],
        [1, 0, 0, "pre.2"],
        [1, 0, 0, "pre.2", "build.4"],
    ),  # fmt: on
)
def test_should_compare_version_list(lst):
    v0 = Version(major=0, minor=4, patch=5, prerelease="pre.2", build="build.4")
    v1 = Version(major=3, minor=4, patch=5, prerelease="pre.2", build="build.4")

    assert v0 < lst
    assert v0 <= lst
    assert v0 != lst
    assert not v0 == lst
    assert v1 > lst
    assert v1 >= lst
    # Symmetric
    assert lst > v0
    assert lst >= v0
    assert lst < v1
    assert lst <= v1
    assert lst != v0
    assert not lst == v0


@pytest.mark.parametrize(
    "s",  # fmt: off
    (
        "1.0.0",
        # "1.0",
        # "1",
        "1.0.0-pre.2",
        "1.0.0-pre.2+build.4",
    ),  # fmt: on
)
def test_should_compare_version_string(s):
    v0 = Version(major=0, minor=4, patch=5, prerelease="pre.2", build="build.4")
    v1 = Version(major=3, minor=4, patch=5, prerelease="pre.2", build="build.4")

    assert v0 < s
    assert v0 <= s
    assert v0 != s
    assert not v0 == s
    assert v1 > s
    assert v1 >= s
    # Symmetric
    assert s > v0
    assert s >= v0
    assert s < v1
    assert s <= v1
    assert s != v0
    assert not s == v0


@pytest.mark.parametrize("s", ("1", "1.0", "1.0.x"))
def test_should_not_allow_to_compare_invalid_versionstring(s):
    v = Version(major=3, minor=4, patch=5, prerelease="pre.2", build="build.4")
    with pytest.raises(ValueError):
        v < s
    with pytest.raises(ValueError):
        s > v


def test_should_not_allow_to_compare_version_with_int():
    v1 = Version(major=3, minor=4, patch=5, prerelease="pre.2", build="build.4")
    with pytest.raises(TypeError):
        v1 > 1
    with pytest.raises(TypeError):
        1 > v1
    with pytest.raises(TypeError):
        semver.compare(1)


def test_should_compare_prerelease_and_build_with_numbers():
    assert Version(major=1, minor=9, patch=1, prerelease=1, build=1) < Version(
        major=1, minor=9, patch=1, prerelease=2, build=1
    )
    assert Version(1, 9, 1, 1, 1) < Version(1, 9, 1, 2, 1)
    assert Version("2") < Version(10)
    assert Version("2") < Version("10")
