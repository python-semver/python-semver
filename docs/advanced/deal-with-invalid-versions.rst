.. _sec_dealing_with_invalid_versions:

Dealing with Invalid Versions
=============================

.. meta::
   :description lang=en:
      Dealing with invalid versions

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
