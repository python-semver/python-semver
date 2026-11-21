import sys

import pytest

from semver import Version


def test_bump_prerelease_with_long_numeric_identifier():
    identifier = "9" * 5000
    version = f"1.2.3-rc.{identifier}"

    assert Version.is_valid(version)
    assert str(Version.parse(version).bump_prerelease()) == f"1.2.3-rc.1{'0' * 5000}"


def test_bump_build_with_long_numeric_identifier():
    identifier = "9" * 5000
    version = f"1.2.3+build.{identifier}"

    assert Version.is_valid(version)
    assert str(Version.parse(version).bump_build()) == f"1.2.3+build.1{'0' * 5000}"


def test_bump_build_preserves_leading_zeroes_when_carrying():
    version = Version.parse("1.2.3+build.0099")

    assert str(version.bump_build()) == "1.2.3+build.0100"


@pytest.mark.parametrize(
    "prerelease, expected",
    [("0009", "10"), ("rc.0099", "rc.100"), ("rc.0000", "rc.1")],
)
def test_bump_prerelease_normalizes_constructor_leading_zeroes(prerelease, expected):
    version = Version(1, 2, 3, prerelease=prerelease)

    assert version.bump_prerelease().prerelease == expected
    assert version.prerelease == prerelease


@pytest.mark.parametrize(
    "part, identifier, expected",
    [
        ("prerelease", "rc.\u0660\u0660\u0669\u0669", "rc.100"),
        ("build", "build.\u0660\u0660\u0669\u0669", "build.\u0660100"),
    ],
)
def test_bump_preserves_constructor_unicode_digit_behavior(part, identifier, expected):
    version = Version(1, 2, 3, **{part: identifier})

    assert getattr(getattr(version, f"bump_{part}")(), part) == expected


@pytest.mark.parametrize("part", ["prerelease", "build"])
def test_bump_long_identifier_without_carry_does_not_change_int_limit(part):
    identifier = "1" + "0" * 4999
    version = Version.parse(f"1.2.3{'-' if part == 'prerelease' else '+'}{identifier}")
    original_limit = (
        sys.get_int_max_str_digits() if hasattr(sys, "get_int_max_str_digits") else None
    )

    bumped = getattr(version, f"bump_{part}")()

    assert getattr(bumped, part) == "1" + "0" * 4998 + "1"
    assert Version.is_valid(str(bumped))
    assert getattr(version, part) == identifier
    if original_limit is not None:
        assert sys.get_int_max_str_digits() == original_limit


def test_bump_long_build_preserves_all_leading_zeroes():
    identifier = "0" * 5000
    version = Version.parse(f"1.2.3+{identifier}")

    assert version.bump_build().build == "0" * 4999 + "1"
