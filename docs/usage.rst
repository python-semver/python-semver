Using semver
============

The :mod:`semver` module can store a version in the :class:`~semver.version.Version` class.
For historical reasons, a version can be also stored as a string or dictionary.

Each type can be converted into the other, if the minimum requirements
are met.


Getting the Implemented semver.org Version
------------------------------------------

The semver.org page is the authoritative specification of how semantic
versioning is defined.
To know which version of semver.org is implemented in the semver library,
use the following constant::

   >>> semver.SEMVER_SPEC_VERSION
   '2.0.0'


Getting the Version of semver
-----------------------------

To know the version of semver itself, use the following construct::

   >>> semver.__version__
   '3.0.0-dev.2'


Creating a Version
------------------

.. versionchanged:: 3.0.0

  The former :class:`~semver.version.VersionInfo`
  has been renamed to :class:`~semver.version.Version`.

The preferred way to create a new version is with the class
:class:`~semver.version.Version`.

.. note::

   In the previous major release semver 2 it was possible to
   create a version with module level functions.
   However, module level functions are marked as *deprecated*
   since version 2.x.y now.
   These functions will be removed in semver 3.1.0.
   For details, see the sections :ref:`sec_replace_deprecated_functions`
   and :ref:`sec_display_deprecation_warnings`.

A :class:`~semver.version.Version` instance can be created in different ways:

* From a Unicode string::

    >>> from semver.version import Version
    >>> Version.parse("3.4.5-pre.2+build.4")
    Version(major=3, minor=4, patch=5, prerelease='pre.2', build='build.4')
    >>> Version.parse(u"5.3.1")
    Version(major=5, minor=3, patch=1, prerelease=None, build=None)

* From a byte string::

    >>> Version.parse(b"2.3.4")
    Version(major=2, minor=3, patch=4, prerelease=None, build=None)

* From individual parts by a dictionary::

    >>> d = {'major': 3, 'minor': 4, 'patch': 5,  'prerelease': 'pre.2', 'build': 'build.4'}
    >>> Version(**d)
    Version(major=3, minor=4, patch=5, prerelease='pre.2', build='build.4')

  Keep in mind, the ``major``, ``minor``, ``patch`` parts has to
  be positive integers or strings:

      >>> d = {'major': -3, 'minor': 4, 'patch': 5,  'prerelease': 'pre.2', 'build': 'build.4'}
      >>> Version(**d)
      Traceback (most recent call last):
      ...
      ValueError: 'major' is negative. A version can only be positive.

  As a minimum requirement, your dictionary needs at least the ``major``
  key, others can be omitted. You get a ``TypeError`` if your
  dictionary contains invalid keys.
  Only the keys ``major``, ``minor``, ``patch``, ``prerelease``, and ``build``
  are allowed.

* From a tuple::

    >>> t = (3, 5, 6)
    >>> Version(*t)
    Version(major=3, minor=5, patch=6, prerelease=None, build=None)

  You can pass either an integer or a string for ``major``, ``minor``, or
  ``patch``::

    >>> Version("3", "5", 6)
    Version(major=3, minor=5, patch=6, prerelease=None, build=None)

The old, deprecated module level functions are still available but
using them are discoraged. They are available to convert old code
to semver3.

If you need them, they return different builtin objects (string and dictionary).
Keep in mind, once you have converted a version into a string or dictionary,
it's an ordinary builtin object. It's not a special version object like
the :class:`~semver.version.Version` class anymore.

Depending on your use case, the following methods are available:

* From individual version parts into a string

  In some cases you only need a string from your version data::

    >>> semver.format_version(3, 4, 5, 'pre.2', 'build.4')
    '3.4.5-pre.2+build.4'

* From a string into a dictionary

  To access individual parts, you can use the function :func:`semver.parse`::

    >>> semver.parse("3.4.5-pre.2+build.4")
    OrderedDict([('major', 3), ('minor', 4), ('patch', 5), ('prerelease', 'pre.2'), ('build', 'build.4')])

  If you pass an invalid version string you will get a :py:exc:`ValueError`::

    >>> semver.parse("1.2")
    Traceback (most recent call last):
    ...
    ValueError: 1.2 is not valid SemVer string


Parsing a Version String
------------------------

"Parsing" in this context means to identify the different parts in a string.
Use the function :func:`Version.parse <semver.version.Version.parse>`::

    >>> Version.parse("3.4.5-pre.2+build.4")
    Version(major=3, minor=4, patch=5, prerelease='pre.2', build='build.4')


Checking for a Valid Semver Version
-----------------------------------

If you need to check a string if it is a valid semver version, use the
classmethod :func:`Version.isvalid <semver.version.Version.isvalid>`:

.. code-block:: python

    >>> Version.isvalid("1.0.0")
    True
    >>> Version.isvalid("invalid")
    False


.. _sec.properties.parts:

Accessing Parts of a Version Through Names
------------------------------------------

The :class:`~semver.version.Version` class contains attributes to access the different
parts of a version:

.. code-block:: python

    >>> v = Version.parse("3.4.5-pre.2+build.4")
    >>> v.major
    3
    >>> v.minor
    4
    >>> v.patch
    5
    >>> v.prerelease
    'pre.2'
    >>> v.build
    'build.4'

However, the attributes are read-only. You cannot change any of the above attributes.
If you do, you get an :py:exc:`AttributeError`::

    >>> v.minor = 5
    Traceback (most recent call last):
    ...
    AttributeError: attribute 'minor' is readonly

If you need to replace different parts of a version, refer to section :ref:`sec.replace.parts`.

In case you need the different parts of a version stepwise, iterate over the :class:`~semver.version.Version` instance::

    >>> for item in Version.parse("3.4.5-pre.2+build.4"):
    ...     print(item)
    3
    4
    5
    pre.2
    build.4
    >>> list(Version.parse("3.4.5-pre.2+build.4"))
    [3, 4, 5, 'pre.2', 'build.4']


.. _sec.getitem.parts:

Accessing Parts Through Index Numbers
-------------------------------------

.. versionadded:: 2.10.0

Another way to access parts of a version is to use an index notation. The underlying
:class:`~semver.version.Version` object allows to access its data through
the magic method :func:`~semver.version.Version.__getitem__`.

For example, the ``major`` part can be accessed by index number 0 (zero).
Likewise the other parts:

.. code-block:: python

    >>> ver = Version.parse("10.3.2-pre.5+build.10")
    >>> ver[0], ver[1], ver[2], ver[3], ver[4]
    (10, 3, 2, 'pre.5', 'build.10')

If you need more than one part at the same time, use the slice notation:

.. code-block:: python

    >>> ver[0:3]
    (10, 3, 2)

Or, as an alternative, you can pass a :func:`slice` object:

.. code-block:: python

    >>> sl = slice(0,3)
    >>> ver[sl]
    (10, 3, 2)

Negative numbers or undefined parts raise an :py:exc:`IndexError` exception:

.. code-block:: python

    >>> ver = Version.parse("10.3.2")
    >>> ver[3]
    Traceback (most recent call last):
    ...
    IndexError: Version part undefined
    >>> ver[-2]
    Traceback (most recent call last):
    ...
    IndexError: Version index cannot be negative

.. _sec.replace.parts:

Replacing Parts of a Version
----------------------------

If you want to replace different parts of a version, but leave other parts
unmodified, use the function :func:`replace <semver.version.Version.replace>`:

* From a :class:`Version <semver.version.Version>` instance::

   >>> version = semver.Version.parse("1.4.5-pre.1+build.6")
   >>> version.replace(major=2, minor=2)
   Version(major=2, minor=2, patch=5, prerelease='pre.1', build='build.6')

* From a version string::

   >>> semver.replace("1.4.5-pre.1+build.6", major=2)
   '2.4.5-pre.1+build.6'

If you pass invalid keys you get an exception::

   >>> semver.replace("1.2.3", invalidkey=2)
   Traceback (most recent call last):
   ...
   TypeError: replace() got 1 unexpected keyword argument(s): invalidkey
   >>> version = semver.Version.parse("1.4.5-pre.1+build.6")
   >>> version.replace(invalidkey=2)
   Traceback (most recent call last):
   ...
   TypeError: replace() got 1 unexpected keyword argument(s): invalidkey


.. _sec.convert.versions:

Converting a Version instance into Different Types
------------------------------------------------------

Sometimes it is needed to convert a :class:`Version <semver.version.Version>` instance into
a different type. For example, for displaying or to access all parts.

It is possible to convert a :class:`Version <semver.version.Version>` instance:

* Into a string with the builtin function :func:`str`::

    >>> str(Version.parse("3.4.5-pre.2+build.4"))
    '3.4.5-pre.2+build.4'

* Into a dictionary with :func:`to_dict <semver.version.Version.to_dict>`::

    >>> v = Version(major=3, minor=4, patch=5)
    >>> v.to_dict()
    OrderedDict([('major', 3), ('minor', 4), ('patch', 5), ('prerelease', None), ('build', None)])

* Into a tuple with :func:`to_tuple <semver.version.Version.to_tuple>`::

    >>> v = Version(major=5, minor=4, patch=2)
    >>> v.to_tuple()
    (5, 4, 2, None, None)


Raising Parts of a Version
--------------------------

The ``semver`` module contains the following functions to raise parts of
a version:

* :func:`Version.bump_major <semver.version.Version.bump_major>`: raises the major part and set all other parts to
  zero. Set ``prerelease`` and ``build`` to ``None``.
* :func:`Version.bump_minor <semver.version.Version.bump_minor>`: raises the minor part and sets ``patch`` to zero.
  Set ``prerelease`` and ``build`` to ``None``.
* :func:`Version.bump_patch <semver.version.Version.bump_patch>`: raises the patch part. Set ``prerelease`` and
  ``build`` to ``None``.
* :func:`Version.bump_prerelease <semver.version.Version.bump_prerelease>`: raises the prerelease part and set
  ``build`` to ``None``.
* :func:`Version.bump_build <semver.version.Version.bump_build>`: raises the build part.

.. code-block:: python

    >>> str(Version.parse("3.4.5-pre.2+build.4").bump_major())
    '4.0.0'
    >>> str(Version.parse("3.4.5-pre.2+build.4").bump_minor())
    '3.5.0'
    >>> str(Version.parse("3.4.5-pre.2+build.4").bump_patch())
    '3.4.6'
    >>> str(Version.parse("3.4.5-pre.2+build.4").bump_prerelease())
    '3.4.5-pre.3'
    >>> str(Version.parse("3.4.5-pre.2+build.4").bump_build())
    '3.4.5-pre.2+build.5'

Likewise the module level functions :func:`semver.bump_major`.


Increasing Parts of a Version Taking into Account Prereleases
-------------------------------------------------------------

.. versionadded:: 2.10.0
   Added :func:`Version.next_version <semver.version.Version.next_version>`.

If you want to raise your version and take prereleases into account,
the function :func:`next_version <semver.version.Version.next_version>`
would perhaps a better fit.


.. code-block:: python

    >>> v = Version.parse("3.4.5-pre.2+build.4")
    >>> str(v.next_version(part="prerelease"))
    '3.4.5-pre.3'
    >>> str(Version.parse("3.4.5-pre.2+build.4").next_version(part="patch"))
    '3.4.5'
    >>> str(Version.parse("3.4.5+build.4").next_version(part="patch"))
    '3.4.5'
    >>> str(Version.parse("0.1.4").next_version("prerelease"))
    '0.1.5-rc.1'


Comparing Versions
------------------

To compare two versions depends on your type:

* **Two strings**

  Use :func:`semver.compare`::

    >>> semver.compare("1.0.0", "2.0.0")
    -1
    >>> semver.compare("2.0.0", "1.0.0")
    1
    >>> semver.compare("2.0.0", "2.0.0")
    0

  The return value is negative if ``version1 < version2``, zero if
  ``version1 == version2`` and strictly positive if ``version1 > version2``.

* **Two** :class:`Version <semver.version.Version>` **instances**

  Use the specific operator. Currently, the operators ``<``,
  ``<=``, ``>``, ``>=``, ``==``, and ``!=`` are supported::

    >>> v1 = Version.parse("3.4.5")
    >>> v2 = Version.parse("3.5.1")
    >>> v1 < v2
    True
    >>> v1 > v2
    False

* **A** :class:`Version <semver.version.Version>` **type and a** :func:`tuple` **or** :func:`list`

  Use the operator as with two :class:`Version <semver.version.Version>` types::

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

* **A** :class:`Version <semver.version.Version>` **type and a** :func:`str`

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

  However, if you compare incomplete strings, you get a :py:exc:`ValueError` exception::

    >>> v > "1.0"
    Traceback (most recent call last):
    ...
    ValueError: 1.0 is not valid SemVer string

* **A** :class:`Version <semver.version.Version>` **type and a** :func:`dict`

  You can also use a dictionary. In contrast to strings, you can have an "incomplete"
  version (as the other parts are set to zero)::

   >>> v > dict(major=1)
   True

  The opposite does also work::

   >>> dict(major=1) < v
   True

  If the dictionary contains unknown keys, you get a :py:exc:`TypeError` exception::

    >>> v > dict(major=1, unknown=42)
    Traceback (most recent call last):
    ...
    TypeError: ... got an unexpected keyword argument 'unknown'


Other types cannot be compared.

If you need to convert some types into others, refer to :ref:`sec.convert.versions`.

The use of these comparison operators also implies that you can use builtin
functions that leverage this capability; builtins including, but not limited to: :func:`max`, :func:`min`
(for examples, see :ref:`sec_max_min`) and :func:`sorted`.


Determining Version Equality
----------------------------

Version equality means for semver, that major, minor, patch, and prerelease
parts are equal in both versions you compare. The build part is ignored.
For example::

    >>> v = Version.parse("1.2.3-rc4+1e4664d")
    >>> v == "1.2.3-rc4+dedbeef"
    True

This also applies when a :class:`Version <semver.version.Version>` is a member of a set, or a
dictionary key::

    >>> d = {}
    >>> v1 = Version.parse("1.2.3-rc4+1e4664d")
    >>> v2 = Version.parse("1.2.3-rc4+dedbeef")
    >>> d[v1] = 1
    >>> d[v2]
    1
    >>> s = set()
    >>> s.add(v1)
    >>> v2 in s
    True



Comparing Versions through an Expression
----------------------------------------

If you need a more fine-grained approach of comparing two versions,
use the :func:`semver.match` function. It expects two arguments:

1. a version string
2. a match expression

Currently, the match expression supports the following operators:

* ``<`` smaller than
* ``>`` greater than
* ``>=`` greater or equal than
* ``<=`` smaller or equal than
* ``==`` equal
* ``!=`` not equal

That gives you the following possibilities to express your condition:

.. code-block:: python

    >>> semver.match("2.0.0", ">=1.0.0")
    True
    >>> semver.match("1.0.0", ">1.0.0")
    False

.. _sec_max_min:

Getting Minimum and Maximum of Multiple Versions
------------------------------------------------
.. versionchanged:: 2.10.2
   The functions :func:`semver.max_ver` and :func:`semver.min_ver` are deprecated in
   favor of their builtin counterparts :func:`max` and :func:`min`.

Since :class:`Version <semver.version.Version>` implements
:func:`__gt__ <semver.version.Version.__gt__>` and
:func:`__lt__ <semver.version.Version.__lt__>`, it can be used with builtins requiring:

.. code-block:: python

    >>> max([Version(0, 1, 0), Version(0, 2, 0), Version(0, 1, 3)])
    Version(major=0, minor=2, patch=0, prerelease=None, build=None)
    >>> min([Version(0, 1, 0), Version(0, 2, 0), Version(0, 1, 3)])
    Version(major=0, minor=1, patch=0, prerelease=None, build=None)

Incidentally, using :func:`map`, you can get the min or max version of any number of versions of the same type
(convertible to :class:`Version <semver.version.Version>`).

For example, here are the maximum and minimum versions of a list of version strings:

.. code-block:: python

    >>> str(max(map(Version.parse, ['1.1.0', '1.2.0', '2.1.0', '0.5.10', '0.4.99'])))
    '2.1.0'
    >>> str(min(map(Version.parse, ['1.1.0', '1.2.0', '2.1.0', '0.5.10', '0.4.99'])))
    '0.4.99'

And the same can be done with tuples:

.. code-block:: python

    >>> max(map(lambda v: Version(*v), [(1, 1, 0), (1, 2, 0), (2, 1, 0), (0, 5, 10), (0, 4, 99)])).to_tuple()
    (2, 1, 0, None, None)
    >>> min(map(lambda v: Version(*v), [(1, 1, 0), (1, 2, 0), (2, 1, 0), (0, 5, 10), (0, 4, 99)])).to_tuple()
    (0, 4, 99, None, None)

For dictionaries, it is very similar to finding the max version tuple: see :ref:`sec.convert.versions`.

The "old way" with :func:`semver.max_ver` or :func:`semver.min_ver` is still available, but not recommended:

.. code-block:: python

    >>> semver.max_ver("1.0.0", "2.0.0")
    '2.0.0'
    >>> semver.min_ver("1.0.0", "2.0.0")
    '1.0.0'


.. _sec_dealing_with_invalid_versions:

Dealing with Invalid Versions
-----------------------------

As semver follows the semver specification, it cannot parse version
strings which are considered "invalid" by that specification. The semver
library cannot know all the possible variations so you need to help the
library a bit.

For example, if you have a version string ``v1.2`` would be an invalid
semver version.
However, "basic" version strings consisting of major, minor,
and patch part, can be easy to convert. The following function extract this
information and returns a tuple with two items:

.. literalinclude:: coerce.py
   :language: python


The function returns a *tuple*, containing a :class:`Version <semver.version.Version>`
instance or None as the first element and the rest as the second element.
The second element (the rest) can be used to make further adjustments.

For example:

.. code-block:: python

    >>> coerce("v1.2")
    (Version(major=1, minor=2, patch=0, prerelease=None, build=None), '')
    >>> coerce("v2.5.2-bla")
    (Version(major=2, minor=5, patch=2, prerelease=None, build=None), '-bla')


.. _sec_replace_deprecated_functions:

Replacing Deprecated Functions
------------------------------

.. versionchanged:: 2.10.0
   The development team of semver has decided to deprecate certain functions on
   the module level. The preferred way of using semver is through the
   :class:`semver.Version` class.

The deprecated functions can still be used in version 2.10.0 and above. In version 3 of
semver, the deprecated functions will be removed.

The following list shows the deprecated functions and how you can replace
them with code which is compatible for future versions:


* :func:`semver.bump_major`, :func:`semver.bump_minor`, :func:`semver.bump_patch`, :func:`semver.bump_prerelease`, :func:`semver.bump_build`

  Replace them with the respective methods of the :class:`Version <semver.version.Version>`
  class.
  For example, the function :func:`semver.bump_major` is replaced by
  :func:`semver.Version.bump_major` and calling the ``str(versionobject)``:

  .. code-block:: python

     >>> s1 = semver.bump_major("3.4.5")
     >>> s2 = str(Version.parse("3.4.5").bump_major())
     >>> s1 == s2
     True

  Likewise with the other module level functions.

* :func:`semver.finalize_version`

  Replace it with :func:`semver.Version.finalize_version`:

  .. code-block:: python

     >>> s1 = semver.finalize_version('1.2.3-rc.5')
     >>> s2 = str(semver.Version.parse('1.2.3-rc.5').finalize_version())
     >>> s1 == s2
     True

* :func:`semver.format_version`

  Replace it with ``str(versionobject)``:

  .. code-block:: python

     >>> s1 = semver.format_version(5, 4, 3, 'pre.2', 'build.1')
     >>> s2 = str(Version(5, 4, 3, 'pre.2', 'build.1'))
     >>> s1 == s2
     True

* :func:`semver.max_ver`

  Replace it with ``max(version1, version2, ...)`` or ``max([version1, version2, ...])``:

  .. code-block:: python

     >>> s1 = semver.max_ver("1.2.3", "1.2.4")
     >>> s2 = str(max(map(Version.parse, ("1.2.3", "1.2.4"))))
     >>> s1 == s2
     True

* :func:`semver.min_ver`

  Replace it with ``min(version1, version2, ...)`` or ``min([version1, version2, ...])``:

  .. code-block:: python

     >>> s1 = semver.min_ver("1.2.3", "1.2.4")
     >>> s2 = str(min(map(Version.parse, ("1.2.3", "1.2.4"))))
     >>> s1 == s2
     True

* :func:`semver.parse`

  Replace it with :func:`semver.Version.parse` and
  :func:`semver.Version.to_dict`:

  .. code-block:: python

     >>> v1 = semver.parse("1.2.3")
     >>> v2 = Version.parse("1.2.3").to_dict()
     >>> v1 == v2
     True

* :func:`semver.parse_version_info`

  Replace it with :func:`semver.Version.parse`:

  .. code-block:: python

     >>> v1 = semver.parse_version_info("3.4.5")
     >>> v2 = Version.parse("3.4.5")
     >>> v1 == v2
     True

* :func:`semver.replace`

  Replace it with :func:`semver.Version.replace`:

  .. code-block:: python

     >>> s1 = semver.replace("1.2.3", major=2, patch=10)
     >>> s2 = str(Version.parse('1.2.3').replace(major=2, patch=10))
     >>> s1 == s2
     True


.. _sec_display_deprecation_warnings:

Displaying Deprecation Warnings
-------------------------------

By default,  deprecation warnings are `ignored in Python <https://docs.python.org/3/library/warnings.html#warning-categories>`_.
This also affects semver's own warnings.

It is recommended that you turn on deprecation warnings in your scripts. Use one of
the following methods:

* Use the option `-Wd <https://docs.python.org/3/using/cmdline.html#cmdoption-w>`_
  to enable default warnings:

  * Directly running the Python command::

       $ python3 -Wd scriptname.py

  * Add the option in the shebang line (something like ``#!/usr/bin/python3``)
    after the command::

       #!/usr/bin/python3 -Wd

* In your own scripts add a filter to ensure that *all* warnings are displayed:

   .. code-block:: python

       import warnings
       warnings.simplefilter("default")
       # Call your semver code

   For further details, see the section
   `Overriding the default filter <https://docs.python.org/3/library/warnings.html#overriding-the-default-filter>`_
   of the Python documentation.


.. _sec_creating_subclasses_from_versioninfo:

Creating Subclasses from Version
------------------------------------

If you do not like creating functions to modify the behavior of semver
(as shown in section :ref:`sec_dealing_with_invalid_versions`), you can
also create a subclass of the :class:`Version <semver.version.Version>` class.

For example, if you want to output a "v" prefix before a version,
but the other behavior is the same, use the following code:

.. literalinclude:: semverwithvprefix.py
   :language: python
   :lines: 4-


The derived class :class:`SemVerWithVPrefix` can be used like
the original class:

.. code-block:: python

     >>> v1 = SemVerWithVPrefix.parse("v1.2.3")
     >>> assert str(v1) == "v1.2.3"
     >>> print(v1)
     v1.2.3
     >>> v2 = SemVerWithVPrefix.parse("v2.3.4")
     >>> v2 > v1
     True
     >>> bad = SemVerWithVPrefix.parse("1.2.4")
     Traceback (most recent call last):
     ...
     ValueError: '1.2.4': not a valid semantic version tag. Must start with 'v' or 'V'
