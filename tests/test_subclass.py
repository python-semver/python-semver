from semver import Version
import pytest


def test_subclass_from_versioninfo():
    class SemVerWithVPrefix(Version):
        @classmethod
        def parse(cls, version):
            if not version[0] in ("v", "V"):
                raise ValueError(
                    "{v!r}: version must start with 'v' or 'V'".format(v=version)
                )
            return super().parse(version[1:])

        def __str__(self):
            # Reconstruct the tag.
            return "v" + super().__str__()

    v = SemVerWithVPrefix.parse("v1.2.3")
    assert str(v) == "v1.2.3"


def test_replace_from_subclass():
    # Issue#426
    # Taken from the example "Creating Subclasses from Version"
    class SemVerWithVPrefix(Version):
        """
        A subclass of Version which allows a "v" prefix
        """

        @classmethod
        def parse(cls, version: str) -> "SemVerWithVPrefix":
            """
            Parse version string to a Version instance.

            :param version: version string with "v" or "V" prefix
            :raises ValueError: when version does not start with "v" or "V"
            :return: a new instance
            """
            if not version[0] in ("v", "V"):
                raise ValueError(
                    f"{version!r}: not a valid semantic version tag. "
                    "Must start with 'v' or 'V'"
                )
            return super().parse(version[1:], optional_minor_and_patch=True)

        def __str__(self) -> str:
            # Reconstruct the tag
            return "v" + super().__str__()

    version = SemVerWithVPrefix.parse("v1.1.0")
    dev_version = version.replace(prerelease="dev.0")

    assert str(dev_version) == "v1.1.0-dev.0"


def test_compare_with_subclass():
    class SemVerSubclass(Version):
        pass

    with pytest.raises(TypeError):
        SemVerSubclass.parse("1.0.0").compare(Version.parse("1.0.0"))
    assert Version.parse("1.0.0").compare(SemVerSubclass.parse("1.0.0")) == 0

    assert (
        SemVerSubclass.parse("1.0.0").__eq__(Version.parse("1.0.0")) is NotImplemented
    )
    assert Version.parse("1.0.0").__eq__(SemVerSubclass.parse("1.0.0")) is True

    assert SemVerSubclass.parse("1.0.0") == Version.parse("1.0.0")
    assert Version.parse("1.0.0") == SemVerSubclass.parse("1.0.0")
