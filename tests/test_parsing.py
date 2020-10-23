import pytest

from semver import Version, parse, parse_version_info


@pytest.mark.parametrize(
    "version,expected",
    [
        # no. 1
        (
            "1.2.3-alpha.1.2+build.11.e0f985a",
            {
                "major": 1,
                "minor": 2,
                "patch": 3,
                "prerelease": "alpha.1.2",
                "build": "build.11.e0f985a",
            },
        ),
        # no. 2
        (
            "1.2.3-alpha-1+build.11.e0f985a",
            {
                "major": 1,
                "minor": 2,
                "patch": 3,
                "prerelease": "alpha-1",
                "build": "build.11.e0f985a",
            },
        ),
        (
            "0.1.0-0f",
            {"major": 0, "minor": 1, "patch": 0, "prerelease": "0f", "build": None},
        ),
        (
            "0.0.0-0foo.1",
            {"major": 0, "minor": 0, "patch": 0, "prerelease": "0foo.1", "build": None},
        ),
        (
            "0.0.0-0foo.1+build.1",
            {
                "major": 0,
                "minor": 0,
                "patch": 0,
                "prerelease": "0foo.1",
                "build": "build.1",
            },
        ),
    ],
)
def test_should_parse_version(version, expected):
    result = parse(version)
    assert result == expected


def test_parse_version_info_str_hash():
    s_version = "1.2.3-alpha.1.2+build.11.e0f985a"
    v = parse_version_info(s_version)
    assert v.__str__() == s_version
    d = {}
    d[v] = ""  # to ensure that Version are hashable


@pytest.mark.parametrize(
    "version,expected",
    [
        # no. 1
        (
            "1.2.3-rc.0+build.0",
            {
                "major": 1,
                "minor": 2,
                "patch": 3,
                "prerelease": "rc.0",
                "build": "build.0",
            },
        ),
        # no. 2
        (
            "1.2.3-rc.0.0+build.0",
            {
                "major": 1,
                "minor": 2,
                "patch": 3,
                "prerelease": "rc.0.0",
                "build": "build.0",
            },
        ),
    ],
)
def test_should_parse_zero_prerelease(version, expected):
    result = parse(version)
    assert result == expected


@pytest.mark.parametrize("version", ["01.2.3", "1.02.3", "1.2.03"])
def test_should_raise_value_error_for_zero_prefixed_versions(version):
    with pytest.raises(ValueError):
        parse(version)


def test_equal_versions_have_equal_hashes():
    v1 = parse_version_info("1.2.3-alpha.1.2+build.11.e0f985a")
    v2 = parse_version_info("1.2.3-alpha.1.2+build.22.a589f0e")
    assert v1 == v2
    assert hash(v1) == hash(v2)
    d = {}
    d[v1] = 1
    d[v2] = 2
    assert d[v1] == 2
    s = set()
    s.add(v1)
    assert v2 in s


def test_parse_method_for_version_info():
    s_version = "1.2.3-alpha.1.2+build.11.e0f985a"
    v = Version.parse(s_version)
    assert str(v) == s_version


def test_next_version_with_invalid_parts():
    version = Version.parse("1.0.1")
    with pytest.raises(ValueError):
        version.next_version("invalid")


@pytest.mark.parametrize(
    "version, part, expected",
    [
        # major
        ("1.0.4-rc.1", "major", "2.0.0"),
        ("1.1.0-rc.1", "major", "2.0.0"),
        ("1.1.4-rc.1", "major", "2.0.0"),
        ("1.2.3", "major", "2.0.0"),
        ("1.0.0-rc.1", "major", "1.0.0"),
        # minor
        ("0.2.0-rc.1", "minor", "0.2.0"),
        ("0.2.5-rc.1", "minor", "0.3.0"),
        ("1.3.1", "minor", "1.4.0"),
        # patch
        ("1.3.2", "patch", "1.3.3"),
        ("0.1.5-rc.2", "patch", "0.1.5"),
        # prerelease
        ("0.1.4", "prerelease", "0.1.5-rc.1"),
        ("0.1.5-rc.1", "prerelease", "0.1.5-rc.2"),
        # special cases
        ("0.2.0-rc.1", "patch", "0.2.0"),  # same as "minor"
        ("1.0.0-rc.1", "patch", "1.0.0"),  # same as "major"
        ("1.0.0-rc.1", "minor", "1.0.0"),  # same as "major"
    ],
)
def test_next_version_with_versioninfo(version, part, expected):
    ver = Version.parse(version)
    next_version = ver.next_version(part)
    assert isinstance(next_version, Version)
    assert str(next_version) == expected
