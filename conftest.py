import pytest
import semver


@pytest.fixture(autouse=True)
def add_semver(doctest_namespace):
    doctest_namespace["semver"] = semver
