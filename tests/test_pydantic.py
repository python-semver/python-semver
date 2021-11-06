import pytest
import pydantic

from semver import Version


class Schema(pydantic.BaseModel):
    """An example schema which contains a semver Version object"""

    name: str
    """ Other data which isn't important """
    version: Version
    """ Version number auto-parsed by Pydantic """


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
    result = Schema(name="test", version=version)
    assert result.version == expected


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
    result = Schema(name="test", version=version)
    assert result.version == expected


@pytest.mark.parametrize("version", ["01.2.3", "1.02.3", "1.2.03"])
def test_should_raise_value_error_for_zero_prefixed_versions(version):
    with pytest.raises(pydantic.ValidationError):
        Schema(name="test", version=version)


def test_should_have_schema_examples():
    assert Schema.schema()["properties"]["version"]["examples"] == [
        "1.0.2",
        "2.15.3-alpha",
        "21.3.15-beta+12345",
    ]
