Semver -- python module for semantic versioning
===============================================

![Travis CI](https://travis-ci.org/k-bx/python-semver.svg?branch=master)

Simple module for comparing versions as noted at [semver.org](http://semver.org/).

This module provides just couple of functions, main of which are:

```python
>>> import semver
>>> semver.compare("1.0.0", "2.0.0")
-1
>>> semver.compare("2.0.0", "1.0.0")
1
>>> semver.compare("2.0.0", "2.0.0")
0
>>> semver.match("2.0.0", ">=1.0.0")
True
>>> semver.match("1.0.0", ">1.0.0")
False
```

Installation
------------

For Python 2:

```
pip install semver
```

For Python 3:

```
pip3 install semver
```

Homepage at PyPi: https://pypi.python.org/pypi/semver
