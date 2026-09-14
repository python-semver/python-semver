"""Regression tests: invalid bump tokens must be rejected.

:meth:`Version.bump_prerelease` and :meth:`Version.bump_build` accepted any
string as ``token`` and concatenated it into the resulting version, producing
a :class:`Version` whose string representation is not valid SemVer (it cannot
be round-tripped through :meth:`Version.parse`). These tests verify that
malformed tokens raise :class:`ValueError` instead.
"""

import pytest

from semver import Version


@pytest.mark.parametrize(
    "token",
    [
        "bu/ild",
        "build+meta",
        "bu ild",
        "build.",
        ".build",
        "build..2",
    ],
)
def test_bump_build_rejects_invalid_token(token):
    """bump_build must reject tokens that are not valid build identifiers."""
    version = Version.parse("1.0.0")
    with pytest.raises(ValueError):
        version.bump_build(token)


@pytest.mark.parametrize(
    "token",
    [
        "rc+build",
        "rc/",
        "rc.",
        ".rc",
        "rc..2",
    ],
)
def test_bump_prerelease_rejects_invalid_token(token):
    """bump_prerelease must reject tokens that are not valid prerelease identifiers."""
    version = Version.parse("1.0.0")
    with pytest.raises(ValueError):
        version.bump_prerelease(token)


def test_bump_prerelease_rejects_numeric_leading_zero_segment():
    """A numeric prerelease token segment must not contain leading zeros."""
    version = Version.parse("1.0.0")
    with pytest.raises(ValueError):
        version.bump_prerelease("rc.05")


@pytest.mark.parametrize(
    "token,expected",
    [
        ("build", "1.0.0+build.1"),
        ("b", "1.0.0+b.1"),
        ("build.2", "1.0.0+build.2.1"),
        ("dev-1", "1.0.0+dev-1.1"),
    ],
)
def test_bump_build_still_accepts_valid_tokens(token, expected):
    """Valid build tokens must keep working (documents unchanged behavior)."""
    assert str(Version.parse("1.0.0").bump_build(token)) == expected


@pytest.mark.parametrize(
    "token,expected",
    [
        ("rc", "1.0.0-rc.1"),
        ("rc.1", "1.0.0-rc.1.1"),
        ("dev-1", "1.0.0-dev-1.1"),
        ("alpha.0", "1.0.0-alpha.0.1"),
    ],
)
def test_bump_prerelease_still_accepts_valid_tokens(token, expected):
    """Valid prerelease tokens must keep working (documents unchanged behavior)."""
    assert str(Version.parse("1.0.0").bump_prerelease(token)) == expected


@pytest.mark.parametrize(
    "token, expected_prerelease, expected_build",
    [
        ("", "1.0.0-1", "1.0.0+1"),
        (None, "1.0.0-rc.1", "1.0.0+build.1"),
    ],
    ids=["empty-string", "none"],
)
def test_bump_methods_still_accept_empty_and_none(
    token, expected_prerelease, expected_build
):
    """Empty string and None are documented and must keep their meaning."""
    assert str(Version.parse("1.0.0").bump_prerelease(token)) == expected_prerelease
    assert str(Version.parse("1.0.0").bump_build(token)) == expected_build
