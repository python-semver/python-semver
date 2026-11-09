import pytest

from semver import Version


@pytest.mark.parametrize(
    "version, index, expected",
    [
        # Simple positive indices
        ("1.2.3-rc.0+build.0", 0, 1),
        ("1.2.3-rc.0+build.0", 1, 2),
        ("1.2.3-rc.0+build.0", 2, 3),
        ("1.2.3-rc.0+build.0", 3, "rc.0"),
        ("1.2.3-rc.0+build.0", 4, "build.0"),
        ("1.2.3-rc.0", 0, 1),
        ("1.2.3-rc.0", 1, 2),
        ("1.2.3-rc.0", 2, 3),
        ("1.2.3-rc.0", 3, "rc.0"),
        ("1.2.3", 0, 1),
        ("1.2.3", 1, 2),
        ("1.2.3", 2, 3),
        # Special cases
        ("1.0.2", 1, 0),
    ],
)
def test_version_info_should_be_accessed_with_index(version, index, expected):
    version_info = Version.parse(version)
    assert version_info[index] == expected


@pytest.mark.parametrize(
    "version, slice_object, expected",
    [
        # Slice indices
        ("1.2.3-rc.0+build.0", slice(0, 5), (1, 2, 3, "rc.0", "build.0")),
        ("1.2.3-rc.0+build.0", slice(0, 4), (1, 2, 3, "rc.0")),
        ("1.2.3-rc.0+build.0", slice(0, 3), (1, 2, 3)),
        ("1.2.3-rc.0+build.0", slice(0, 2), (1, 2)),
        ("1.2.3-rc.0+build.0", slice(3, 5), ("rc.0", "build.0")),
        ("1.2.3-rc.0", slice(0, 4), (1, 2, 3, "rc.0")),
        ("1.2.3-rc.0", slice(0, 3), (1, 2, 3)),
        ("1.2.3-rc.0", slice(0, 2), (1, 2)),
        ("1.2.3", slice(0, 10), (1, 2, 3)),
        ("1.2.3", slice(0, 3), (1, 2, 3)),
        ("1.2.3", slice(0, 2), (1, 2)),
        # Special cases
        ("1.2.3-rc.0+build.0", slice(3), (1, 2, 3)),
        ("1.2.3-rc.0+build.0", slice(0, 5, 2), (1, 3, "build.0")),
        ("1.2.3-rc.0+build.0", slice(None, 5, 2), (1, 3, "build.0")),
        ("1.2.3-rc.0+build.0", slice(5, 0, -2), ("build.0", 3)),
        ("1.2.0-rc.0+build.0", slice(3), (1, 2, 0)),
    ],
)
def test_version_info_should_be_accessed_with_slice_object(
    version, slice_object, expected
):
    version_info = Version.parse(version)
    assert version_info[slice_object] == expected


@pytest.mark.parametrize(
    "version, index",
    [
        ("1.2.3", 3),
        ("1.2.3", slice(3, 4)),
        ("1.2.3", 4),
        ("1.2.3", slice(4, 5)),
        ("1.2.3", 5),
        ("1.2.3", slice(5, 6)),
        ("1.2.3-rc.0", 5),
        ("1.2.3-rc.0", slice(5, 6)),
        ("1.2.3-rc.0", 6),
        ("1.2.3-rc.0", slice(6, 7)),
    ],
)
def test_version_info_should_throw_index_error(version, index):
    version_info = Version.parse(version)
    with pytest.raises(IndexError, match=r"Version part undefined"):
        version_info[index]


@pytest.mark.parametrize(
    "version, index",
    [
        ("1.2.3", -1),
        ("1.2.3", -2),
        ("1.2.3", slice(-2, 2)),
        ("1.2.3", slice(2, -2)),
        ("1.2.3", slice(-2, -2)),
    ],
)
def test_version_info_should_throw_index_error_when_negative_index(version, index):
    version_info = Version.parse(version)
    with pytest.raises(IndexError, match=r"Version index cannot be negative"):
        version_info[index]


class Index:
    def __init__(self, value):
        self.value = value

    def __index__(self):
        return self.value


def test_version_accepts_index_protocol():
    version = Version.parse("1.2.3")
    assert version[Index(1)] == 2
    assert version[Index(0):Index(2)] == (1, 2)
    with pytest.raises(IndexError):
        version[Index(-1)]


@pytest.mark.parametrize("key", [None, "1", 1.0])
def test_invalid_version_index_type(key):
    with pytest.raises(TypeError):
        Version.parse("1.2.3")[key]
