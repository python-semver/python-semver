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

  The configured ``skip_missing_interpreters`` option skips Python
  interpreters that are not installed on your system.

  It is possible to use one or more specific Python versions. Use the ``-e``
  option and one or more abbreviations (``py311`` for Python 3.11,
  ``py312`` for Python 3.12 etc.)::

      $ tox -e py311
      $ tox -e py311,py312

  To get a complete list and a short description, run::

      $ tox -av

* To run only a specific test, pytest requires the syntax
  ``TEST_FILE::TEST_FUNCTION``.

  For example, the following line tests only the function
  ``test_should_bump_major`` in the file :file:`test_bump.py` using Python 3.11::

      $ tox -e py311 -- tests/test_bump.py::test_should_bump_major

  By default, pytest prints only a dot for each test function. To
  reveal the executed test function, use the following syntax::

     $ tox -- -v

  You can combine the specific test function with the ``-e`` option, for
  example, to limit the tests for Python 3.11 and 3.12 only::

      $ tox -e py311,py312 -- tests/test_bump.py::test_should_bump_major

The ``checks`` environment runs `Ruff`_ for code-style checks. The
``mypy`` and ``docstrings`` environments run `mypy`_ and `docformatter`_,
respectively.

It is recommended to run code-style checks together with the tests, for example::

   $ tox -e checks,py311,py312


.. _Ruff: https://docs.astral.sh/ruff/
.. _docformatter: https://pypi.org/project/docformatter/
.. _mypy: http://mypy-lang.org/
.. _pytest: http://pytest.org/
.. _tox: https://tox.rtfd.org/
