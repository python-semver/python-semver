* Verify that `__version__` in [semver.py](https://github.com/k-bx/python-semver/blob/master/semver.py) have been updated
* Verify that [CHANGELOG](https://github.com/k-bx/python-semver/blob/master/CHANGELOG) have been updated
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
