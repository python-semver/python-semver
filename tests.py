import pytest  # noqa

from semver import compare
from semver import match
from semver import parse
from semver import format_version
from semver import bump_major
from semver import bump_minor
from semver import bump_patch
from semver import bump_prerelease
from semver import bump_build
from semver import finalize_version
from semver import min_ver
from semver import max_ver
from semver import VersionInfo


SEMVERFUNCS = [
    compare, match, parse, format_version,
    bump_major, bump_minor, bump_patch, bump_prerelease, bump_build,
    max_ver, min_ver, finalize_version
]


@pytest.mark.parametrize("func", SEMVERFUNCS,
                         ids=[func.__name__ for func in SEMVERFUNCS])
def test_fordocstrings(func):
    assert func.__doc__, "Need a docstring for function %r" % func.__name


def test_should_parse_version():
    result = parse("1.2.3-alpha.1.2+build.11.e0f985a")
    assert result == {
        'major': 1,
        'minor': 2,
        'patch': 3,
        'prerelease': 'alpha.1.2',
        'build': 'build.11.e0f985a',
    }

    result = parse("1.2.3-alpha-1+build.11.e0f985a")
    assert result == {
        'major': 1,
        'minor': 2,
        'patch': 3,
        'prerelease': 'alpha-1',
        'build': 'build.11.e0f985a',
    }


def test_should_parse_zero_prerelease():
    result = parse("1.2.3-rc.0+build.0")

    assert result == {
        'major': 1,
        'minor': 2,
        'patch': 3,
        'prerelease': 'rc.0',
        'build': 'build.0',
    }

    result = parse("1.2.3-rc.0.0+build.0")

    assert result == {
        'major': 1,
        'minor': 2,
        'patch': 3,
        'prerelease': 'rc.0.0',
        'build': 'build.0',
    }


def test_should_get_less():
    assert compare("1.0.0", "2.0.0") == -1
    assert compare('1.0.0-alpha', '1.0.0-alpha.1') == -1
    assert compare('1.0.0-alpha.1', '1.0.0-alpha.beta') == -1
    assert compare('1.0.0-alpha.beta', '1.0.0-beta') == -1
    assert compare('1.0.0-beta', '1.0.0-beta.2') == -1
    assert compare('1.0.0-beta.2', '1.0.0-beta.11') == -1
    assert compare('1.0.0-beta.11', '1.0.0-rc.1') == -1
    assert compare('1.0.0-rc.1', '1.0.0') == -1


def test_should_get_greater():
    assert compare("2.0.0", "1.0.0") == 1
    assert compare('1.0.0-alpha.1', '1.0.0-alpha') == 1
    assert compare('1.0.0-alpha.beta', '1.0.0-alpha.1') == 1
    assert compare('1.0.0-beta', '1.0.0-alpha.beta') == 1
    assert compare('1.0.0-beta.2', '1.0.0-beta') == 1
    assert compare('1.0.0-beta.11', '1.0.0-beta.2') == 1
    assert compare('1.0.0-rc.1', '1.0.0-beta.11') == 1
    assert compare('1.0.0', '1.0.0-rc.1') == 1


def test_should_match_simple():
    assert match("2.3.7", ">=2.3.6") is True


def test_should_no_match_simple():
    assert match("2.3.7", ">=2.3.8") is False


def test_should_match_not_equal():
    assert match("2.3.7", "!=2.3.8") is True
    assert match("2.3.7", "!=2.3.6") is True
    assert match("2.3.7", "!=2.3.7") is False


def test_should_not_raise_value_error_for_expected_match_expression():
    assert match("2.3.7", "<2.4.0") is True
    assert match("2.3.7", ">2.3.5") is True

    assert match("2.3.7", "<=2.3.9") is True
    assert match("2.3.7", ">=2.3.5") is True
    assert match("2.3.7", "==2.3.7") is True
    assert match("2.3.7", "!=2.3.7") is False


def test_should_raise_value_error_for_unexpected_match_expression():
    with pytest.raises(ValueError):
        match("2.3.7", "=2.3.7")
    with pytest.raises(ValueError):
        match("2.3.7", "~2.3.7")
    with pytest.raises(ValueError):
        match("2.3.7", "^2.3.7")


def test_should_raise_value_error_for_zero_prefixed_versions():
    with pytest.raises(ValueError):
        parse("01.2.3")
    with pytest.raises(ValueError):
        parse("1.02.3")
    with pytest.raises(ValueError):
        parse("1.2.03")


def test_should_raise_value_error_for_invalid_value():
    with pytest.raises(ValueError):
        compare('foo', 'bar')
    with pytest.raises(ValueError):
        compare('1.0', '1.0.0')
    with pytest.raises(ValueError):
        compare('1.x', '1.0.0')


def test_should_raise_value_error_for_invalid_match_expression():
    with pytest.raises(ValueError):
        match('1.0.0', '')
    with pytest.raises(ValueError):
        match('1.0.0', '!')
    with pytest.raises(ValueError):
        match('1.0.0', '1.0.0')


def test_should_follow_specification_comparison():
    """
    produce comparison chain:
    1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-beta.2 < 1.0.0-beta.11
    < 1.0.0-rc.1 < 1.0.0-rc.1+build.1 < 1.0.0 < 1.0.0+0.3.7 < 1.3.7+build
    < 1.3.7+build.2.b8f12d7 < 1.3.7+build.11.e0f985a
    and in backward too.
    """
    chain = [
        '1.0.0-alpha', '1.0.0-alpha.1', '1.0.0-beta.2', '1.0.0-beta.11',
        '1.0.0-rc.1', '1.0.0', '1.3.7+build',
    ]
    versions = zip(chain[:-1], chain[1:])
    for low_version, high_version in versions:
        assert compare(low_version, high_version) == -1, \
            '%s should be lesser than %s' % (low_version, high_version)
        assert compare(high_version, low_version) == 1,  \
            '%s should be higher than %s' % (high_version, low_version)


def test_should_compare_rc_builds():
    assert compare('1.0.0-beta.2', '1.0.0-beta.11') == -1


def test_should_compare_release_candidate_with_release():
    assert compare('1.0.0-rc.1', '1.0.0') == -1
    assert compare('1.0.0-rc.1+build.1', '1.0.0') == -1


def test_should_say_equal_versions_are_equal():
    assert compare('2.0.0', '2.0.0') == 0
    assert compare('1.1.9-rc.1', '1.1.9-rc.1') == 0
    assert compare('1.1.9+build.1', '1.1.9+build.1') == 0
    assert compare('1.1.9-rc.1+build.1', '1.1.9-rc.1+build.1') == 0


def test_should_compare_versions_with_build_and_release():
    assert compare('1.1.9-rc.1', '1.1.9-rc.1+build.1') == 0
    assert compare('1.1.9-rc.1', '1.1.9+build.1') == -1


def test_should_ignore_builds_on_compare():
    assert compare('1.0.0+build.1', '1.0.0') == 0
    assert compare('1.0.0-alpha.1+build.1', '1.0.0-alpha.1') == 0
    assert compare('1.0.0+build.1', '1.0.0-alpha.1') == 1
    assert compare('1.0.0+build.1', '1.0.0-alpha.1+build.1') == 1


def test_should_correctly_format_version():
    assert format_version(3, 4, 5) == '3.4.5'
    assert format_version(3, 4, 5, 'rc.1') == '3.4.5-rc.1'
    assert format_version(3, 4, 5, prerelease='rc.1') == '3.4.5-rc.1'
    assert format_version(3, 4, 5, build='build.4') == '3.4.5+build.4'
    assert format_version(3, 4, 5, 'rc.1', 'build.4') == '3.4.5-rc.1+build.4'


def test_should_bump_major():
    assert bump_major('3.4.5') == '4.0.0'


def test_should_bump_minor():
    assert bump_minor('3.4.5') == '3.5.0'


def test_should_bump_patch():
    assert bump_patch('3.4.5') == '3.4.6'


def test_should_ignore_extensions_for_bump():
    assert bump_patch('3.4.5-rc1+build4') == '3.4.6'


def test_should_get_max():
    assert max_ver('3.4.5', '4.0.2') == '4.0.2'


def test_should_get_min():
    assert min_ver('3.4.5', '4.0.2') == '3.4.5'


def test_should_get_min_same():
    assert min_ver('3.4.5', '3.4.5') == '3.4.5'


def test_should_get_more_rc1():
    assert compare("1.0.0-rc1", "1.0.0-rc0") == 1


def test_prerelease_order():
    assert min_ver('1.2.3-rc.2', '1.2.3-rc.10') == '1.2.3-rc.2'
    assert min_ver('1.2.3-rc2', '1.2.3-rc10') == '1.2.3-rc10'
    # identifiers with letters or hyphens are compared lexically in ASCII sort
    # order.
    assert min_ver('1.2.3-Rc10', '1.2.3-rc10') == '1.2.3-Rc10'
    # Numeric identifiers always have lower precedence than non-numeric
    # identifiers.
    assert min_ver('1.2.3-2', '1.2.3-rc') == '1.2.3-2'
    # A larger set of pre-release fields has a higher precedence than a
    # smaller set, if all of the preceding identifiers are equal.
    assert min_ver('1.2.3-rc.2.1', '1.2.3-rc.2') == '1.2.3-rc.2'
    # When major, minor, and patch are equal, a pre-release version has lower
    # precedence than a normal version.
    assert min_ver('1.2.3', '1.2.3-1') == '1.2.3-1'
    assert min_ver('1.0.0-alpha', '1.0.0-alpha.1') == '1.0.0-alpha'


def test_should_bump_prerelease():
    assert bump_prerelease('3.4.5-rc.9') == '3.4.5-rc.10'
    assert bump_prerelease('3.4.5') == '3.4.5-rc.1'
    assert bump_prerelease('3.4.5', 'dev') == '3.4.5-dev.1'
    assert bump_prerelease('3.4.5', '') == '3.4.5-rc.1'


def test_should_ignore_build_on_prerelease_bump():
    assert bump_prerelease('3.4.5-rc.1+build.4') == '3.4.5-rc.2'


def test_should_bump_build():
    assert bump_build('3.4.5-rc.1+build.9') == '3.4.5-rc.1+build.10'
    assert bump_build('3.4.5-rc.1+0009.dev') == '3.4.5-rc.1+0010.dev'
    assert bump_build('3.4.5-rc.1') == '3.4.5-rc.1+build.1'
    assert bump_build('3.4.5') == '3.4.5+build.1'
    assert bump_build('3.4.5', 'nightly') == '3.4.5+nightly.1'
    assert bump_build('3.4.5', '') == '3.4.5+build.1'


def test_should_finalize_version():
    assert finalize_version('1.2.3') == '1.2.3'
    assert finalize_version('1.2.3-rc.5') == '1.2.3'
    assert finalize_version('1.2.3+build.2') == '1.2.3'
    assert finalize_version('1.2.3-rc.1+build.5') == '1.2.3'
    assert finalize_version('1.2.3-alpha') == '1.2.3'
    assert finalize_version('1.2.0') == '1.2.0'


def test_should_compare_version_info_objects():
    v1 = VersionInfo(major=0, minor=10, patch=4, prerelease=None, build=None)
    v2 = VersionInfo(
        major=0, minor=10, patch=4, prerelease='beta.1', build=None)

    # use `not` to enforce using comparision operators
    assert v1 != v2
    assert v1 > v2
    assert v1 >= v2
    assert not(v1 < v2)
    assert not(v1 <= v2)
    assert not(v1 == v2)

    v3 = VersionInfo(major=0, minor=10, patch=4, prerelease=None, build=None)

    assert not(v1 != v3)
    assert not(v1 > v3)
    assert v1 >= v3
    assert not(v1 < v3)
    assert v1 <= v3
    assert v1 == v3

    v4 = VersionInfo(major=0, minor=10, patch=5, prerelease=None, build=None)
    assert v1 != v4
    assert not(v1 > v4)
    assert not(v1 >= v4)
    assert v1 < v4
    assert v1 <= v4
    assert not(v1 == v4)


def test_should_compare_version_dictionaries():
    v1 = VersionInfo(major=0, minor=10, patch=4, prerelease=None, build=None)
    v2 = dict(major=0, minor=10, patch=4, prerelease='beta.1', build=None)

    assert v1 != v2
    assert v1 > v2
    assert v1 >= v2
    assert not(v1 < v2)
    assert not(v1 <= v2)
    assert not(v1 == v2)

    v3 = dict(major=0, minor=10, patch=4, prerelease=None, build=None)

    assert not(v1 != v3)
    assert not(v1 > v3)
    assert v1 >= v3
    assert not(v1 < v3)
    assert v1 <= v3
    assert v1 == v3

    v4 = dict(major=0, minor=10, patch=5, prerelease=None, build=None)
    assert v1 != v4
    assert not(v1 > v4)
    assert not(v1 >= v4)
    assert v1 < v4
    assert v1 <= v4
    assert not(v1 == v4)


def test_should_compare_prerelease_with_numbers_and_letters():
    v1 = VersionInfo(major=1, minor=9, patch=1, prerelease='1unms', build=None)
    v2 = VersionInfo(major=1, minor=9, patch=1, prerelease=None, build='1asd')
    assert v1 < v2
    assert compare("1.9.1-1unms", "1.9.1+1") == -1
