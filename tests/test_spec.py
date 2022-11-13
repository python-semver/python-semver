import pytest  # noqa

from semver.spec import Spec, InvalidSpecifier


@pytest.mark.parametrize(
    "spec",
    [
        "1.2.3",
        b"2.3.4",
    ],
)
def test_spec_with_different_types(spec):
    assert Spec(spec)


@pytest.mark.parametrize(
    "spec",
    [
        "1",
        "1.2",
        "1.2.3",
        "1.2.x",
        "1.2.X",
        "1.2.*",
    ],
)
def test_spec_with_no_operator(spec):
    assert Spec(spec)


@pytest.mark.parametrize(
    "spec",
    [
        "==1",
        "==1.2",
        "==1.2.3",
        "==1.2.x",
        "==1.2.X",
        "==1.2.*",
    ],
)
def test_spec_with_equal_operator(spec):
    assert Spec(spec)


@pytest.mark.parametrize(
    "spec",
    [
        "!=1",
        "!=1.2",
        "!=1.2.3",
        "!=1.2.x",
        "!=1.2.X",
        "!=1.2.*",
    ],
)
def test_spec_with_notequal_operator(spec):
    assert Spec(spec)


@pytest.mark.parametrize(
    "spec",
    [
        "<1",
        "<1.2",
        "<1.2.3",
        "<1.2.x",
        "<1.2.X",
        "<1.2.*",
    ],
)
def test_spec_with_lt_operator(spec):
    assert Spec(spec)


@pytest.mark.parametrize(
    "spec",
    [
        "<=1",
        "<=1.2",
        "<=1.2.3",
        "<=1.2.x",
        "<=1.2.X",
        "<=1.2.*",
    ],
)
def test_spec_with_le_operator(spec):
    assert Spec(spec)


@pytest.mark.parametrize(
    "spec",
    [
        ">1",
        ">1.2",
        ">1.2.3",
        ">1.2.x",
        ">1.2.X",
        ">1.2.*",
    ],
)
def test_spec_with_gt_operator(spec):
    assert Spec(spec)


@pytest.mark.parametrize(
    "spec",
    [
        ">=1",
        ">=1.2",
        ">=1.2.3",
        ">=1.2.x",
        ">=1.2.X",
        ">=1.2.*",
    ],
)
def test_spec_with_ge_operator(spec):
    assert Spec(spec)


@pytest.mark.parametrize(
    "spec",
    [
        "~1",
        "~1.2",
        "~1.2.3",
        "~1.2.x",
        "~1.2.X",
        "~1.2.*",
    ],
)
def test_spec_with_tilde_operator(spec):
    assert Spec(spec)


@pytest.mark.parametrize(
    "spec",
    [
        "^1",
        "^1.2",
        "^1.2.3",
        "^1.2.x",
        "^1.2.X",
        "^1.2.*",
    ],
)
def test_spec_with_caret_operator(spec):
    assert Spec(spec)


@pytest.mark.parametrize(
    "spec",
    [
        "foo",
        "",
        None,
        "*1.2",
    ],
)
def test_with_invalid_spec(spec):
    with pytest.raises(InvalidSpecifier, match="Invalid specifier.*"):
        Spec(spec)


@pytest.mark.parametrize(
    "spec, realspec",
    [
        ("==1", "==1.0.0"),
        ("1.0.0", "==1.0.0"),
        ("1.*", "==1.*.*"),
    ],
)
def test_valid_spec_property(spec, realspec):
    assert Spec(spec).spec == realspec


@pytest.mark.parametrize(
    "spec,op",
    [
        ("<=1", "<="),
        ("1", "=="),
        ("1.2", "=="),
        ("1.2.3", "=="),
        ("1.X", "=="),
        ("1.2.X", "=="),
        ("<1.2", "<"),
        ("<1.2.3", "<"),
    ],
)
def test_valid_operator_and_value(spec, op):
    s = Spec(spec)
    assert s.operator == op


def test_valid_str():
    assert str(Spec("<1.2.3")) == "<1.2.3"


def test_valid_repr():
    assert repr(Spec(">2.3.4")) == "Spec('>2.3.4')"


@pytest.mark.parametrize("spec", ["1", "1.0", "1.0.0"])
def test_extend_spec(spec):
    assert Spec(spec).real_version_tuple == (1, 0, 0)


@pytest.mark.parametrize(
    "spec, version",
    [
        ("1", "1.0.0"),
        ("1.x", "1.*.*"),
        ("1.2", "1.2.0"),
        ("1.2.x", "1.2.*"),
    ],
)
def test_version_in_spec(spec, version):
    assert Spec(spec).realversion == version


@pytest.mark.parametrize(
    "spec, real",
    [
        ("1", "1.0.0"),
        ("1.x", "1.*.*"),
        ("1.2.x", "1.2.*"),
    ],
)
def test_when_minor_and_major_contain_stars(spec, real):
    assert Spec(spec).realversion == real


# --- Comparison
@pytest.mark.parametrize(
    "spec, other",
    [
        ("==1", "1.0.0"),
        ("==1.2", "1.2.0"),
        ("==1.2.4", "1.2.4"),
    ],
)
def test_compare_eq_with_other(spec, other):
    assert Spec(spec) == other


@pytest.mark.parametrize(
    "spec, other",
    [
        ("!=1", "2.0.0"),
        ("!=1.2", "1.3.9"),
        ("!=1.2.4", "1.5.0"),
    ],
)
def test_compare_ne_with_other(spec, other):
    assert Spec(spec) != other


@pytest.mark.parametrize(
    "spec, other",
    [
        ("<1", "0.5.0"),
        ("<1.2", "1.1.9"),
        ("<1.2.5", "1.2.4"),
    ],
)
def test_compare_lt_with_other(spec, other):
    assert Spec(spec) < other


@pytest.mark.parametrize(
    "spec, other",
    [
        (">1", "2.1.0"),
        (">1.2", "1.3.1"),
        (">1.2.5", "1.2.6"),
    ],
)
def test_compare_gt_with_other(spec, other):
    assert Spec(spec) > other


@pytest.mark.parametrize(
    "spec, other",
    [
        ("<=1", "0.9.9"),
        ("<=1.2", "1.1.9"),
        ("<=1.2.5", "1.2.5"),
    ],
)
def test_compare_le_with_other(spec, other):
    assert Spec(spec) <= other


@pytest.mark.parametrize(
    "spec, other",
    [
        (">=1", "2.1.0"),
        (">=1.2", "1.2.1"),
        (">=1.2.5", "1.2.6"),
    ],
)
def test_compare_ge_with_other(spec, other):
    assert Spec(spec) >= other


@pytest.mark.parametrize(
    "spec, others",
    [
        # ~1.2.3 =>  >=1.2.3 <1.3.0
        ("~1.2.3", ["1.2.3", "1.2.10"]),
        # ~1.2   =>  >=1.2.0 <1.3.0
        ("~1.2", ["1.2.0", "1.2.4"]),
        # ~1     =>  >=1.0.0 <2.0.0
        ("~1", ["1.0.0", "1.2.0", "1.5.9"]),
    ],
)
def test_compare_tilde_with_other(spec, others):
    for other in others:
        assert Spec(spec).match(other)


@pytest.mark.parametrize(
    "spec, others",
    [
        # ^1.2.3 =  >=1.2.3 <2.0.0
        ("^1.2.3", ["1.2.3", "1.2.4", "1.2.10"]),
        # ^0.2.3 =  >=0.2.3 <0.3.0
        ("^0.2.3", ["0.2.3", "0.2.4", "0.2.10"]),
        # ^0.0.3 =  >=0.0.3 <0.0.4
        ("^0.0.3", ["0.0.3"]),
        # ^1.2.x =  >=1.2.0 <2.0.0
        ("^1.2.x", ["1.2.0", "1.2.4", "1.2.10"]),
        # ^0.0.x =  >=0.0.0 <0.1.0
        ("^0.0.x", ["0.0.0", "0.0.5"]),
        #  ^2, ^2.x, ^2.x.x =  >=2.0.0 <3.0.0
        ("^2", ["2.0.0", "2.1.4", "2.10.99"]),
        ("^2.x", ["2.0.0", "2.1.1", "2.10.89"]),
        ("^2.x.x", ["2.0.0", "2.1.1", "2.11.100"]),
        # ^0.0.0  =>
        ("^0.0.0", ["0.0.1", "0.0.6"]),
    ],
)
def test_compare_caret_with_other(spec, others):
    for other in others:
        assert Spec(spec).match(other)


@pytest.mark.parametrize(
    "othertype",
    [
        tuple([1, 2, 3]),
        dict(major=1, minor=2, patch=3),
    ],
)
def test_compare_with_valid_types(othertype):
    spec = "1.2.3"
    assert Spec(spec) == othertype


@pytest.mark.parametrize(
    "othertype, exception",
    [
        (dict(foo=2), TypeError),
        (list(), TypeError),
        (tuple(), TypeError),
        (set(), AssertionError),
        (frozenset(), AssertionError),
    ],
)
def test_compare_with_invalid_types(othertype, exception):
    spec = "1.2.3"
    with pytest.raises(exception):
        assert Spec(spec) == othertype


def test_invalid_spec_raise_invalidspecifier():
    with pytest.raises(InvalidSpecifier):
        s = Spec("1.x.2")
