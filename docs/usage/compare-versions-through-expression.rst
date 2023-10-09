Comparing Versions through an Expression
========================================

.. meta::
   :description lang=en:
      Comparing versions through an expression

If you need a more fine-grained approach of comparing two versions,
use the :meth:`~semver.version.Version.match` function. It expects two arguments:

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

    >>> Version.parse("2.0.0").match(">=1.0.0")
    True
    >>> Version.parse("1.0.0").match(">1.0.0")
    False

If no operator is specified, the match expression is interpreted as a
version to be compared for equality. This allows handling the common
case of version compatibility checking through either an exact version
or a match expression very easy to implement, as the same code will
handle both cases:

.. code-block:: python

    >>> Version.parse("2.0.0").match("2.0.0")
    True
    >>> Version.parse("1.0.0").match("3.5.1")
    False
