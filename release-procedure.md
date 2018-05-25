* Verify that latest build was passing https://travis-ci.org/k-bx/python-semver

* Verify that `__version__` in [semver.py](https://github.com/k-bx/python-semver/blob/master/semver.py) have been updated and follow https://semver.org/

* Verify that [CHANGELOG](https://github.com/k-bx/python-semver/blob/master/CHANGELOG) have been updated

* If one or several supported Python versions have been removed or added, verify that the 3 following files have been updated:
  * [setup.py](https://github.com/k-bx/python-semver/blob/master/setup.py)
  * [tox.ini](https://github.com/k-bx/python-semver/blob/master/tox.ini)
  * [.travis.yml](https://github.com/k-bx/python-semver/blob/master/.travis.yml)

* Verify that doc reflecting new changes have been updated

* Add eventually new contributor(s) to [CONTRIBUTORS](https://github.com/k-bx/python-semver/blob/master/CONTRIBUTORS)

* Tag commit and push to github using command line interface
```bash
git tag -a x.x.x -m 'Version x.x.x'
git push python-semver master --tags
```
or using GitHub web interface available at https://github.com/k-bx/python-semver/releases

* Upload to PyPI

```bash
git clean -xfd
python setup.py register sdist bdist_wheel --universal
twine upload dist/*
```

* Go to https://pypi.org/project/semver/ to verify that new version is online and page is rendered correctly

