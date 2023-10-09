.. _sec.getitem.parts:

Accessing Parts Through Index Numbers
=====================================

.. meta::
   :description lang=en:
      Accessing parts through index numbers

.. versionadded:: 2.10.0

Another way to access parts of a version is to use an index notation. The underlying
:class:`~semver.version.Version` object allows to access its data through
the magic method :meth:`~semver.version.Version.__getitem__`.

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

Negative numbers or undefined parts raise an :py:exc:`python:IndexError` exception:

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
