import pytest

from semver import (
    bump_build,
    bump_major,
    bump_minor,
    bump_patch,
    bump_prerelease,
    parse_version_info,
)


def test_should_bump_major():
    assert bump_major("3.4.5") == "4.0.0"


def test_should_bump_minor():
    assert bump_minor("3.4.5") == "3.5.0"


def test_should_bump_patch():
    assert bump_patch("3.4.5") == "3.4.6"


def test_should_versioninfo_bump_major_and_minor():
    v = parse_version_info("3.4.5")
    expected = parse_version_info("4.1.0")
    assert v.bump_major().bump_minor() == expected


def test_should_versioninfo_bump_minor_and_patch():
    v = parse_version_info("3.4.5")
    expected = parse_version_info("3.5.1")
    assert v.bump_minor().bump_patch() == expected


def test_should_versioninfo_bump_patch_and_prerelease():
    v = parse_version_info("3.4.5-rc.1")
    expected = parse_version_info("3.4.6-rc.1")
    assert v.bump_patch().bump_prerelease() == expected


def test_should_versioninfo_bump_patch_and_prerelease_with_token():
    v = parse_version_info("3.4.5-dev.1")
    expected = parse_version_info("3.4.6-dev.1")
    assert v.bump_patch().bump_prerelease("dev") == expected


def test_should_versioninfo_bump_prerelease_and_build():
    v = parse_version_info("3.4.5-rc.1+build.1")
    expected = parse_version_info("3.4.5-rc.2+build.2")
    assert v.bump_prerelease().bump_build() == expected


def test_should_versioninfo_bump_prerelease_and_build_with_token():
    v = parse_version_info("3.4.5-rc.1+b.1")
    expected = parse_version_info("3.4.5-rc.2+b.2")
    assert v.bump_prerelease().bump_build("b") == expected


def test_should_versioninfo_bump_multiple():
    v = parse_version_info("3.4.5-rc.1+build.1")
    expected = parse_version_info("3.4.5-rc.2+build.2")
    assert v.bump_prerelease().bump_build().bump_build() == expected
    expected = parse_version_info("3.4.5-rc.3")
    assert v.bump_prerelease().bump_build().bump_build().bump_prerelease() == expected


def test_should_ignore_extensions_for_bump():
    assert bump_patch("3.4.5-rc1+build4") == "3.4.6"


@pytest.mark.parametrize(
    "version,token,expected",
    [
        ("3.4.5-rc.9", None, "3.4.5-rc.10"),
        ("3.4.5", None, "3.4.5-rc.1"),
        ("3.4.5", "dev", "3.4.5-dev.1"),
        ("3.4.5", "", "3.4.5-rc.1"),
    ],
)
def test_should_bump_prerelease(version, token, expected):
    token = "rc" if not token else token
    assert bump_prerelease(version, token) == expected


def test_should_ignore_build_on_prerelease_bump():
    assert bump_prerelease("3.4.5-rc.1+build.4") == "3.4.5-rc.2"


@pytest.mark.parametrize(
    "version,expected",
    [
        ("3.4.5-rc.1+build.9", "3.4.5-rc.1+build.10"),
        ("3.4.5-rc.1+0009.dev", "3.4.5-rc.1+0010.dev"),
        ("3.4.5-rc.1", "3.4.5-rc.1+build.1"),
        ("3.4.5", "3.4.5+build.1"),
    ],
)
def test_should_bump_build(version, expected):
    assert bump_build(version) == expected
