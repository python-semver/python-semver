import pytest

from semver import max_ver, min_ver


def test_should_get_max():
    assert max_ver("3.4.5", "4.0.2") == "4.0.2"


def test_should_get_max_same():
    assert max_ver("3.4.5", "3.4.5") == "3.4.5"


def test_should_get_min():
    assert min_ver("3.4.5", "4.0.2") == "3.4.5"


def test_should_get_min_same():
    assert min_ver("3.4.5", "3.4.5") == "3.4.5"


@pytest.mark.parametrize(
    "left,right,expected",
    [
        ("1.2.3-rc.2", "1.2.3-rc.10", "1.2.3-rc.2"),
        ("1.2.3-rc2", "1.2.3-rc10", "1.2.3-rc10"),
        # identifiers with letters or hyphens are compared lexically in ASCII sort
        # order.
        ("1.2.3-Rc10", "1.2.3-rc10", "1.2.3-Rc10"),
        # Numeric identifiers always have lower precedence than non-numeric
        # identifiers.
        ("1.2.3-2", "1.2.3-rc", "1.2.3-2"),
        # A larger set of pre-release fields has a higher precedence than a
        # smaller set, if all of the preceding identifiers are equal.
        ("1.2.3-rc.2.1", "1.2.3-rc.2", "1.2.3-rc.2"),
        # When major, minor, and patch are equal, a pre-release version has lower
        # precedence than a normal version.
        ("1.2.3", "1.2.3-1", "1.2.3-1"),
        ("1.0.0-alpha", "1.0.0-alpha.1", "1.0.0-alpha"),
    ],
)
def test_prerelease_order(left, right, expected):
    assert min_ver(left, right) == expected
