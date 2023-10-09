.. _testsuite:

Running the Test Suite
======================

.. meta::
   :description lang=en:
      Running the test suite through tox

We use `pytest`_ and `tox`_ to run tests against all supported Python
versions.  All test dependencies are resolved automatically.

You can decide to run the complete test suite or only part of it:

* To run all tests, use::

     $ tox

  If you have not all Python interpreters installed on your system
  it will probably give you some errors (``InterpreterNotFound``).
  To avoid such errors, use::

     $ tox --skip-missing-interpreters

  It is possible to use one or more specific Python versions. Use the ``-e``
  option and one or more abbreviations (``py37`` for Python 3.7,
  ``py38`` for Python 3.8 etc.)::

      $ tox -e py37
      $ tox -e py37,py38

  To get a complete list and a short description, run::

      $ tox -av

* To run only a specific test, pytest requires the syntax
  ``TEST_FILE::TEST_FUNCTION``.

  For example, the following line tests only the function
  :func:`test_immutable_major` in the file :file:`test_bump.py` for all
  Python versions::

      $ tox -e py37 -- tests/test_bump.py::test_should_bump_major

  By default, pytest prints only a dot for each test function. To
  reveal the executed test function, use the following syntax::

     $ tox -- -v

  You can combine the specific test function with the ``-e`` option, for
  example, to limit the tests for Python 3.7 and 3.8 only::

      $ tox -e py37,py38 -- tests/test_bump.py::test_should_bump_major

Our code is checked against formatting, style, type, and docstring issues
(`black`_, `flake8`_, `mypy`_, and `docformatter`_).
It is recommended to run your tests in combination with :command:`checks`,
for example::

   $ tox -e checks,py37,py38


.. _black: https://black.rtfd.io
.. _docformatter: https://pypi.org/project/docformatter/
.. _flake8: https://flake8.rtfd.io
.. _mypy: http://mypy-lang.org/
.. _pytest: http://pytest.org/
.. _tox: https://tox.rtfd.org/
