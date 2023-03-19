.. _build-semver:

Building semver
===============


.. _PEP 517: https://www.python.org/dev/peps/pep-0517/
.. _PEP 621: https://www.python.org/dev/peps/pep-0621/
.. _A Practical Guide to Setuptools and Pyproject.toml: https://godatadriven.com/blog/a-practical-guide-to-setuptools-and-pyproject-toml/
.. _Declarative config: https://setuptools.rtfd.io/en/latest/userguide/declarative_config.html


This project changed slightly its way how it is built. The reason for this
was to still support the "traditional" way with :command:`setup.py`,
but at the same time try out the newer way with :file:`pyproject.toml`.
As Python 3.6 got deprecated, this project does support from now on only
:file:`pyproject.toml`.


Background information
----------------------

Skip this section and head over to :ref:`build-pyproject-build` if you just
want to know how to build semver.
This section gives some background information how this project is set up.

The traditional way with :command:`setup.py` in this project uses a
`Declarative config`_. With this approach, the :command:`setup.py` is
stripped down to its bare minimum and all the metadata is stored in
:file:`setup.cfg`.

The new :file:`pyproject.toml` contains only information about the build backend, currently setuptools.build_meta. The idea is taken from
`A Practical Guide to Setuptools and Pyproject.toml`_.
Setuptools-specific configuration keys as defined in `PEP 621`_ are currently
not used.


.. _build-pyproject-build:

Building with pyproject-build
-----------------------------

To build semver you need:

* The :mod:`build` module which implements the `PEP 517`_ build
  frontend.
  Install it with::

        pip install build

  Some Linux distributions has already packaged it. If you prefer
  to use the module with your package manager, search for
  :file:`python-build` or :file:`python3-build` and install it.

* The command :command:`pyproject-build` from the :mod:`build` module.

To build semver, run::

    pyproject-build

After the command is finished, you can find two files in the :file:`dist` folder: a ``.tar.gz`` and a ``.whl`` file.