Comparing Versions
==================

.. meta::
   :description lang=en:
      Comparing versions with semver.compare and the Version class

To compare two versions depends on your type:

* **Two strings**

  Use :func:`semver.compare <semver._deprecated.compare>`::

    >>> semver.compare("1.0.0", "2.0.0")
    -1
    >>> semver.compare("2.0.0", "1.0.0")
    1
    >>> semver.compare("2.0.0", "2.0.0")
    0

  The return value is negative if ``version1 < version2``, zero if
  ``version1 == version2`` and strictly positive if ``version1 > version2``.

* **Two** :class:`~semver.version.Version` **instances**

  Use the specific operator. Currently, the operators ``<``,
  ``<=``, ``>``, ``>=``, ``==``, and ``!=`` are supported::

    >>> v1 = Version.parse("3.4.5")
    >>> v2 = Version.parse("3.5.1")
    >>> v1 < v2
    True
    >>> v1 > v2
    False

* **A** :class:`~semver.version.Version` **type and a** :func:`tuple` **or** :func:`list`

  Use the operator as with two :class:`~semver.version.Version` types::

    >>> v = Version.parse("3.4.5")
    >>> v > (1, 0)
    True
    >>> v < [3, 5]
    True

  The opposite does also work::

    >>> (1, 0) < v
    True
    >>> [3, 5] > v
    True

* **A** :class:`~semver.version.Version` **type and a** :func:`str`

  You can use also raw strings to compare::

    >>> v > "1.0.0"
    True
    >>> v < "3.5.0"
    True

  The opposite does also work::

    >>> "1.0.0" < v
    True
    >>> "3.5.0" > v
    True

  However, if you compare incomplete strings, you get a :py:exc:`python:ValueError` exception::

    >>> v > "1.0"
    Traceback (most recent call last):
    ...
    ValueError: 1.0 is not valid SemVer string

* **A** :class:`~semver.version.Version` **type and a** :func:`dict`

  You can also use a dictionary. In contrast to strings, you can have an "incomplete"
  version (as the other parts are set to zero)::

   >>> v > dict(major=1)
   True

  The opposite does also work::

   >>> dict(major=1) < v
   True

  If the dictionary contains keys that cannot construct a comparable version
  (for example, unknown keys), the comparison is not supported.  The
  comparison operators follow the general rule for invalid comparison operand
  types and return :py:const:`NotImplemented` (see :gh:`316`), so Python
  raises its standard :py:exc:`python:TypeError` instead of an internal
  conversion error::

    >>> v > dict(major=1, unknown=42)
    Traceback (most recent call last):
    ...
    TypeError: '>' not supported between instances of 'Version' and 'dict'


Other types cannot be compared.

If you need to convert some types into others, refer to :ref:`sec.convert.versions`.

The use of these comparison operators also implies that you can use builtin
functions that leverage this capability; builtins including, but not limited to: :func:`max`, :func:`min`
(for examples, see :ref:`sec_max_min`) and :func:`sorted`.

Classifying Version Differences
-------------------------------

Use :meth:`~semver.version.Version.diff` to classify two versions like
`node-semver 7.7.2 <https://github.com/npm/node-semver/blob/v7.7.2/functions/diff.js>`_.
It returns ``major``, ``minor``, ``patch``, ``premajor``, ``preminor``,
``prepatch``, or ``prerelease``. Versions with equal precedence return ``None``,
including versions that differ only in build metadata::

    >>> Version.parse("1.0.0").diff("1.1.5")
    'minor'
    >>> Version.parse("1.0.0+one").diff("1.0.0+two") is None
    True

The higher version determines the classification, regardless of argument order.
If it is a prerelease and a core part differs, the result has a ``pre`` prefix.
Different prereleases with the same core return ``prerelease``::

    >>> Version.parse("1.2.3").diff("1.2.4-rc.1")
    'prepatch'
    >>> Version.parse("1.2.4-rc.1").diff("1.2.3")
    'prepatch'
    >>> Version.parse("1.2.3-alpha").diff("1.2.3-beta")
    'prerelease'

When the lower version is a prerelease and the higher version is a release,
node-semver applies special rules. A lower version with zero minor and patch
always gives ``major``, even if the core versions differ. Otherwise, for equal
core versions, zero patch gives ``minor`` and nonzero patch gives ``patch``::

    >>> Version.parse("1.0.0-alpha").diff("1.0.0")
    'major'
    >>> Version.parse("1.0.0-alpha").diff("1.1.1")
    'major'
    >>> Version.parse("1.1.0-alpha").diff("1.1.0")
    'minor'
    >>> Version.parse("1.0.1-rc.1").diff("1.0.1")
    'patch'

``diff`` classifies version differences; it does not decide which bump to apply
on a staging branch. For example, the last pair gives ``patch``, even if your
release policy calls for a minor bump. It does not change ``next_version`` or
the bump methods.

The operand may be a ``Version`` (including a subclass), ``str``, ``bytes``,
``dict``, ``tuple``, or ``list``. Strings and bytes are parsed using the receiver's
class; collections are passed as keyword or positional constructor arguments::

    >>> Version(1).diff(b"2.0.0")
    'major'
    >>> Version(1).diff({"major": 2})
    'major'
    >>> Version(1).diff((2, 0, 0))
    'major'
    >>> Version(1).diff([2, 0, 0])
    'major'

Existing ``Version`` instances are used without reconstruction. Classification
uses SemVer precedence, including on subclass receivers. Unsupported types and
invalid constructor argument types or shapes raise ``TypeError``. Invalid
strings, byte decoding, and invalid constructor values raise ``ValueError``;
conversion errors are propagated as in Python's parsing and construction APIs.
