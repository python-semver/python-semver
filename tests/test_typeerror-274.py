import pytest
import semver


def test_should_work_with_string_and_bytes():
    result = semver.compare("1.1.0", b"1.2.2")
    assert result == -1
    result = semver.compare(b"1.1.0", "1.2.2")
    assert result == -1


def test_should_not_work_with_invalid_args():
    with pytest.raises(TypeError):
        semver.version.Version.parse(8)
