.. _sec_creating_subclasses_from_versioninfo:

Creating Subclasses from Version
================================

.. meta::
   :description lang=en:
      Creating subclasses from Version class

If you do not like creating functions to modify the behavior of semver
(as shown in section :ref:`sec_dealing_with_invalid_versions`), you can
also create a subclass of the :class:`Version <semver.version.Version>` class.

For example, if you want to output a "v" prefix before a version,
but the other behavior is the same, use the following code:

.. literalinclude:: semverwithvprefix.py
   :language: python
   :lines: 4-


The derived class :class:`SemVerWithVPrefix` can be used like
the original class. Additionally, you can pass "incomplete"
version strings like ``v2.3``:

.. code-block:: python

     >>> v1 = SemVerWithVPrefix.parse("v1.2.3")
     >>> assert str(v1) == "v1.2.3"
     >>> print(v1)
     v1.2.3
     >>> v2 = SemVerWithVPrefix.parse("v2.3")
     >>> v2 > v1
     True
     >>> bad = SemVerWithVPrefix.parse("1.2.4")
     Traceback (most recent call last):
     ...
     ValueError: '1.2.4': not a valid semantic version tag. Must start with 'v' or 'V'
