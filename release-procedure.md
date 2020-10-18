# Release Procedure

The following procedures gives a short overview of what steps are needed to
create a new release.

## Prepare the Release

1. Verify that issues about new release are closed https://github.com/python-semver/python-semver/issues.

1. Verify that no pull requests that should be included in this release haven't been left out https://github.com/python-semver/python-semver/pulls.

1. Verify that continuous integration for latest build was passing https://travis-ci.com/python-semver/python-semver.

1. Create a new branch `release/VERSION`.

1. If one or several supported Python versions have been removed or added, verify that the 3 following files have been updated:
   * [setup.py](https://github.com/python-semver/python-semver/blob/master/setup.py)
   * [tox.ini](https://github.com/python-semver/python-semver/blob/master/tox.ini)
   * [.travis.yml](https://github.com/python-semver/python-semver/blob/master/.travis.yml)

1. Add eventually new contributor(s) to [CONTRIBUTORS](https://github.com/python-semver/python-semver/blob/master/CONTRIBUTORS).

1. Verify that `__version__` in [semver.py](https://github.com/python-semver/python-semver/blob/master/semver.py) have been updated and follow https://semver.org.

1. Show the new draft [CHANGELOG](https://github.com/python-semver/python-semver/blob/master/CHANGELOG.rst) entry for the latest release with:

       $ tox -e changelog

   Check the output. If you are not happy, update the files in the
   `changelog.d/` directory.
   If everything is okay, build the new `CHANGELOG` with:

       $ tox -e changelog -- build

1. Build the documentation and check the output:

       $ tox -e docs


## Create the New Release

1. Ensure that long description (ie [README.rst](https://github.com/python-semver/python-semver/blob/master/README.rst)) can be correctly rendered by Pypi using `restview --long-description`

1. Upload the wheel and source to TestPyPI first:

    ```bash
    $ git clean -xfd
    $ rm dist/*
    $ python3 setup.py sdist bdist_wheel
    $ twine upload --repository-url https://test.pypi.org/legacy/  dist/*
    ```

   If you have a `~/.pypirc` with a `testpyi` section, the upload can be
   simplified:

       $ twine upload --repository testpyi dist/*

1. Check if everything is okay with the wheel.

1. Upload to PyPI:

    ```bash
    $ git clean -xfd
    $ python setup.py register sdist bdist_wheel
    $ twine upload dist/*
    ```

1. Go to https://pypi.org/project/semver/ to verify that new version is online and the page is rendered correctly.

1. Tag commit and push to GitHub using command line interface:

    ```bash
    $ git tag -a x.x.x -m 'Version x.x.x'
    $ git push python-semver master --tags
    ```

1. In [GitHub Release page](https://github.com/python-semver/python-semver/release)
   document the new release.
   Usually it's enough to take it from a commit message or the tag description.

You're done! Celebrate!
