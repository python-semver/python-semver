from semver import VersionInfo


class SemVerWithVPrefix(VersionInfo):
    """
    A subclass of VersionInfo which allows a "v" prefix
    """

    @classmethod
    def parse(cls, version):
        """
        Parse version string to a VersionInfo instance.

        :param version: version string with "v" or "V" prefix
        :type version: str
        :raises ValueError: when version does not start with "v" or "V"
        :return: a new instance
        :rtype: :class:`SemVerWithVPrefix`
        """
        if not version[0] in ("v", "V"):
            raise ValueError(
                "{v!r}: not a valid semantic version tag. Must start with 'v' or 'V'".format(
                    v=version
                )
            )
        self = super(SemVerWithVPrefix, cls).parse(version[1:])
        return self

    def __str__(self):
        # Reconstruct the tag
        return "v" + super(SemVerWithVPrefix, self).__str__()
