Combining Pydantic and semver
=============================

.. meta::
   :description lang=en:
      Combining Pydantic and semver

According to its homepage, `Pydantic <https://pydantic-docs.helpmanual.io>`_
"enforces type hints at runtime, and provides user friendly errors when data
is invalid."

To work with Pydantic>2.0, use the following steps:


1. Derive a new class from :class:`~semver.version.Version`
   first and add the magic methods :py:meth:`__get_pydantic_core_schema__`
   and :py:meth:`__get_pydantic_json_schema__` like this:

    .. code-block:: python

        from typing import Annotated, Any, Callable
        from pydantic import GetJsonSchemaHandler
        from pydantic_core import core_schema
        from pydantic.json_schema import JsonSchemaValue
        from semver import Version


        class _VersionPydanticAnnotation:
            @classmethod
            def __get_pydantic_core_schema__(
                cls,
                _source_type: Any,
                _handler: Callable[[Any], core_schema.CoreSchema],
            ) -> core_schema.CoreSchema:
                def validate_from_str(value: str) -> Version:
                    return Version.parse(value)

                from_str_schema = core_schema.chain_schema(
                    [
                        core_schema.str_schema(),
                        core_schema.no_info_plain_validator_function(validate_from_str),
                    ]
                )

                return core_schema.json_or_python_schema(
                    json_schema=from_str_schema,
                    python_schema=core_schema.union_schema(
                        [
                            core_schema.is_instance_schema(Version),
                            from_str_schema,
                        ]
                    ),
                    serialization = core_schema.to_string_ser_schema(),
                )

            @classmethod
            def __get_pydantic_json_schema__(
                cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
            ) -> JsonSchemaValue:
                return handler(core_schema.str_schema())

        ManifestVersion = Annotated[Version, _VersionPydanticAnnotation]

2. Create a new model (in this example :class:`MyModel`) and derive
   it from :py:class:`pydantic:pydantic.BaseModel`:

    .. code-block:: python

        import pydantic

        class MyModel(pydantic.BaseModel):
            version: _VersionPydanticAnnotation

3. Use your model like this:

    .. code-block:: python

        model = MyModel.parse_obj({"version": "1.2.3"})

   The attribute :py:attr:`model.version` will be an instance of
   :class:`~semver.version.Version`.
   If the version is invalid, the construction will raise a
   :py:class:`pydantic:pydantic_core.ValidationError`.
