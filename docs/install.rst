Installing semver
=================

.. meta::
   :description lang=en:
      Installing semver on the system

Release Policy
--------------

As semver uses `Semantic Versioning`_, breaking changes are only introduced in major
releases (incremented ``X`` in "X.Y.Z").
Refer to section :ref:`version-policy` for a general overview.

For users who want or need to stay with major 3 releases only, add the
following version restriction (:file:`setup.py`, :file:`requirements.txt`,
or :file:`pyproject.toml`)::

    semver>=3,<4

This line avoids surprises. You will get any updates within the major 3 release like 3.1.x and above. However, you will never get an update for semver 4.0.0.

For users who have to stay with major 2 releases only, use the following line::

    semver>=2,<3


With Pip
--------

.. code-block:: bash
   :name: install-pip

    pip3 install semver

If you want to install this specific version (for example, 3.0.0), use the command :command:`pip`
with an URL and its version:

.. parsed-literal::

    pip3 install git+https://github.com/python-semver/python-semver.git@3.0.0


With uv
-------

First, install the :command:`uv` command. Refer to https://docs.astral.sh/uv/getting-started/installation/ for more information.

Then use the command :command:`uv` to install the package:

.. code-block:: bash
   :name: install-uv

    uv pip install semver


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

    $ sudo zypper addrepo --refresh \
      --name devel_languages_python \
      "https://download.opensuse.org/repositories/devel:/languages:/python/\$releasever"

2. Install the package::

    $ sudo zypper install --repo devel_languages_python python3-semver


Ubuntu
^^^^^^

1. Update the package index::

    $ sudo apt-get update

2. Install the package::

    $ sudo apt-get install python3-semver


.. _semantic versioning: https://semver.org/
