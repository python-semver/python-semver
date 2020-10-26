import pytest

from semver import match


def test_should_match_simple():
    assert match("2.3.7", ">=2.3.6") is True


def test_should_no_match_simple():
    assert match("2.3.7", ">=2.3.8") is False


@pytest.mark.parametrize(
    "left,right,expected",
    [
        ("2.3.7", "!=2.3.8", True),
        ("2.3.7", "!=2.3.6", True),
        ("2.3.7", "!=2.3.7", False),
    ],
)
def test_should_match_not_equal(left, right, expected):
    assert match(left, right) is expected


@pytest.mark.parametrize(
    "left,right,expected",
    [
        ("2.3.7", "<2.4.0", True),
        ("2.3.7", ">2.3.5", True),
        ("2.3.7", "<=2.3.9", True),
        ("2.3.7", ">=2.3.5", True),
        ("2.3.7", "==2.3.7", True),
        ("2.3.7", "!=2.3.7", False),
    ],
)
def test_should_not_raise_value_error_for_expected_match_expression(
    left, right, expected
):
    assert match(left, right) is expected


@pytest.mark.parametrize(
    "left,right", [("2.3.7", "=2.3.7"), ("2.3.7", "~2.3.7"), ("2.3.7", "^2.3.7")]
)
def test_should_raise_value_error_for_unexpected_match_expression(left, right):
    with pytest.raises(ValueError):
        match(left, right)


@pytest.mark.parametrize(
    "left,right", [("1.0.0", ""), ("1.0.0", "!"), ("1.0.0", "1.0.0")]
)
def test_should_raise_value_error_for_invalid_match_expression(left, right):
    with pytest.raises(ValueError):
        match(left, right)
