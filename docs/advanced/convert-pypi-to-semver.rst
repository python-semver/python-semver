Converting Versions between PyPI and semver
===========================================

.. meta::
   :description lang=en:
      Converting versions between PyPI and semver

.. Link
   https://packaging.pypa.io/en/latest/_modules/packaging/version.html#InvalidVersion

When packaging for PyPI, your versions are defined through `PEP 440`_.
This is the standard version scheme for Python packages and
implemented by the :class:`packaging.version.Version` class.

However, these versions are different from semver versions
(cited from `PEP 440`_):

* The "Major.Minor.Patch" (described in this PEP as "major.minor.micro")
  aspects of semantic versioning (clauses 1-8 in the 2.0.0
  specification) are fully compatible with the version scheme defined
  in this PEP, and abiding by these aspects is encouraged.

* Semantic versions containing a hyphen (pre-releases - clause 10)
  or a plus sign (builds - clause 11) are *not* compatible with this PEP
  and are not permitted in the public version field.

In other words, it's not always possible to convert between these different
versioning schemes without information loss. It depends on what parts are
used. The following table gives a mapping between these two versioning
schemes:

+--------------+----------------+
| PyPI Version | Semver version |
+==============+================+
| ``epoch``    | n/a            |
+--------------+----------------+
| ``major``    | ``major``      |
+--------------+----------------+
| ``minor``    | ``minor``      |
+--------------+----------------+
| ``micro``    | ``patch``      |
+--------------+----------------+
| ``pre``      | ``prerelease`` |
+--------------+----------------+
| ``dev``      | ``build``      |
+--------------+----------------+
| ``post``     | n/a            |
+--------------+----------------+


.. _convert_pypi_to_semver:

From PyPI to semver
-------------------

We distinguish between the following use cases:


* **"Incomplete" versions**

  If you only have a major part, this shouldn't be a problem.
  The initializer of :class:`semver.Version <semver.version.Version>` takes
  care to fill missing parts with zeros (except for major).

  .. code-block:: python

      >>> from packaging.version import Version as PyPIVersion
      >>> from semver import Version

      >>> p = PyPIVersion("3.2")
      >>> p.release
      (3, 2)
      >>> Version(*p.release)
      Version(major=3, minor=2, patch=0, prerelease=None, build=None)

* **Major, minor, and patch**

  This is the simplest and most compatible approch. Both versioning
  schemes are compatible without information loss.

  .. code-block:: python

      >>> p = PyPIVersion("3.0.0")
      >>> p.base_version
      '3.0.0'
      >>> p.release
      (3, 0, 0)
      >>> Version(*p.release)
      Version(major=3, minor=0, patch=0, prerelease=None, build=None)

* **With** ``pre`` **part only**

  A prerelease exists in both versioning schemes. As such, both are
  a natural candidate. A prelease in PyPI version terms is the same
  as a "release candidate", or "rc".

  .. code-block:: python

      >>> p = PyPIVersion("2.1.6.pre5")
      >>> p.base_version
      '2.1.6'
      >>> p.pre
      ('rc', 5)
      >>> pre = "".join([str(i) for i in p.pre])
      >>> Version(*p.release, pre)
      Version(major=2, minor=1, patch=6, prerelease='rc5', build=None)

* **With only development version**

  Semver doesn't have a "development" version.
  However, we could use Semver's ``build`` part:

  .. code-block:: python

      >>> p = PyPIVersion("3.0.0.dev2")
      >>> p.base_version
      '3.0.0'
      >>> p.dev
      2
      >>> Version(*p.release, build=f"dev{p.dev}")
      Version(major=3, minor=0, patch=0, prerelease=None, build='dev2')

* **With a** ``post`` **version**

  Semver doesn't know the concept of a post version. As such, there
  is currently no way to convert it reliably.

* **Any combination**

  There is currently no way to convert a PyPI version which consists
  of, for example, development *and* post parts.


You can use the following function to convert a PyPI version into
semver:

.. code-block:: python

    def convert2semver(ver: packaging.version.Version) -> semver.Version:
        """Converts a PyPI version into a semver version

        :param ver: the PyPI version
        :return: a semver version
        :raises ValueError: if epoch or post parts are used
        """
        if not ver.epoch:
            raise ValueError("Can't convert an epoch to semver")
        if not ver.post:
            raise ValueError("Can't convert a post part to semver")

        pre = None if not ver.pre else "".join([str(i) for i in ver.pre])
        return semver.Version(*ver.release, prerelease=pre, build=ver.dev)


.. _convert_semver_to_pypi:

From semver to PyPI
-------------------

We distinguish between the following use cases:


* **Major, minor, and patch**

  .. code-block:: python

      >>> from packaging.version import Version as PyPIVersion
      >>> from semver import Version

      >>> v = Version(1, 2, 3)
      >>> PyPIVersion(str(v.finalize_version()))
      <Version('1.2.3')>

* **With** ``pre`` **part only**

  .. code-block:: python

      >>> v = Version(2, 1, 4, prerelease="rc1")
      >>> PyPIVersion(str(v))
      <Version('2.1.4rc1')>

* **With only development version**

  .. code-block:: python

      >>> v = Version(3, 2, 8, build="dev4")
      >>> PyPIVersion(f"{v.finalize_version()}{v.build}")
      <Version('3.2.8.dev4')>

If you are unsure about the parts of the version, the following
function helps to convert the different parts:

.. code-block:: python

    def convert2pypi(ver: semver.Version) -> packaging.version.Version:
        """Converts a semver version into a version from PyPI

        A semver prerelease will be converted into a
        prerelease of PyPI.
        A semver build will be converted into a development
        part of PyPI
        :param semver.Version ver: the semver version
        :return: a PyPI version
        """
        v = ver.finalize_version()
        prerelease = ver.prerelease if ver.prerelease else ""
        build = ver.build if ver.build else ""
        return PyPIVersion(f"{v}{prerelease}{build}")


.. _PEP 440: https://www.python.org/dev/peps/pep-0440/
