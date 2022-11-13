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
* ``~`` for tilde ranges, see :ref:`tilde_expressions`
* ``^`` for caret ranges, see :ref:`caret_expressions`

That gives you the following possibilities to express your condition:

.. code-block:: python

    >>> version = Version(2, 0, 0)
    >>> version.match(">=1.0.0")
    True
    >>> version.match("<1.0.0")
    False

If no operator is specified, the match expression is interpreted as a
version to be compared for equality with the ``==`` operator.
This allows handling the common case of version compatibility checking
through either an exact version or a match expression very easy to
implement, as the same code will handle both cases:

.. code-block:: python

    >>> version = Version(2, 0, 0)
    >>> version.match("2.0.0")
    True
    >>> version.match("3.5.1")
    False


Using the :class:`Spec <semver.spec.Spec>` class
------------------------------------------------

The :class:`Spec <semver.spec.Spec>` class is the underlying object
which makes comparison possible.

It supports comparisons through usual Python operators:

.. code-block:: python

   >>> Spec("1.2") > '1.2.1'
   True
   >>> Spec("1.3") == '1.3.10'
   False

If you need to reuse a ``Spec`` object, use the :meth:`match <semver.spec.Spec.match>` method:

.. code-block:: python

   >>> spec = Spec(">=1.2.3")
   >>> spec.match("1.3.1")
   True
   >>> spec.match("1.2.1")
   False


.. _tilde_expressions:

Using tilde expressions
-----------------------

Tilde expressions are "approximately equivalent to a version".
They are expressions like ``~1``, ``~1.2``, or ``~1.2.3``.
Tilde expression freezes major and minor numbers. They are used if
you want to avoid potentially incompatible changes, but want to accept bug fixes.

Internally they are converted into two comparisons:

* ``~1`` is converted into ``>=1.0.0 <(1+1).0.0`` which is ``>=1.0.0 <2.0.0``
* ``~1.2`` is converted into ``>=1.2.0 <1.(2+1).0`` which is ``>=1.2.0 <1.3.0``
* ``~1.2.3`` is converted into ``>=1.2.3 <1.(2+1).0`` which is ``>=1.2.3 <1.3.0``

Only if both comparisions are true, the tilde expression as whole is true
as in the following examples:

.. code-block:: python

   >>> version = Version(1, 2, 0)
   >>> version.match("~1.2")  # same as >=1.2.0 AND <1.3.0
   True
   >>> version.match("~1.3.2")  # same as >=1.3.2 AND <1.4.0
   False


.. _caret_expressions:

Using caret expressions
-----------------------

Care expressions are "compatible with a version".
They are expressions like ``^1``, ``^1.2``, or ``^1.2.3``.
Care expressions freezes the major number only.

Internally they are converted into two comparisons:

* ``^1`` is converted into ``>=1.0.0 <2.0.0``
* ``^1.2`` is converted into ``>=1.2.0 <2.0.0``
* ``^1.2.3`` is converted into ``>=1.2.3 <2.0.0``

.. code-block:: python

   >>> version = Version(1, 2, 0)
   >>> version.match("^1.2")  # same as >=1.2.0 AND <2.0.0
   True
   >>> version.match("^1.3")
   False

It is possible to add placeholders to the care expression. Placeholders
are ``x``, ``X``, or ``*`` and are replaced by zeros like in the following examples:

.. code-block:: python

   >>> version = Version(1, 2, 3)
   >>> version.match("^1.x")  # same as >=1.0.0 AND <2.0.0
   True
   >>> version.match("^1.2.x")  # same as >=1.2.0 AND <2.0.0
   True
   >>> version.match("^1.3.*")  # same as >=1.3.0 AND <2.0.0
   False
