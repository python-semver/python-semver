import pytest

from semver import (
    Version,
    bump_build,
    bump_major,
    bump_minor,
    bump_patch,
    bump_prerelease,
    compare,
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
    assert v.compare(expected) == -1


def test_should_versioninfo_bump_patch_and_prerelease():
    v = parse_version_info("3.4.5-rc.1")
    expected = parse_version_info("3.4.6-rc.1")
    assert v.bump_patch().bump_prerelease() == expected
    assert v.compare(expected) == -1


def test_should_versioninfo_bump_patch_and_prerelease_with_token():
    v = parse_version_info("3.4.5-dev.1")
    expected = parse_version_info("3.4.6-dev.1")
    assert v.bump_patch().bump_prerelease("dev") == expected
    assert v.compare(expected) == -1


def test_should_versioninfo_bump_prerelease_and_build():
    v = parse_version_info("3.4.5-rc.1+build.1")
    expected = parse_version_info("3.4.5-rc.2+build.2")
    assert v.bump_prerelease().bump_build() == expected
    assert v.compare(expected) == -1


def test_should_versioninfo_bump_prerelease_and_build_with_token():
    v = parse_version_info("3.4.5-rc.1+b.1")
    expected = parse_version_info("3.4.5-rc.2+b.2")
    assert v.bump_prerelease().bump_build("b") == expected
    assert v.compare(expected) == -1


def test_should_versioninfo_bump_multiple():
    v = parse_version_info("3.4.5-rc.1+build.1")
    expected = parse_version_info("3.4.5-rc.2+build.2")
    assert v.bump_prerelease().bump_build().bump_build() == expected
    assert v.compare(expected) == -1
    expected = parse_version_info("3.4.5-rc.3")
    assert v.bump_prerelease().bump_build().bump_build().bump_prerelease() == expected
    assert v.compare(expected) == -1


def test_should_versioninfo_bump_prerelease_with_empty_str():
    v = parse_version_info("3.4.5")
    expected = parse_version_info("3.4.5-1")
    assert v.bump_prerelease("") == expected
    assert v.compare(expected) == 1


def test_should_versioninfo_bump_prerelease_with_none():
    v = parse_version_info("3.4.5")
    expected = parse_version_info("3.4.5-rc.1")
    assert v.bump_prerelease(None) == expected
    assert v.compare(expected) == 1


def test_should_versioninfo_bump_prerelease_nonnumeric():
    v = parse_version_info("3.4.5-rc1")
    expected = parse_version_info("3.4.5-rc1.0")
    assert v.bump_prerelease(None) == expected
    assert v.compare(expected) == -1


def test_should_versioninfo_bump_prerelease_nonnumeric_nine():
    v = parse_version_info("3.4.5-rc9")
    expected = parse_version_info("3.4.5-rc9.0")
    assert v.bump_prerelease(None) == expected
    assert v.compare(expected) == -1


def test_should_versioninfo_bump_prerelease_bump_patch():
    v = parse_version_info("3.4.5")
    expected = parse_version_info("3.4.6-rc.1")
    assert v.bump_prerelease(bump_when_empty=True) == expected
    assert v.compare(expected) == -1


def test_should_versioninfo_bump_patch_and_prerelease_bump_patch():
    v = parse_version_info("3.4.5")
    expected = parse_version_info("3.4.7-rc.1")
    assert v.bump_patch().bump_prerelease(bump_when_empty=True) == expected
    assert v.compare(expected) == -1


def test_should_versioninfo_bump_build_with_empty_str():
    v = parse_version_info("3.4.5")
    expected = parse_version_info("3.4.5+1")
    assert v.bump_build("") == expected
    assert v.compare(expected) == 0


def test_should_versioninfo_bump_build_with_none():
    v = parse_version_info("3.4.5")
    expected = parse_version_info("3.4.5+build.1")
    assert v.bump_build(None) == expected
    assert v.compare(expected) == 0


def test_should_ignore_extensions_for_bump():
    assert bump_patch("3.4.5-rc1+build4") == "3.4.6"


@pytest.mark.parametrize(
    "version,token,expected,expected_compare",
    [
        ("3.4.5-rc.9", None, "3.4.5-rc.10", -1),
        ("3.4.5", None, "3.4.5-rc.1", 1),
        ("3.4.5", "dev", "3.4.5-dev.1", 1),
        ("3.4.5", "", "3.4.5-rc.1", 1),
    ],
)
def test_should_bump_prerelease(version, token, expected, expected_compare):
    token = "rc" if not token else token
    assert bump_prerelease(version, token) == expected
    assert compare(version, expected) == expected_compare

def test_should_ignore_build_on_prerelease_bump():
    assert bump_prerelease("3.4.5-rc.1+build.4") == "3.4.5-rc.2"


@pytest.mark.parametrize(
    "version,token,expected",
    [
        ("1.2.3-alpha.beta.1+build.7", "alpha.beta", "1.2.3-alpha.beta.2"),
        ("1.2.3-alpha.beta.gamma.1", "alpha", "1.2.3-alpha.beta.gamma.2"),
        ("1.2.3-rc3", "rc", "1.2.3-rc4"),
        ("1.2.3-rc.3", "rc", "1.2.3-rc.4"),
        ("1.2.3-alphaXbeta9", "alpha.beta", "1.2.3-alpha.beta.1"),
    ],
)
def test_next_version_matches_literal_prerelease_token_family(
    version, token, expected
):
    original = Version.parse(version)
    result = original.next_version("prerelease", token)
    assert str(result) == expected
    assert Version.parse(str(result)).to_tuple() == result.to_tuple()
    assert str(original) == version


@pytest.mark.parametrize(
    "token", ["[", "rc.", "rc+build", "rc..next", "rc.01", "01", "ré"]
)
def test_next_version_rejects_invalid_prerelease_token(token):
    with pytest.raises(ValueError):
        Version.parse("1.2.3-rc.1").next_version("prerelease", token)


@pytest.mark.parametrize("token", [None, ""])
def test_next_version_preserves_empty_token_semantics(token):
    version = Version.parse("1.2.3-alpha.beta.1")
    assert str(version.next_version("prerelease", token)) == "1.2.3-alpha.beta.2"


@pytest.mark.parametrize(
    "part,token,expected",
    [
        ("major", "rc.", "2.0.0"),
        ("minor", "rc+build", "1.3.0"),
        ("patch", "rc..next", "1.2.4"),
    ],
)
def test_next_version_ignores_token_for_main_parts(part, token, expected):
    assert str(Version.parse("1.2.3").next_version(part, token)) == expected


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
    assert compare(version, expected) == 0
