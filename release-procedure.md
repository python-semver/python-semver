# Release Procedure

The following procedures gives a short overview of what steps are needed to
create a new release.

## Prepare your environment

1. Create your API tokens:

   1. From the [PyPI test server](https://test.pypi.org/manage/account/token/).

   1. From the official [PyPI server](https://test.pypi.org/manage/account/token/).

   1. Save both tokens it in a safe place like your password manager.

1. Create a file `~/.pypirc` with file mode 0600 and the following minimal content:

       # Protect the file with chmod 0600 ~/.pypirc
       [distutils]
       index-servers =
            test-semver
            semver

       [test-semver]
       repository = https://test.pypi.org/legacy/
       username = __token__
       password = <YOUR_TEST_API_TOKEN>

       [semver]
       repository = https://pypi.org/legacy/
       username = __token__
       password = <YOUR_API_TOKEN>

1. Install uv as shown in Astral's [Installing uv](https://docs.astral.sh/uv/getting-started/installation/) documentation.

1. Update the project's environment:

       uv sync --group devel

1. Activate your environment:

       source .venv/bin/activate

## Prepare the Release

1. Create a new branch `release/<VERSION>`.

1. If one or several supported **Python** versions have been removed or added, verify that the following files have been updated:
   * `pyproject.toml` (look into the key `project.requires-python` and `project.classifiers`)
   * `tox.ini`
   * `.git/workflows/pythonpackage.yml`
   * `CITATION.cff`

1. Verify that:

   * the version has been updated and follow <https://semver.org>:
        * `src/semver/__about__.py`
        * `docs/usage/semver-version.rst`

   * all issues for a new release are closed: <https://github.com/python-semver/python-semver/issues>.

   * all pull requests that should be included in this release are merged: <https://github.com/python-semver/python-semver/pulls>.

   * continuous integration for latest build was passing:
     <https://github.com/python-semver/python-semver/actions>.

1. Add eventually new contributor(s) to [CONTRIBUTORS](https://github.com/python-semver/python-semver/blob/master/CONTRIBUTORS).

1. Create the changelog:

    1. Check if all changelog entries are created. If some are missing, [create them](https://python-semver.readthedocs.io/en/latest/development.html#adding-a-changelog-entry).

    1. Show the new draft [CHANGELOG](https://github.com/python-semver/python-semver/blob/master/CHANGELOG.rst) entry for the latest release with:

           uvx tox r -e changelog

    1. Check the output. If you are not happy, update the files in the
    `changelog.d/` directory.
    If everything is okay, build the new `CHANGELOG` with:

           uvx tox r -e changelog -- build

1. Build the documentation and check the output:

       uvx tox r -e docs

1. Commit all changes, push, and create a pull request.


## Create the New Release

1. Ensure that long description ([README.rst](https://github.com/python-semver/python-semver/blob/master/README.rst)) can be correctly rendered by Pypi using `uvx restview -b README.rst`

1. Clean up your local Git repository. Be careful,
   as it **will remove all files** which are not
   versioned by Git:

       git clean -xfd

   Before you create your distribution files, clean
   the directory too:

       rm dist/*

1. Create the distribution files (wheel and source):

       uvx tox r -e prepare-dist

1. Upload the wheel and source to TestPyPI first:

       twine upload --verbose --repository test-semver dist/*

   (Normally you would do it with `uv publish`, but for some unknown reason it didn't work for me.)

1. Check if everything is okay with the wheel.
   Check also the web site `https://test.pypi.org/project/<VERSION>/`

# Finish the release

1. If everything looks fine, merge the pull request.

1. Upload to PyPI:

       $ git clean -xfd
       $ tox r -e prepare-dist
       $ twine upload --verbose --repository semver dist/*

1. Go to https://pypi.org/project/semver/ to verify that new version is online and the page is rendered correctly.

1. Create a tag:

       git tag -a x.y.z

   It's recommended to use the generated Tox output from the Changelog.

1. Push the tag:

       git push origin x.y.z

1. In [GitHub Release page](https://github.com/python-semver/python-semver/release) document the new release.
   Select the tag from the last step and copy the content of the tag description into the release description.

1. Announce it in <https://github.com/python-semver/python-semver/discussions/categories/announcements>.

You're done! Celebrate!
