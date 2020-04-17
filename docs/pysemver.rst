:orphan:

pysemver |version|
==================

Synopsis
--------

.. _invocation:

.. code:: bash

   pysemver <COMMAND> <OPTION>...


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

    The part to bump. Valid strings are ``major``, ``minor``,
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


pysemver check
~~~~~~~~~~~~~~

Checks if a string is a valid semver version.

.. code:: bash

   pysemver check <VERSION>

.. option:: <VERSION>

    The version string to check.

The *error code* returned by the script indicates if the
version is valid (=0) or not (!=0)::

    $ pysemver check 1.2.3; echo $?
    0
    $ pysemver check 2.1; echo $?
    ERROR Invalid version '2.1'
    2


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


Return Code
-----------

The *return code* of the script (accessible by ``$?`` from the Bash)
indicates if the subcommand returned successfully nor not. It is *not*
meant as the result of the subcommand.

The result of the subcommand is printed on the standard out channel
("stdout" or ``0``), any error messages to standard error ("stderr" or
``2``).

For example, to compare two versions, the command expects two valid
semver versions::

    $ pysemver compare 1.2.3 2.4.0
    -1
    $ echo $?
    0

The return code is zero, but the result is ``-1``.

However, if you pass invalid versions, you get this situation::

    $ pysemver compare 1.2.3 2.4
    ERROR 2.4 is not valid SemVer string
    $ echo $?
    2

If you use the :command:`pysemver` in your own scripts, check the
return code first before you process the standard output.


See also
--------

:Documentation: https://python-semver.readthedocs.io/
:Source code:   https://github.com/python-semver/python-semver
:Bug tracker:   https://github.com/python-semver/python-semver/issues
