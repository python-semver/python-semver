from semver import Version


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
