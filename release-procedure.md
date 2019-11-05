#################
Release procedure
#################

* Verify that issues about new release are closed https://github.com/python-semver/python-semver/issues and verify that no pull requests that should be included in this release haven't been left out https://github.com/python-semver/python-semver/pulls

* Verify that continuous integration for latest build was passing https://travis-ci.com/python-semver/python-semver

* Verify that `__version__` in [semver.py](https://github.com/python-semver/python-semver/blob/master/semver.py) have been updated and follow https://semver.org/

* Verify that [CHANGELOG](https://github.com/python-semver/python-semver/blob/master/CHANGELOG.rst) have been updated. No WIP should be present in CHANGELOG during release!

* If one or several supported Python versions have been removed or added, verify that the 3 following files have been updated:
  * [setup.py](https://github.com/python-semver/python-semver/blob/master/setup.py)
  * [tox.ini](https://github.com/python-semver/python-semver/blob/master/tox.ini)
  * [.travis.yml](https://github.com/python-semver/python-semver/blob/master/.travis.yml)

* Verify that doc reflecting new changes have been updated and are available at https://python-semver.readthedocs.io/en/latest/ If necessary, trigger doc build at https://readthedocs.org/projects/python-semver/

* Add eventually new contributor(s) to [CONTRIBUTORS](https://github.com/python-semver/python-semver/blob/master/CONTRIBUTORS)

* Ensure that long description (ie [README.rst](https://github.com/python-semver/python-semver/blob/master/README.rst)) can be correctly rendered by Pypi using `restview --long-description`

* Upload to PyPI

```bash
git clean -xfd
python setup.py register sdist bdist_wheel --universal
twine upload dist/*
```

* Go to https://pypi.org/project/semver/ to verify that new version is online and page is rendered correctly

* Tag commit and push to github using command line interface

```bash
git tag -a x.x.x -m 'Version x.x.x'
git push python-semver master --tags
```

or using GitHub web interface available at https://github.com/python-semver/python-semver/releases
