Contributing to semver
======================

The semver source code is managed using Git and is hosted on GitHub::

   git clone git://github.com/k-bx/python-semver


Reporting Bugs and Feedback
---------------------------

If you think you have encountered a bug in semver or have an idea for a new
feature? Great! We like to hear from you.

First, take the time to look into our GitHub `issues`_ tracker if
this already covered. If not, changes are good that we avoid double work.


Fixing Bugs and Implementing New Features
-----------------------------------------

Before you make changes to the code, we would highly appreciate if you
consider the following general requirements:

* Make sure your code adheres to the `Semantic Versioning`_ specification.

* Check if your feature is covered by the Semantic Versioning specification.
  If not, ask on its GitHub project https://github.com/semver/semver.

* Write test cases if you implement a new feature.

* Test also for side effects of your new feature and run the complete
  test suite.

* Document the new feature, see :ref:`doc` for details.


Modifying the Code
------------------

We recommend the following workflow:

#. Fork our project on GitHub using this link:
   https://github.com/k-bx/python-semver/fork

#. Clone your forked Git repository (replace ``GITHUB_USER`` with your
   account name on GitHub)::

    $ git clone git@github.com:GITHUB_USER/python-semver.git

#. Create a new branch. You can name your branch whatever you like, but we
   recommend to use some meaningful name. If your fix is based on a
   existing GitHub issue, add also the number. Good examples would be:

   * ``feature/123-improve-foo`` when implementing a new feature in issue 123
   * ``bugfix/234-fix-security-bar`` a bugfixes for issue 234

   Use this :command:`git` command::

   $ git checkout -b feature/NAME_OF_YOUR_FEATURE

#. Work on your branch. Commit your work.

#. Write test cases and run the test suite, see :ref:`testsuite` for details.

#. Create a `pull request`_. Describe in the pull request what you did
   and why. If you have open questions, ask.

#. Wait for feedback. If you receive any comments, address these.

#. After your pull request got accepted, delete your branch.

#. Use the ``clean`` command to remove build and test files and folders::

   $ python setup.py clean


.. _testsuite:

Running the Test Suite
----------------------

We use `pytest`_ and `tox`_ to run tests against all supported Python
versions.  All test dependencies are resolved automatically.

You can decide to run the complete test suite or only part of it:

* To run all tests, use::

     $ tox

  If you have not all Python interpreters installed on your system
  it will probably give you some errors (``InterpreterNotFound``).
  To avoid such errors, use::

     $ tox --skip-missing-interpreters

  It is possible to use only specific Python versions. Use the ``-e``
  option and one or more abbreviations (``py27`` for Python 2.7, ``py34`` for
  Python 3.4 etc.)::

      $ tox -e py34
      $ tox -e py27,py34

  To get a complete list, run::

      $ tox -l

* To run only a specific test, pytest requires the syntax
  ``TEST_FILE::TEST_FUNCTION``.

  For example, the following line tests only the function
  :func:`test_immutable_major` in the file :file:`test_semver.py` for all
  Python versions::

      $ tox test_semver.py::test_immutable_major

  By default, pytest prints a dot for each test function only. To
  reveal the executed test function, use the following syntax::

     $ tox -- -v

  You can combine the specific test function with the ``-e`` option, for
  example, to limit the tests for Python 2.7 and 3.6 only::

      $ tox -e py27,py36 test_semver.py::test_immutable_major

Our code is checked against `flake8`_ for style guide issues. It is recommended
to run your tests in combination with :command:`flake8`, for example::

   $ tox -e py27,py36,flake8


.. _doc:

Documenting semver
------------------

Documenting the features of semver is very important. It gives our developers
an overview what is possible with semver, how it "feels", and how it is
used efficiently.

.. note::

    To build the documentation locally use the following command::

      $ tox -e docs

    The built documentation is available in :file:`dist/docs`.


A new feature is *not* complete if it isn't proberly documented. A good
documentation includes:

  * **A docstring**

    Each docstring contains a summary line, a linebreak, the description
    of its arguments in `Sphinx style`_, and an optional doctest.
    The docstring is extracted and reused in the :ref:`api` section.
    An appropriate docstring should look like this::

        def compare(ver1, ver2):
            """Compare two versions

            :param ver1: version string 1
            :param ver2: version string 2
            :return: The return value is negative if ver1 < ver2,
                    zero if ver1 == ver2 and strictly positive if ver1 > ver2
            :rtype: int

            >>> semver.compare("1.0.0", "2.0.0")
            -1
            >>> semver.compare("2.0.0", "1.0.0")
            1
            >>> semver.compare("2.0.0", "2.0.0")
            0
            """

  * **The documentation**

    A docstring is good, but in most cases it's too dense. Describe how
    to use your new feature in our documentation. Here you can give your
    readers more examples, describe it in a broader context or show
    edge cases.


.. _flake8: https://flake8.readthedocs.io
.. _issues:  https://github.com/k-bx/python-semver/issues
.. _pull request: https://github.com/k-bx/python-semver/pulls
.. _pytest: http://pytest.org/
.. _Semantic Versioning: https://semver.org
.. _Sphinx style: https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html
.. _tox: https://tox.readthedocs.org/
