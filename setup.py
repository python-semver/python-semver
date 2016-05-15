#!/usr/bin/env python
from setuptools import setup
from setuptools.command.test import test as TestCommand
from shlex import split


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

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


def read_file(filename):
    with open(filename) as f:
        return f.read()

setup(
    name='semver',
    version='2.4.1',
    description='Python helper for Semantic Versioning (http://semver.org/)',
    long_description=read_file('README.rst'),
    author='Konstantine Rybnikov',
    author_email='k-bx@k-bx.com',
    url='https://github.com/k-bx/python-semver',
    download_url='https://github.com/k-bx/python-semver/downloads',
    py_modules=['semver'],
    include_package_data=True,
    license='BSD',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    tests_require=['tox', 'virtualenv<14.0.0'],
    cmdclass={
        'test': Tox,
    },
)
