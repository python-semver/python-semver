Release Procedure
=================

.. meta::
   :description lang=en:
      Release procedure: prepare and create the release

The following procedures gives a short overview of what steps are needed
to create a new release.

These steps are interesting for the release manager only.


Prepare the Release
-------------------

1. Verify that:

   -  all issues for a new release are closed:
      https://github.com/python-semver/python-semver/issues.

   -  all pull requests that should be included in this release are
      merged: https://github.com/python-semver/python-semver/pulls.

   -  continuous integration for latest build was passing:
      https://github.com/python-semver/python-semver/actions.

2. Create a new branch ``release/<VERSION>``.

3. If one or several supported Python versions have been removed or
   added, verify that the following files have been updated:

   - :file:`setup.cfg`
   - :file:`tox.ini`
   - :file:`.git/workflows/pythonpackage.yml`
   - :file:`.github/workflows/python-testing.yml`

4. Verify that the version in file :file:`src/semver/__about__.py`
   has been updated and follows the `Semver <https://semver.org>`_
   specification.

5. Add eventually new contributor(s) to
   `CONTRIBUTORS <https://github.com/python-semver/python-semver/blob/master/CONTRIBUTORS>`_.

6. Check if all changelog entries are created. If some are missing,
   `create
   them <https://python-semver.readthedocs.io/en/latest/development.html#adding-a-changelog-entry>`__.

7. Show the new draft
   `CHANGELOG <https://github.com/python-semver/python-semver/blob/master/CHANGELOG.rst>`_ entry for the latest release with:

   ::

      $ tox -e changelog

   Check the output. If you are not happy, update the files in the
   ``changelog.d/`` directory. If everything is okay, build the new
   ``CHANGELOG`` with:

   ::

      $ tox -e changelog -- build

8. Build the documentation and check the output:

   ::

      $ tox -e docs

9. Commit all changes, push, and create a pull request.

Create the New Release
----------------------

1. Ensure that long description
   (`README.rst <https://github.com/python-semver/python-semver/blob/master/README.rst>`_)
   can be correctly rendered by Pypi using
   ``restview --long-description``

2. Clean up your local Git repository. Be careful, as it **will remove
   all files** which are not versioned by Git:

   ::

      $ git clean -xfd

   Before you create your distribution files, clean the directory too:

   ::

      $ rm dist/*

3. Create the distribution files (wheel and source):

   ::

      $ tox -e prepare-dist

4. Upload the wheel and source to TestPyPI first:

   .. code:: bash

      $ twine upload --repository-url https://test.pypi.org/legacy/  dist/*

   If you have a ``~/.pypirc`` with a ``testpypi`` section, the upload
   can be simplified:

   ::

      $ twine upload --repository testpypi dist/*

5. Check if everything is okay with the wheel. Check also the web site
   ``https://test.pypi.org/project/<VERSION>/``

6. If everything looks fine, merge the pull request.

7. Upload to PyPI:

   .. code:: bash

      $ git clean -xfd
      $ tox -e prepare-dist
      $ twine upload dist/*

8. Go to https://pypi.org/project/semver/ to verify that new version is
   online and the page is rendered correctly.

