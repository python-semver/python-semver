Installing semver
=================


Pip
---

For Python 2:

.. code-block:: bash

    pip install semver

For Python 3:

.. code-block:: bash

    pip3 install semver

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

1. Enable the the ``devel:languages:python`` repository on the Open Build Service (replace ``<VERSION>`` with the preferred openSUSE release)::

    $ zypper addrepo https://download.opensuse.org/repositories/devel:/languages:/python/openSUSE_Leap_<VERSION>/devel:languages:python.repo

2. Install the package::

    $ zypper --repo devel_languages_python python3-semver


Ubuntu
^^^^^^

1. Update the package index::

    $ sudo apt-get update

2. Install the package::

    $ sudo apt-get install python3-semver
