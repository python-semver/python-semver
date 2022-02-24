.. _sec_reading_versions_from_file:

Reading versions from file
==========================

In cases where a version is stored inside a file, one possible solution
is to use the following function:

.. code-block:: python

    from semver.version import Version

    def get_version(path: str = "version") -> Version:
        """
        Construct a Version from a file
        
        :param path: A text file only containing the semantic version
        :return: A :class:`Version` object containing the semantic
                 version from the file.
        """
        with open(path,"r") as fh:
            version = fh.read().strip()
        return Version.parse(version)
