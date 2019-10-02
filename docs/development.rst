Contributing to semver
======================

Do you want to contribute? Great! We would like to give you some
helpful tips and tricks.
When you make changes to the code, we would greatly appreciate if you
consider the following requirements:

* Make sure your code adheres to the `Semantic Versioning`_ specification.

* Check if your feature is covered by the Semantic Versioning specification.
  If not, ask on its GitHub project https://github.com/semver/semver.

* Write test cases if you implement a new feature.

* Test also for side effects of your new feature and run the complete
  test suite.
* Document the new feature.

We use `pytest`_ and `tox`_ to run tests against all supported Python
versions.  All test dependencies are resolved automatically, apart from
virtualenv, which for the moment you still may have to install manually:

.. code-block:: bash

    pip install "virtualenv<14.0.0"  # <14.0.0 needed for Python 3.2 only

We recommend to use the following workflow if you would like to contribute:

1. Fork our project on GitHub using this link:
   https://github.com/k-bx/python-semver/fork

2. Clone your forked Git repository (replace ``GITHUB_USER`` with your
   account name on GitHub)::

    $ git clone git@github.com:GITHUB_USER/python-semver.git

3. Create a new branch. You can name your branch whatever you like, but we
   recommend to use some meaningful name. If your fix is based on a
   existing GitHub issue, add also the number. Good examples would be:

   * ``feature/123-improve-foo`` when implementing a new feature
   * ``bugfix/123-fix-security-bar`` when dealing with bugfixes

   Use this :command:`git` command::

   $ git checkout -b feature/NAME_OF_YOUR_FEATURE

4. Work on your branch. Commit your work. Don't forget to write test cases
   for your new feature.

5. Run the test suite. You can decide to run the complete test suite or
   only part of it:

   * To run all tests, use::

     $ tox

    If you have not all Python interpreters installed on your system
    it will probably give you some errors. To avoid such errors, use::

     $ tox --skip-missing-interpreters

   * To run a test for a specific Python version, use the
     :command:`tox` command, for example, for Python 3.6::

      $ tox -e py36

6. Create a `pull request`_. Describe in the pull request what you did
   and why. If you have open questions, ask.

7. Wait for feedback. If you receive any comments, address these.

8. After your pull request got accepted, delete your branch.

9. Use the ``clean`` command to remove build and test files and folders::

   $ python setup.py clean


.. _pull request: https://github.com/k-bx/python-semver/pulls
.. _pytest: http://pytest.org/
.. _tox: https://tox.readthedocs.org/
.. _Semantic Versioning: https://semver.org
