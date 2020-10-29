from semver import Version


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
