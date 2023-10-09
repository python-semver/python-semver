.. _sec_reading_versions_from_file:

Reading Versions from File
==========================

.. meta::
   :description lang=en:
      Reading versions from file

In cases where a version is stored inside a file, one possible solution
is to use the following function:

.. code-block:: python

    import os
    from typing import Union
    from semver.version import Version

    def get_version(path: Union[str, os.PathLike]) -> semver.Version:
        """
        Construct a Version object from a file
        
        :param path: A text file only containing the semantic version
        :return: A :class:`Version` object containing the semantic
                 version from the file.
        """
        version = open(path,"r").read().strip()
        return Version.parse(version)
