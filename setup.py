# -*- coding: utf-8 -*-

from distutils.core import setup

with open('README.rst') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='semver',
    version='0.0.2',
    description='Python package to work with Semantic Versioning (http://semver.org/)',
    long_description=LONG_DESCRIPTION,
    author='Konstantine Rybnikov',
    author_email='k-bx@k-bx.com',
    url='https://github.com/k-bx/python-semver',
    download_url='https://github.com/k-bx/python-semver/downloads',
    py_modules=['semver'],
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
