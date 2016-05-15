Semver |latest-version|
=======================

|build-status| |python-support| |downloads| |license|

A Python module for `semantic versioning`_. Simplifies comparing versions.


.. |latest-version| image:: https://img.shields.io/pypi/v/semver.svg
   :alt: Latest version on PyPI
   :target: https://pypi.python.org/pypi/semver
.. |build-status| image:: https://travis-ci.org/k-bx/python-semver.svg?branch=master
   :alt: Build status
   :target: https://travis-ci.org/k-bx/python-semver
.. |python-support| image:: https://img.shields.io/pypi/pyversions/semver.svg
   :target: https://pypi.python.org/pypi/semver
   :alt: Python versions
.. |downloads| image:: https://img.shields.io/pypi/dm/semver.svg
   :alt: Monthly downloads from PyPI
   :target: https://pypi.python.org/pypi/semver
.. |license| image:: https://img.shields.io/pypi/l/semver.svg
   :alt: Software license
   :target: https://github.com/k-bx/python-semver/blob/master/LICENSE.txt
.. _semantic versioning: http://semver.org/

Usage
-----

This module provides just couple of functions, main of which are:

.. code-block:: python

    >>> import semver
    >>> semver.compare("1.0.0", "2.0.0")
    -1
    >>> semver.compare("2.0.0", "1.0.0")
    1
    >>> semver.compare("2.0.0", "2.0.0")
    0
    >>> semver.match("2.0.0", ">=1.0.0")
    True
    >>> semver.match("1.0.0", ">1.0.0")
    False
    >>> semver.format_version(3, 4, 5, 'pre.2', 'build.4')
    '3.4.5-pre.2+build.4'
    >>> semver.bump_major("3.4.5")
    '4.0.0'
    >>> semver.bump_minor("3.4.5")
    '3.5.0'
    >>> semver.bump_patch("3.4.5")
    '3.4.6'
    >>> semver.max_ver("1.0.0", "2.0.0")
    '2.0.0'
    >>> semver.min_ver("1.0.0", "2.0.0")
    '1.0.0'

Installation
------------

For Python 2:

.. code-block:: bash

    pip install semver

For Python 3:

.. code-block:: bash

    pip3 install semver

How to Contribute
-----------------

When you make changes to the code please run the tests before pushing your
code to your fork and opening a `pull request`_:

.. code-block:: bash

    python setup.py test

We use `py.test`_ and `tox`_ to run tests against all supported Python
versions.  All test dependencies are resolved automatically, apart from
virtualenv, which for the moment you still may have to install manually:

.. code-block:: bash

    pip install "virtualenv<14.0.0"  # <14.0.0 needed for Python 3.2 only

You can use the ``clean`` command to remove build and test files and folders:

.. code-block:: bash

    python setup.py clean


.. _pull request: https://github.com/k-bx/python-semver/pulls
.. _py.test: http://pytest.org/
.. _tox: http://tox.testrun.org/
