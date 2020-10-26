#!/usr/bin/env python3
# import semver as package
from os.path import dirname, join
from setuptools import setup
import re


VERSION_MATCH = re.compile(r"__version__ = ['\"]([^'\"]*)['\"]", re.M)


def read_file(filename):
    """
    Read RST file and return content

    :param filename: the RST file
    :return: content of the RST file
    """
    with open(join(dirname(__file__), filename)) as f:
        return f.read()


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta), META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


NAME = "semver"
META_FILE = read_file("semver.py")


# -----------------------------------------------------------------------------
setup(
    name=NAME,
    version=find_meta("version"),
    description=find_meta("description").strip(),
    long_description=read_file("README.rst"),
    long_description_content_type="text/x-rst",
    author=find_meta("author"),
    author_email=find_meta("author_email"),
    url="https://github.com/python-semver/python-semver",
    download_url="https://github.com/python-semver/python-semver/downloads",
    project_urls={
        "Documentation": "https://python-semver.rtfd.io",
        "Releases": "https://github.com/python-semver/python-semver/releases",
        "Bug Tracker": "https://github.com/python-semver/python-semver/issues",
    },
    py_modules=[NAME],
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
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        # "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6.*",
    tests_require=["tox", "virtualenv", "wheel"],
    entry_points={"console_scripts": ["pysemver = semver:main"]},
)
