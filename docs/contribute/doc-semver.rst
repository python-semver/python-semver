.. _doc:

Documenting semver
==================

.. meta::
   :description lang=en:
      Documenting semver with type annotations, docstrings, Sphinx directives

Documenting the features of semver is very important. It gives our developers
an overview what is possible with semver, how it "feels", and how it is
used efficiently.

.. note::

    To build the documentation locally use the following command::

      $ tox -e docs

    The built documentation is available in :file:`docs/_build/html`.


A new feature is *not* complete if it isn't proberly documented. A good
documentation includes:

  * **Type annotations**

    This library supports type annotations. Therefore, each function
    or method requires types for each arguments and return objects.
    Exception of this rule is ``self``.

  * **A docstring**

    Each docstring contains a summary line, a linebreak, an optional
    directive (see next item), the description of its arguments in
    `Sphinx style`_, and an optional doctest.
    The docstring is extracted and reused in the :ref:`api` section.
    An appropriate docstring looks like this::

         def to_tuple(self) -> VersionTuple:
            """
            Convert the Version object to a tuple.

            .. versionadded:: 2.10.0
               Renamed ``VersionInfo._astuple`` to ``VersionInfo.to_tuple`` to
               make this function available in the public API.

            :return: a tuple with all the parts

            >>> semver.Version(5, 3, 1).to_tuple()
            (5, 3, 1, None, None)

            """

  * **An optional directive**

    If you introduce a new feature, change a function/method, or remove something,
    it is a good practice to introduce Sphinx directives into the docstring.
    This gives the reader an idea what version is affected by this change.

    The first required argument, ``VERSION``, defines the version when this change
    was introduced. You can choose from:

    * ``.. versionadded:: VERSION``

      Use this directive to describe a new feature.

    * ``.. versionchanged:: VERSION``

      Use this directive to describe when something has changed, for example,
      new parameters were added, changed side effects, different return values, etc.

    * ``.. deprecated:: VERSION``

      Use this directive when a feature is deprecated. Describe what should
      be used instead, if appropriate.


    Add such a directive *after* the summary line, as shown above.

  * **The documentation**

    A docstring is good, but in most cases it is too short. API documentation
    cannot replace good user documentation.
    Describe *how* to use your new feature in the documentation.
    Here you can give your readers more examples, describe it in a broader
    context, or show edge cases.


.. _Sphinx style: https://sphinx-rtd-tutorial.rtfd.io/en/latest/docstrings.html
