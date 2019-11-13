:orphan:

pysemver |version|
==================

Synopsis
--------

.. _invocation:

.. code:: bash

   pysemver compare <VERSION1> <VERSION2>
   pysemver bump {major,minor,patch,prerelease,build} <VERSION>


Description
-----------

The semver library provides a command line interface with the name
:command:`pysemver` to make the functionality accessible for shell
scripts. The script supports several subcommands.


Global Options
~~~~~~~~~~~~~~

.. program:: pysemver

.. option:: -h, --help

   Display usage summary.

.. option:: --version

   Show program's version number and exit.


Commands
--------

.. HINT: Sort the subcommands alphabetically

pysemver bump
~~~~~~~~~~~~~

Bump a version.

.. code:: bash

   pysemver bump <PART> <VERSION>

.. option:: <PART>

    The part to bump. Valid strings can be ``major``, ``minor``,
    ``patch``, ``prerelease``, or ``build``. The part has the
    following effects:

    * ``major``: Raise the major part of the version and set
      minor and patch to zero, remove prerelease and build.
    * ``minor``: Raise the minor part of the version and set
      patch to zero, remove prerelease and build.
    * ``patch``: Raise the patch part of the version and
      remove prerelease and build.
    * ``prerelease`` Raise the prerelease of the version and
      remove the build part.
    * ``build``: Raise the build part.

.. option:: <VERSION>

    The version to bump.

To bump a version, you pass the name of the part (``major``, ``minor``,
``patch``, ``prerelease``, or ``build``) and the version string.
The bumped version is printed on standard out::

   $ pysemver bump major 1.2.3
   2.0.0
   $ pysemver bump minor 1.2.3
   1.3.0

If you pass a version string which is not a valid semantical version,
you get an error message and a return code != 0::

   $ pysemver bump build 1.5
   ERROR 1.5 is not valid SemVer string


pysemver compare
~~~~~~~~~~~~~~~~

Compare two versions.

.. code:: bash

   pysemver compare <VERSION1> <VERSION2>

.. option:: <VERSION1>

    First version

.. option:: <VERSION2>

    Second version

When you compare two versions, the result is printed on *standard out*,
to indicates which is the bigger version:

* ``-1`` if first version is smaller than the second version,
* ``0`` if both versions are the same,
* ``1`` if the first version is greater than the second version.

The *error code* returned by the script indicates if both versions
are valid (return code 0) or not (return code != 0)::

    $ pysemver compare 1.2.3 2.4.0
    -1
    $ pysemver compare 1.2.3 2.4.0 ; echo $?
    0
    $ pysemver compare 1.2.3 2.4.0 ; echo $?
    ERROR 1.2.x is not valid SemVer string
    2


See also
--------

:Documentation: https://python-semver.readthedocs.io/
:Source code:   https://github.com/python-semver/python-semver
:Bug tracker:   https://github.com/python-semver/python-semver/issues
