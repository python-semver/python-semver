#!/usr/bin/env python
from os.path import dirname, join
from setuptools import setup

import semver as package


def read_file(filename):
    """
    Read RST file and return content

    :param filename: the RST file
    :return: content of the RST file
    """
    with open(join(dirname(__file__), filename)) as f:
        return f.read()


setup(
    name=package.__name__,
    version=package.__version__,
    description=package.__doc__.strip(),
    long_description=read_file("README.rst"),
    long_description_content_type="text/x-rst",
    author=package.__author__,
    author_email=package.__author_email__,
    url="https://github.com/python-semver/python-semver",
    download_url="https://github.com/python-semver/python-semver/downloads",
    project_urls={
        "Documentation": "https://python-semver.rtfd.io",
        "Releases": "https://github.com/python-semver/python-semver/releases",
        "Bug Tracker": "https://github.com/python-semver/python-semver/issues",
    },
    py_modules=[package.__name__],
    include_package_data=True,
    license="BSD",
    classifiers=[
        # See https://pypi.org/pypi?%3Aaction=list_classifiers
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.5.*",
    tests_require=["tox", "virtualenv"],
    entry_points={"console_scripts": ["pysemver = semver:main"]},
)
