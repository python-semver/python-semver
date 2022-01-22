Comparing Versions through an Expression
========================================

If you need a more fine-grained approach of comparing two versions,
use the :func:`semver.match` function. It expects two arguments:

1. a version string
2. a match expression

Currently, the match expression supports the following operators:

* ``<`` smaller than
* ``>`` greater than
* ``>=`` greater or equal than
* ``<=`` smaller or equal than
* ``==`` equal
* ``!=`` not equal

That gives you the following possibilities to express your condition:

.. code-block:: python

    >>> semver.match("2.0.0", ">=1.0.0")
    True
    >>> semver.match("1.0.0", ">1.0.0")
    False
