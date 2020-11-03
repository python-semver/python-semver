import sys

import pytest

import semver

sys.path.insert(0, "docs")

from coerce import coerce  # noqa:E402
from semverwithvprefix import SemVerWithVPrefix  # noqa:E402


@pytest.fixture(autouse=True)
def add_semver(doctest_namespace):
    doctest_namespace["Version"] = semver.version.Version
    doctest_namespace["semver"] = semver
    doctest_namespace["coerce"] = coerce
    doctest_namespace["SemVerWithVPrefix"] = SemVerWithVPrefix


@pytest.fixture
def version():
    """
    Creates a version

    :return: a version type
    :rtype: Version
    """
    return semver.Version(
        major=1, minor=2, patch=3, prerelease="alpha.1.2", build="build.11.e0f985a"
    )
