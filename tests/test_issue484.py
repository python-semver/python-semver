"""Regression test for issue #484: next_version with old-style prereleases."""

import pytest

from semver import Version


@pytest.mark.parametrize(
    "current, token, expected",
    [
        ("1.2.3-rc.1", "alpha", "1.2.4-alpha.1"),
        ("1.2.3-beta.3", "alpha", "1.2.4-alpha.1"),
        ("1.2.3-rc.1+build.7", "dev", "1.2.4-dev.1"),
        ("1.2.3-rc3", "alpha", "1.2.4-alpha.1"),
        ("1.2.3-rc.1", "2", "1.2.4-2.1"),
        ("1.2.3-alpha.4", "rc", "1.2.3-rc.1"),
    ],
)
def test_token_switch_preserves_version_order(current, token, expected):
    original = Version.parse(current)
    result = original.next_version("prerelease", token)
    assert str(result) == expected
    assert result > original
    assert str(original) == current


def test_issue_484_rc3_to_rc4():
    """Old-style prerelease 'rc3' should bump to 'rc4', not reset to 'rc.1'."""
    v = Version.parse("0.1.2-rc3")
    assert str(v.next_version("prerelease")) == "0.1.2-rc4"


def test_issue_484_rc9_to_rc10():
    """Keep the legacy counter while ensuring digit rollover moves forward."""
    v = Version.parse("1.2.3-rc9")
    result = v.next_version("prerelease")
    assert str(result) == "1.2.4-rc10"
    assert result > v


def test_issue_484_dot_style_unchanged():
    """Dot-separated prereleases should still work as before."""
    v = Version.parse("0.1.2-rc.3")
    assert str(v.next_version("prerelease")) == "0.1.2-rc.4"


def test_issue_484_different_token():
    """A different prerelease token should still reset to rc.1."""
    v = Version.parse("1.2.3-alpha1")
    assert str(v.next_version("prerelease")) == "1.2.3-rc.1"


def test_issue_484_custom_token():
    """Custom prerelease token should be respected."""
    v = Version.parse("1.2.3-beta2")
    assert str(v.next_version("prerelease", "beta")) == "1.2.3-beta3"


def test_issue_484_old_style_drops_build():
    """Build metadata is dropped, as it is for dot-separated prereleases."""
    v = Version.parse("1.2.3-rc3+build.5")
    assert v.next_version("prerelease").build is None
