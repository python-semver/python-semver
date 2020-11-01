.. _contributing:

Contributing to semver
======================

The semver source code is managed using Git and is hosted on GitHub::

   git clone git://github.com/python-semver/python-semver


Reporting Bugs and Feedback
---------------------------

If you think you have encountered a bug in semver or have an idea for a new
feature? Great! We like to hear from you.

First, take the time to look into our GitHub `issues`_ tracker if
this already covered. If not, changes are good that we avoid double work.


Prerequisites
-------------

Before you make changes to the code, we would highly appreciate if you
consider the following general requirements:

* Make sure your code adheres to the `Semantic Versioning`_ specification.

* Check if your feature is covered by the Semantic Versioning specification.
  If not, ask on its GitHub project https://github.com/semver/semver.



Modifying the Code
------------------

We recommend the following workflow:

#. Fork our project on GitHub using this link:
   https://github.com/python-semver/python-semver/fork

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

#. Work on your branch and create a pull request:

   a. Write test cases and run the complete test suite, see :ref:`testsuite`
      for details.

   b. Write a changelog entry, see section :ref:`changelog`.

   c. If you have implemented a new feature, document it into our
      documentation to help our reader. See section :ref:`doc` for
      further details.

   d. Create a `pull request`_. Describe in the pull request what you did
      and why. If you have open questions, ask.

#. Wait for feedback. If you receive any comments, address these.

#. After your pull request got accepted, delete your branch.


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

  It is possible to use one or more specific Python versions. Use the ``-e``
  option and one or more abbreviations (``py36`` for Python 3.6, ``py37`` for
  Python 3.7 etc.)::

      $ tox -e py36
      $ tox -e py36,py37

  To get a complete list and a short description, run::

      $ tox -av

* To run only a specific test, pytest requires the syntax
  ``TEST_FILE::TEST_FUNCTION``.

  For example, the following line tests only the function
  :func:`test_immutable_major` in the file :file:`test_bump.py` for all
  Python versions::

      $ tox -e py36 -- tests/test_bump.py::test_should_bump_major

  By default, pytest prints only a dot for each test function. To
  reveal the executed test function, use the following syntax::

     $ tox -- -v

  You can combine the specific test function with the ``-e`` option, for
  example, to limit the tests for Python 3.6 and 3.7 only::

      $ tox -e py36,py37 -- tests/test_bump.py::test_should_bump_major

Our code is checked against formatting, style, type, and docstring issues
(`black`_, `flake8`_, `mypy`_, and `docformatter`_).
It is recommended to run your tests in combination with :command:`checks`,
for example::

   $ tox -e checks,py36,py37


.. _doc:

Documenting semver
------------------

Documenting the features of semver is very important. It gives our developers
an overview what is possible with semver, how it "feels", and how it is
used efficiently.

.. note::

    To build the documentation locally use the following command::

      $ tox -e docs

    The built documentation is available in :file:`docs/_build/html`.


A new feature is *not* complete if it isn't proberly documented. A good
documentation includes:

  * **A docstring**

    Each docstring contains a summary line, a linebreak, an optional
    directive (see next item), the description of its arguments in
    `Sphinx style`_, and an optional doctest.
    The docstring is extracted and reused in the :ref:`api` section.
    An appropriate docstring should look like this::

         def to_tuple(self) -> VersionTuple:
            """
            Convert the Version object to a tuple.

            .. versionadded:: 2.10.0
               Renamed ``VersionInfo._astuple`` to ``VersionInfo.to_tuple`` to
               make this function available in the public API.

            :return: a tuple with all the parts

            >>> semver.Version(5, 3, 1).to_tuple()
            (5, 3, 1, None, None)
            """

  * **An optional directive**

    If you introduce a new feature, change a function/method, or remove something,
    it is a good practice to introduce Sphinx directives into the docstring.
    This gives the reader an idea what version is affected by this change.

    The first required argument, ``VERSION``, defines the version when this change
    was introduced. You can choose from:

    * ``.. versionadded:: VERSION``

      Use this directive to describe a new feature.

    * ``.. versionchanged:: VERSION``

      Use this directive to describe when something has changed, for example,
      new parameters were added, changed side effects, different return values, etc.

    * ``.. deprecated:: VERSION``

      Use this directive when a feature is deprecated. Describe what should
      be used instead, if appropriate.


    Add such a directive *after* the summary line, as shown above.

  * **The documentation**

    A docstring is good, but in most cases it's too dense. API documentation
    cannot replace a good user documentation. Describe how
    to use your new feature in our documentation. Here you can give your
    readers more examples, describe it in a broader context or show
    edge cases.


.. _changelog:

Adding a Changelog Entry
------------------------

.. include:: ../changelog.d/README.rst
    :start-after: -text-begin-


.. _black: https://black.rtfd.io
.. _docformatter: https://pypi.org/project/docformatter/
.. _flake8: https://flake8.rtfd.io
.. _mypy: http://mypy-lang.org/
.. _issues:  https://github.com/python-semver/python-semver/issues
.. _pull request: https://github.com/python-semver/python-semver/pulls
.. _pytest: http://pytest.org/
.. _Semantic Versioning: https://semver.org
.. _Sphinx style: https://sphinx-rtd-tutorial.rtfd.io/en/latest/docstrings.html
.. _tox: https://tox.rtfd.org/

