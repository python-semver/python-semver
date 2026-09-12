import pytest

from semver import Version


@pytest.mark.parametrize(
    "version",
    [
        "1.2.3\n",
        "1.2.3-rc.1\n",
        "1.2.3+build.1\n",
        "1\u0662.2.3",
        "1.2\u0663.3",
        "1.2.3\u0664",
        "1.2.3-1\u0662",
        "1.2.3-\u0661alpha",
    ],
)
@pytest.mark.parametrize("optional_minor_and_patch", [False, True])
def test_parse_rejects_non_semver_characters(version, optional_minor_and_patch):
    with pytest.raises(ValueError):
        Version.parse(version, optional_minor_and_patch=optional_minor_and_patch)


@pytest.mark.parametrize("version", ["1\n", "1.2\n", "1\u0662", "1.2\u0663"])
def test_optional_parse_rejects_non_semver_characters(version):
    with pytest.raises(ValueError):
        Version.parse(version, optional_minor_and_patch=True)


@pytest.mark.parametrize("version", ["1.2.3\n", "1\u0662.2.3", "1.2.3-\u0661alpha"])
def test_is_valid_rejects_non_semver_characters(version):
    assert not Version.is_valid(version)
