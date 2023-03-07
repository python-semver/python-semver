Combining Pydantic and semver
=============================

According to its homepage, `Pydantic <https://pydantic-docs.helpmanual.io>`_
"enforces type hints at runtime, and provides user friendly errors when data
is invalid."

To work with Pydantic, use the following steps:


1. Derive a new class from :class:`~semver.version.Version`
   first and add the magic methods :py:meth:`__get_validators__`
   and :py:meth:`__modify_schema__` like this:

    .. code-block:: python

        from semver import Version

        class PydanticVersion(Version):
            @classmethod
            def _parse(cls, version):
                return cls.parse(version)

            @classmethod
            def __get_validators__(cls):
                """Return a list of validator methods for pydantic models."""
                yield cls._parse

            @classmethod
            def __modify_schema__(cls, field_schema):
                """Inject/mutate the pydantic field schema in-place."""
                field_schema.update(examples=["1.0.2",
                                              "2.15.3-alpha",
                                              "21.3.15-beta+12345",
                                              ]
                                    )

2. Create a new model (in this example :class:`MyModel`) and derive
   it from :class:`pydantic.BaseModel`:

    .. code-block:: python

        import pydantic

        class MyModel(pydantic.BaseModel):
            version: PydanticVersion

3. Use your model like this:

    .. code-block:: python

        model = MyModel.parse_obj({"version": "1.2.3"})

   The attribute :py:attr:`model.version` will be an instance of
   :class:`~semver.version.Version`.
   If the version is invalid, the construction will raise a
   :py:exc:`pydantic.ValidationError`.
