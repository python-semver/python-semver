#!/usr/bin/env python
import semver as package
from glob import glob
from os import remove
from os.path import dirname, join
from setuptools import setup
from setuptools.command.test import test as TestCommand

try:
    from setuptools.command.clean import clean as CleanCommand
except ImportError:
    from distutils.command.clean import clean as CleanCommand
from shlex import split
from shutil import rmtree


class Tox(TestCommand):
    user_options = [("tox-args=", "a", "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        from tox import cmdline

        args = self.tox_args
        if args:
            args = split(self.tox_args)
        errno = cmdline(args=args)
        exit(errno)


class Clean(CleanCommand):
    def run(self):
        CleanCommand.run(self)
        delete_in_root = ["build", ".cache", "dist", ".eggs", "*.egg-info", ".tox"]
        delete_everywhere = ["__pycache__", "*.pyc"]
        for candidate in delete_in_root:
            rmtree_glob(candidate)
        for visible_dir in glob("[A-Za-z0-9]*"):
            for candidate in delete_everywhere:
                rmtree_glob(join(visible_dir, candidate))
                rmtree_glob(join(visible_dir, "*", candidate))


def rmtree_glob(file_glob):
    for fobj in glob(file_glob):
        try:
            rmtree(fobj)
            print("%s/ removed ..." % fobj)
        except OSError:
            try:
                remove(fobj)
                print("%s removed ..." % fobj)
            except OSError:
                pass


def read_file(filename):
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
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    tests_require=["tox", "virtualenv"],
    cmdclass={"clean": Clean, "test": Tox},
    entry_points={"console_scripts": ["pysemver = semver:main"]},
)
