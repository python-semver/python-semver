import pytest

from semver import Version, finalize_version, format_version


@pytest.mark.parametrize(
    "version,expected",
    [
        ("1.2.3", "1.2.3"),
        ("1.2.3-rc.5", "1.2.3"),
        ("1.2.3+build.2", "1.2.3"),
        ("1.2.3-rc.1+build.5", "1.2.3"),
        ("1.2.3-alpha", "1.2.3"),
        ("1.2.0", "1.2.0"),
    ],
)
def test_should_finalize_version(version, expected):
    assert finalize_version(version) == expected


def test_should_correctly_format_version():
    assert format_version(3, 4, 5) == "3.4.5"
    assert format_version(3, 4, 5, "rc.1") == "3.4.5-rc.1"
    assert format_version(3, 4, 5, prerelease="rc.1") == "3.4.5-rc.1"
    assert format_version(3, 4, 5, build="build.4") == "3.4.5+build.4"
    assert format_version(3, 4, 5, "rc.1", "build.4") == "3.4.5-rc.1+build.4"


def test_parse_method_for_version_info():
    s_version = "1.2.3-alpha.1.2+build.11.e0f985a"
    v = Version.parse(s_version)
    assert str(v) == s_version


@pytest.mark.parametrize(
    "version, expected",
    [
        (
            Version(major=1, minor=2, patch=3, prerelease=None, build=None),
            "Version(major=1, minor=2, patch=3, prerelease=None, build=None)",
        ),
        (
            Version(major=1, minor=2, patch=3, prerelease="r.1", build=None),
            "Version(major=1, minor=2, patch=3, prerelease='r.1', build=None)",
        ),
        (
            Version(major=1, minor=2, patch=3, prerelease="dev.1", build=None),
            "Version(major=1, minor=2, patch=3, prerelease='dev.1', build=None)",
        ),
        (
            Version(major=1, minor=2, patch=3, prerelease="dev.1", build="b.1"),
            "Version(major=1, minor=2, patch=3, prerelease='dev.1', build='b.1')",
        ),
        (
            Version(major=1, minor=2, patch=3, prerelease="r.1", build="b.1"),
            "Version(major=1, minor=2, patch=3, prerelease='r.1', build='b.1')",
        ),
        (
            Version(major=1, minor=2, patch=3, prerelease="r.1", build="build.1"),
            "Version(major=1, minor=2, patch=3, prerelease='r.1', build='build.1')",
        ),
    ],
)
def test_repr(version, expected):
    assert repr(version) == expected
