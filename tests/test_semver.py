import pytest  # noqa

from semver import VersionInfo


@pytest.mark.parametrize(
    "string,expected", [("rc", "rc"), ("rc.1", "rc.2"), ("2x", "3x")]
)
def test_should_private_increment_string(string, expected):
    assert VersionInfo._increment_string(string) == expected


@pytest.mark.parametrize(
    "ver",
    [
        {"major": -1},
        {"major": 1, "minor": -2},
        {"major": 1, "minor": 2, "patch": -3},
        {"major": 1, "minor": -2, "patch": 3},
    ],
)
def test_should_not_allow_negative_numbers(ver):
    with pytest.raises(ValueError, match=".* is negative. .*"):
        VersionInfo(**ver)


def test_should_versioninfo_to_dict(version):
    resultdict = version.to_dict()
    assert isinstance(resultdict, dict), "Got type from to_dict"
    assert list(resultdict.keys()) == ["major", "minor", "patch", "prerelease", "build"]


def test_should_versioninfo_to_tuple(version):
    result = version.to_tuple()
    assert isinstance(result, tuple), "Got type from to_dict"
    assert len(result) == 5, "Different length from to_tuple()"


def test_version_info_should_be_iterable(version):
    assert tuple(version) == (
        version.major,
        version.minor,
        version.patch,
        version.prerelease,
        version.build,
    )


def test_should_be_able_to_use_strings_as_major_minor_patch():
    v = VersionInfo("1", "2", "3")
    assert isinstance(v.major, int)
    assert isinstance(v.minor, int)
    assert isinstance(v.patch, int)
    assert v.prerelease is None
    assert v.build is None
    assert VersionInfo("1", "2", "3") == VersionInfo(1, 2, 3)


def test_using_non_numeric_string_as_major_minor_patch_throws():
    with pytest.raises(ValueError):
        VersionInfo("a")
    with pytest.raises(ValueError):
        VersionInfo(1, "a")
    with pytest.raises(ValueError):
        VersionInfo(1, 2, "a")


def test_should_be_able_to_use_integers_as_prerelease_build():
    v = VersionInfo(1, 2, 3, 4, 5)
    assert isinstance(v.prerelease, str)
    assert isinstance(v.build, str)
    assert VersionInfo(1, 2, 3, 4, 5) == VersionInfo(1, 2, 3, "4", "5")


def test_should_versioninfo_isvalid():
    assert VersionInfo.isvalid("1.0.0") is True
    assert VersionInfo.isvalid("foo") is False
