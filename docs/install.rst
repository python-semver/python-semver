Installing semver
=================

Release Policy
--------------

As semver uses `Semantic Versioning`_, breaking changes are only introduced in major
releases (incremented ``X`` in "X.Y.Z").

For users who want to stay with major 2 releases only, add the following version
restriction::

    semver>=2,<3

This line avoids surprises. You will get any updates within the major 2 release like
2.11.0 or above. However, you will never get an update for semver 3.0.0.

Keep in mind, as this line avoids any major version updates, you also will never
get new exciting features or bug fixes.

You can add this line in your file :file:`setup.py`, :file:`requirements.txt`, or any other
file that lists your dependencies.

Pip
---

.. code-block:: bash

    pip3 install semver

If you want to install this specific version (for example, 2.10.0), use the command :command:`pip`
with an URL and its version:

.. parsed-literal::

    pip3 install git+https://github.com/python-semver/python-semver.git@2.11.0


Linux Distributions
-------------------

.. note::

   Some Linux distributions can have outdated packages.
   These outdated packages does not contain the latest bug fixes or new features.
   If you need a newer package, you have these option:

    * Ask the maintainer to update the package.
    * Update the package for your favorite distribution and submit it.
    * Use a Python virtual environment and :command:`pip install`.


Arch Linux
^^^^^^^^^^

1. Enable the community repositories first:

   .. code-block:: ini

      [community]
      Include = /etc/pacman.d/mirrorlist

2. Install the package::

    $ pacman -Sy python-semver


Debian
^^^^^^

1. Update the package index::

    $  sudo apt-get update

2. Install the package::

    $ sudo apt-get install python3-semver


Fedora
^^^^^^

.. code-block:: bash

    $ dnf install python3-semver


FreeBSD
^^^^^^^

.. code-block:: bash

    $ pkg install py36-semver

openSUSE
^^^^^^^^

1. Enable the ``devel:languages:python`` repository of the Open Build Service::

    $ sudo zypper addrepo --refresh obs://devel:languages:python devel_languages_python

2. Install the package::

    $ sudo zypper install --repo devel_languages_python python3-semver


Ubuntu
^^^^^^

1. Update the package index::

    $ sudo apt-get update

2. Install the package::

    $ sudo apt-get install python3-semver


.. _semantic versioning: http://semver.org/
