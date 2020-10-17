import pytest


def test_immutable_major(version):
    with pytest.raises(AttributeError, match="attribute 'major' is readonly"):
        version.major = 9


def test_immutable_minor(version):
    with pytest.raises(AttributeError, match="attribute 'minor' is readonly"):
        version.minor = 9


def test_immutable_patch(version):
    with pytest.raises(AttributeError, match="attribute 'patch' is readonly"):
        version.patch = 9


def test_immutable_prerelease(version):
    with pytest.raises(AttributeError, match="attribute 'prerelease' is readonly"):
        version.prerelease = "alpha.9.9"


def test_immutable_build(version):
    with pytest.raises(AttributeError, match="attribute 'build' is readonly"):
        version.build = "build.99.e0f985a"


def test_immutable_unknown_attribute(version):
    with pytest.raises(
        AttributeError, match=".* object has no attribute 'new_attribute'"
    ):
        version.new_attribute = "forbidden"
