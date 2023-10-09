.. _sec_display_deprecation_warnings:

Displaying Deprecation Warnings
===============================

.. meta::
   :description lang=en:
      Displaying and filtering deprecation warnings

By default,  deprecation warnings are `ignored in Python <https://docs.python.org/3/library/warnings.html#warning-categories>`_.
This also affects semver's own warnings.

It is recommended that you turn on deprecation warnings in your scripts. Use one of
the following methods:

* Use the option `-Wd <https://docs.python.org/3/using/cmdline.html#cmdoption-w>`_
  to enable default warnings:

  * Directly running the Python command::

       $ python3 -Wd scriptname.py

  * Add the option in the shebang line (something like ``#!/usr/bin/python3``)
    after the command::

       #!/usr/bin/python3 -Wd

* In your own scripts add a filter to ensure that *all* warnings are displayed:

   .. code-block:: python

       import warnings
       warnings.simplefilter("default")
       # Call your semver code

   For further details, see the section
   `Overriding the default filter <https://docs.python.org/3/library/warnings.html#overriding-the-default-filter>`_
   of the Python documentation.
