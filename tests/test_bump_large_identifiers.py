import pytest

from semver import Version


@pytest.mark.parametrize(
    "number,expected",
    [
        ("1" * 5000, "1" * 4999 + "2"),
        ("9" * 5000, "1" + "0" * 5000),
        ("1" + "9" * 4999, "2" + "0" * 4999),
    ],
    ids=["no-carry", "new-digit", "carry"],
)
@pytest.mark.parametrize("part", ["prerelease", "build", "old-style-prerelease"])
def test_bump_large_numeric_identifier(number, expected, part):
    if part == "build":
        original = "1.2.3-rc.1+build." + number + ".tail"
        version = Version.parse(original)
        result = version.bump_build()
        expected_version = "1.2.3-rc.1+build." + expected + ".tail"
    elif part == "old-style-prerelease":
        original = "1.2.3-rc" + number + "+build.1"
        version = Version.parse(original)
        result = version.next_version("prerelease", "rc")
        expected_version = "1.2.3-rc" + expected
    else:
        original = "1.2.3-rc." + number + "+build.1"
        version = Version.parse(original)
        result = version.bump_prerelease()
        expected_version = "1.2.3-rc." + expected

    assert str(result) == expected_version
    assert Version.is_valid(str(result))
    assert str(version) == original


def test_bump_preserves_constructor_unicode_digit_behavior():
    version = Version(1, 2, 3, prerelease="rc.\u0660\u0660\u0669")
    assert version.bump_prerelease().prerelease == "rc.10"

    version = Version(1, 2, 3, build="build.\u0660\u0660\u0669")
    assert version.bump_build().build == "build.\u066010"

    version = Version(1, 2, 3, prerelease="rc\u0660\u0660\u0669")
    assert version.next_version("prerelease", "rc").prerelease == "rc10"
