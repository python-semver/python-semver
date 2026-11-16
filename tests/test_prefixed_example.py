import pytest
from semverwithvprefix import SemVerWithVPrefix


@pytest.mark.parametrize("version", ["", "1.2.3", "v", "V"])
def test_prefix_example_rejects_invalid_versions(version):
    with pytest.raises(ValueError):
        SemVerWithVPrefix.parse(version)


@pytest.mark.parametrize("version", ["", "1.2.3", "v", "V"])
def test_prefix_example_reports_invalid_versions(version):
    assert SemVerWithVPrefix.is_valid(version) is False


@pytest.mark.parametrize("version", ["v1", "V1.2", "v1.2.3", "v1.2.3-alpha+build"])
def test_prefix_example_accepts_valid_versions(version):
    assert isinstance(SemVerWithVPrefix.parse(version), SemVerWithVPrefix)
    assert SemVerWithVPrefix.is_valid(version) is True
