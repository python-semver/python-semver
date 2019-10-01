Contributing to semver
======================

When you make changes to the code please run the tests before pushing your
code to your fork and opening a `pull request`_:

.. code-block:: bash

    python setup.py test

We use `pytest`_ and `tox`_ to run tests against all supported Python
versions.  All test dependencies are resolved automatically, apart from
virtualenv, which for the moment you still may have to install manually:

.. code-block:: bash

    pip install "virtualenv<14.0.0"  # <14.0.0 needed for Python 3.2 only

You can use the ``clean`` command to remove build and test files and folders:

.. code-block:: bash

    python setup.py clean


.. _pull request: https://github.com/k-bx/python-semver/pulls
.. _pytest: http://pytest.org/
.. _tox: http://tox.testrun.org/
