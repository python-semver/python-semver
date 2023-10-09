.. _version-policy:

Version Policy
==============

.. |MAINT| replace:: ``maint/v2``
.. _MAINT: https://github.com/python-semver/python-semver/tree/maint/v2
.. |CHANGELOG| replace:: ``Changelog``
.. _CHANGELOG: https://github.com/python-semver/python-semver/blob/maint/v2/CHANGELOG.rst

The move from v2 to v3 introduced many changes and deprecated module functions.
The main functionality is handled by the :class:`~semver.version.Version` class
now. Find more information in the section :ref:`semver2-to-3`.


semver Version 2
----------------

Active development of major version 2 has stopped. No new features nor
backports will be integrated.
We recommend to upgrade your workflow to Python 3 to gain support,
bugfixes, and new features.

If you still need this old version, use the  |MAINT|_ branch. There you
can look for the |CHANGELOG|_ if you need some details about the history.


semver Version 3
----------------

We will not intentionally make breaking changes in minor releases of V3.

Methods marked as ``deprecated`` raise a warning message when used from the
:py:mod:`python:warnings` module.
Refer to section :ref:`sec_display_deprecation_warnings` to get more information about how to customize it.
Check section :ref:`sec_replace_deprecated_functions` to make your code
ready for future major releases.


semver Version 3 and beyond
---------------------------

Methods that were marked as deprecated will be very likely be removed.


Support for Python versions
---------------------------

This project will drop support for a Python version when the
following conditions are met:

* The Python version has reached `EOL <https://devguide.python.org/versions/>`_.
