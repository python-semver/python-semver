import pytest

from semver import (
    bump_build,
    bump_major,
    bump_minor,
    bump_patch,
    bump_prerelease,
    compare,
    deprecated,
    finalize_version,
    format_version,
    match,
    max_ver,
    min_ver,
    parse,
    parse_version_info,
    replace,
)


@pytest.mark.parametrize(
    "func, args, kwargs",
    [
        (bump_build, ("1.2.3",), {}),
        (bump_major, ("1.2.3",), {}),
        (bump_minor, ("1.2.3",), {}),
        (bump_patch, ("1.2.3",), {}),
        (bump_prerelease, ("1.2.3",), {}),
        (compare, ("1.2.1", "1.2.2"), {}),
        (format_version, (3, 4, 5), {}),
        (finalize_version, ("1.2.3-rc.5",), {}),
        (match, ("1.0.0", ">=1.0.0"), {}),
        (parse, ("1.2.3",), {}),
        (parse_version_info, ("1.2.3",), {}),
        (replace, ("1.2.3",), dict(major=2, patch=10)),
        (max_ver, ("1.2.3", "1.2.4"), {}),
        (min_ver, ("1.2.3", "1.2.4"), {}),
    ],
)
def test_should_raise_deprecation_warnings(func, args, kwargs):
    with pytest.warns(
        DeprecationWarning, match=r"Function 'semver.[_a-zA-Z]+' is deprecated."
    ) as record:
        func(*args, **kwargs)
        if not record:
            pytest.fail("Expected a DeprecationWarning for {}".format(func.__name__))
    assert len(record), "Expected one DeprecationWarning record"


def test_deprecated_deco_without_argument():
    @deprecated
    def mock_func():
        return True

    with pytest.deprecated_call():
        assert mock_func()
