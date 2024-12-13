.. _build-semver:

Building semver
===============

.. meta::
   :description lang=en:
      Building semver

.. _Installing uv: https://docs.astral.sh/uv/getting-started/installation/


This project changed its way how it is built over time. We used to have
a :file:`setup.py` file, but switched to a :file:`pyproject.toml` setup.

The build process is managed by :command:`uv` command.

You need:

* Python 3.7 or newer.

* The :mod:`setuptools` module version 61 or newer which is used as
  a build backend.

* The command :command:`uv` from Astral. Refer to the section
  `Installing uv`_  for more information.


To build semver, run::

    uv build

After the command is finished, you can find two files in the :file:`dist` folder: a ``.tar.gz`` and a ``.whl`` file.