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

  If the dictionary contains unknown keys, you get a :py:exc:`python:TypeError` exception::

    >>> v > dict(major=1, unknown=42)
    Traceback (most recent call last):
    ...
    TypeError: ... got an unexpected keyword argument 'unknown'


Other types cannot be compared.

If you need to convert some types into others, refer to :ref:`sec.convert.versions`.

The use of these comparison operators also implies that you can use builtin
functions that leverage this capability; builtins including, but not limited to: :func:`max`, :func:`min`
(for examples, see :ref:`sec_max_min`) and :func:`sorted`.
