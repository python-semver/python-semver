import pytest

from semver import Version, replace


@pytest.mark.parametrize(
    "version,parts,expected",
    [
        ("3.4.5", dict(major=2), "2.4.5"),
        ("3.4.5", dict(major="2"), "2.4.5"),
        ("3.4.5", dict(major=2, minor=5), "2.5.5"),
        ("3.4.5", dict(minor=2), "3.2.5"),
        ("3.4.5", dict(major=2, minor=5, patch=10), "2.5.10"),
        ("3.4.5", dict(major=2, minor=5, patch=10, prerelease="rc1"), "2.5.10-rc1"),
        (
            "3.4.5",
            dict(major=2, minor=5, patch=10, prerelease="rc1", build="b1"),
            "2.5.10-rc1+b1",
        ),
        ("3.4.5-alpha.1.2", dict(major=2), "2.4.5-alpha.1.2"),
        ("3.4.5-alpha.1.2", dict(build="x1"), "3.4.5-alpha.1.2+x1"),
        ("3.4.5+build1", dict(major=2), "2.4.5+build1"),
    ],
)
def test_replace_method_replaces_requested_parts(version, parts, expected):
    assert replace(version, **parts) == expected


def test_replace_raises_TypeError_for_invalid_keyword_arg():
    with pytest.raises(TypeError, match=r"replace\(\).*unknown.*"):
        assert replace("1.2.3", unknown="should_raise")


@pytest.mark.parametrize(
    "version,parts,expected",
    [
        ("3.4.5", dict(major=2, minor=5), "2.5.5"),
        ("3.4.5", dict(major=2, minor=5, patch=10), "2.5.10"),
        ("3.4.5-alpha.1.2", dict(major=2), "2.4.5-alpha.1.2"),
        ("3.4.5-alpha.1.2", dict(build="x1"), "3.4.5-alpha.1.2+x1"),
        ("3.4.5+build1", dict(major=2), "2.4.5+build1"),
    ],
)
def test_should_return_versioninfo_with_replaced_parts(version, parts, expected):
    assert Version.parse(version).replace(**parts) == Version.parse(expected)


def test_replace_raises_ValueError_for_non_numeric_values():
    with pytest.raises(ValueError):
        Version.parse("1.2.3").replace(major="x")
