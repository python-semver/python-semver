"""Legacy prerelease counters must not make next_version move backwards."""

import pytest

from semver import Version


@pytest.mark.parametrize(
    "current,token,expected",
    [
        ("1.2.3-rc9", "rc", "1.2.4-rc10"),
        ("1.2.3-rc99", "rc", "1.2.4-rc100"),
        ("1.2.3-rc999+build.7", "rc", "1.2.4-rc1000"),
        ("1.2.3-beta9", "beta", "1.2.4-beta10"),
        ("1.2.3-alpha.beta9", "alpha.beta", "1.2.4-alpha.beta10"),
        ("1.2.3-0rc9", "0rc", "1.2.4-0rc10"),
        ("0.0.0-rc9", "rc", "0.0.1-rc10"),
        ("1.2.3-rc8", "rc", "1.2.3-rc9"),
        ("1.2.3-rc98", "rc", "1.2.3-rc99"),
        ("1.2.3-rc099", "rc", "1.2.3-rc100"),
        ("1.2.3-rc09", "rc", "1.2.3-rc10"),
        ("1.2.3-rc.9", "rc", "1.2.3-rc.10"),
    ],
)
def test_next_legacy_counter_preserves_order(current, token, expected):
    original = Version.parse(current)
    result = original.next_version("prerelease", token)
    assert str(result) == expected
    assert result > original
    assert result.build is None
    assert Version.parse(str(result)).to_tuple() == result.to_tuple()
    assert str(original) == current


def test_repeated_legacy_bumps_preserve_order_and_subclass():
    class Release(Version):
        pass

    current = Release.parse("1.2.3-rc8+build.7")
    for expected in ("1.2.3-rc9", "1.2.4-rc10", "1.2.4-rc11"):
        result = current.next_version("prerelease")
        assert isinstance(result, Release)
        assert str(result) == expected
        assert result > current
        assert result.build is None
        current = result
