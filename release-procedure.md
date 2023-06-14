# Release Procedure

The following procedures gives a short overview of what steps are needed to
create a new release.

## Prepare the Release

1. Verify:

   * all issues for a new release are closed: <https://github.com/python-semver/python-semver/issues>.

   * that all pull requests that should be included in this release are merged: <https://github.com/python-semver/python-semver/pulls>.

   * that continuous integration for latest build was passing:
     <https://github.com/python-semver/python-semver/actions>.

1. Create a new branch `release/<VERSION>`.

1. If one or several supported Python versions have been removed or added, verify that the 3 following files have been updated:
   * `setup.cfg`
   * `tox.ini`
   * `.git/workflows/pythonpackage.yml`
   * `CITATION.cff`

1. Verify that the version has been updated and follow
   <https://semver.org>:

   * `src/semver/__about__.py`
   * `docs/usage/semver-version.rst`

1. Add eventually new contributor(s) to [CONTRIBUTORS](https://github.com/python-semver/python-semver/blob/master/CONTRIBUTORS).


1. Check if all changelog entries are created. If some are missing, [create them](https://python-semver.readthedocs.io/en/latest/development.html#adding-a-changelog-entry).

1. Show the new draft [CHANGELOG](https://github.com/python-semver/python-semver/blob/master/CHANGELOG.rst) entry for the latest release with:

       $ tox -e changelog

   Check the output. If you are not happy, update the files in the
   `changelog.d/` directory.
   If everything is okay, build the new `CHANGELOG` with:

       $ tox -e changelog -- build

1. Build the documentation and check the output:

       $ tox -e docs

1. Commit all changes, push, and create a pull request.


## Create the New Release

1. Ensure that long description ([README.rst](https://github.com/python-semver/python-semver/blob/master/README.rst)) can be correctly rendered by Pypi using `restview --long-description`

1. Clean up your local Git repository. Be careful,
   as it **will remove all files** which are not
   versioned by Git:

       $ git clean -xfd

   Before you create your distribution files, clean
   the directory too:

       $ rm dist/*

1. Create the distribution files (wheel and source):

       $ tox -e prepare-dist

1. Upload the wheel and source to TestPyPI first:

    ```bash    
    $ twine upload --repository-url https://test.pypi.org/legacy/  dist/*
    ```

   If you have a `~/.pypirc` with a `testpypi` section, the upload can be
   simplified:

       $ twine upload --repository testpypi dist/*

1. Check if everything is okay with the wheel.
   Check also the web site `https://test.pypi.org/project/<VERSION>/`

1. If everything looks fine, merge the pull request.

1. Upload to PyPI:

    ```bash
    $ git clean -xfd
    $ tox -e prepare-dist
    $ twine upload dist/*
    ```

1. Go to https://pypi.org/project/semver/ to verify that new version is online and the page is rendered correctly.

# Finish the release

1. Create a tag:

    ```bash
    $ git tag -a x.y.z
    ```

   It's recommended to use the generated Tox output
   from the Changelog.

1. Push the tag:

    ```bash
    $ git push origin x.y.z
    ```

1. In [GitHub Release page](https://github.com/python-semver/python-semver/release)
   document the new release.
   Select the tag from the last step and copy the
   content of the tag description into the release
   description.

1. Announce it in <https://github.com/python-semver/python-semver/discussions/categories/announcements>.

You're done! Celebrate!
