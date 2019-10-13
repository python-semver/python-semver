CLI
===

The library provides also a command line interface. This allows to include
the functionality of semver into shell scripts.

Using the pysemver Script
-------------------------

The script name is :command:`pysemver` and provides the subcommands ``bump``
and ``compare``.

To bump a version, you pass the name of the part (major, minor, patch, prerelease, or
build) and the version string, for example::

   $ pysemver bump major 1.2.3
   2.0.0
   $ pysemver bump minor 1.2.3
   1.3.0

If you pass a version string which is not a valid semantical version, you get
an error message::

   $ pysemver bump build 1.5
   ERROR 1.5 is not valid SemVer string

To compare two versions, use the ``compare`` subcommand. The result is

* ``-1`` if first version is smaller than the second version,
* ``0`` if both are the same,
* ``1`` if the first version is greater than the second version.

For example::

    $ pysemver compare 1.2.3 2.4.0


.. _interface:

Interface
---------

.. argparse::
   :ref: semver.createparser
   :prog: pysemver
