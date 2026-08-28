from __future__ import annotations

import importlib.util

import pytest

from semver import Version
from semver import version as version_module


def test_optional_backend_is_available_without_changing_public_objects() -> None:
    if importlib.util.find_spec("fast_semver_rs_backend") is None:
        pytest.skip("optional backend is not installed")

    assert version_module._native_parse_parts is not None
    result = Version.parse("1.2.3-rc.1+build.4")
    assert type(result) is Version
    assert result.to_tuple() == (1, 2, 3, "rc.1", "build.4")


def test_optional_backend_is_not_used_for_python_only_optional_parts() -> None:
    result = Version.parse("7", optional_minor_and_patch=True)
    assert result.to_tuple() == (7, 0, 0, None, None)
