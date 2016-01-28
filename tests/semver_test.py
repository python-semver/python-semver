# -*- coding: utf-8 -*-

import unittest
from unittest import TestCase
from semver import compare
from semver import match
from semver import parse
from semver import format_version
from semver import bump_major
from semver import bump_minor
from semver import bump_patch
from semver import bump_prerelease
from semver import bump_build
from semver import min_ver
from semver import max_ver


class TestSemver(TestCase):
    def test_should_parse_version(self):
        self.assertEqual(
            parse("1.2.3-alpha.1.2+build.11.e0f985a"),
            {'major': 1,
             'minor': 2,
             'patch': 3,
             'prerelease': 'alpha.1.2',
             'build': 'build.11.e0f985a'})

        self.assertEqual(
            parse("1.2.3-alpha-1+build.11.e0f985a"),
            {'major': 1,
             'minor': 2,
             'patch': 3,
             'prerelease': 'alpha-1',
             'build': 'build.11.e0f985a'})

    def test_should_get_less(self):
        self.assertEqual(
            compare("1.0.0", "2.0.0"),
            -1)

    def test_should_get_greater(self):
        self.assertEqual(
            compare("2.0.0", "1.0.0"),
            1)

    def test_should_match_simple(self):
        self.assertEqual(
            match("2.3.7", ">=2.3.6"),
            True)

    def test_should_no_match_simple(self):
        self.assertEqual(
            match("2.3.7", ">=2.3.8"),
            False)

    def test_should_raise_value_error_for_zero_prefixed_versions(self):
        self.assertRaises(ValueError, parse, "01.2.3")
        self.assertRaises(ValueError, parse, "1.02.3")
        self.assertRaises(ValueError, parse, "1.2.03")

    def test_should_raise_value_error_for_invalid_value(self):
        self.assertRaises(ValueError, compare, 'foo', 'bar')
        self.assertRaises(ValueError, compare, '1.0', '1.0.0')
        self.assertRaises(ValueError, compare, '1.x', '1.0.0')

    def test_should_raise_value_error_for_invalid_match_expression(self):
        self.assertRaises(ValueError, match, '1.0.0', '')
        self.assertRaises(ValueError, match, '1.0.0', '!')
        self.assertRaises(ValueError, match, '1.0.0', '1.0.0')

    def test_should_follow_specification_comparison(self):
        # produce comparsion chain:
        # 1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-beta.2 < 1.0.0-beta.11
        # < 1.0.0-rc.1 < 1.0.0-rc.1+build.1 < 1.0.0 < 1.0.0+0.3.7 < 1.3.7+build
        # < 1.3.7+build.2.b8f12d7 < 1.3.7+build.11.e0f985a
        # and in backward too.
        chain = ['1.0.0-alpha', '1.0.0-alpha.1', '1.0.0-beta.2',
                 '1.0.0-beta.11', '1.0.0-rc.1',
                 '1.0.0', '1.3.7+build']
        versions = zip(chain[:-1], chain[1:])
        for low_version, high_version in versions:
            self.assertEqual(
                compare(low_version, high_version), -1,
                '%s should be lesser than %s' % (low_version, high_version))
            self.assertEqual(
                compare(high_version, low_version), 1,
                '%s should be higher than %s' % (high_version, low_version))

    def test_should_compare_rc_builds(self):
        self.assertEqual(compare('1.0.0-beta.2', '1.0.0-beta.11'), -1)

    def test_should_compare_release_candidate_with_release(self):
        self.assertEqual(compare('1.0.0-rc.1+build.1', '1.0.0'), -1)

    def test_should_say_equal_versions_are_equal(self):
        self.assertEqual(compare("2.0.0", "2.0.0"), 0)

    def test_should_correctly_format_version(self):
        self.assertEqual(format_version(3, 4, 5), '3.4.5')
        self.assertEqual(format_version(3, 4, 5, 'rc.1'), '3.4.5-rc.1')
        self.assertEqual(format_version(3, 4, 5, prerelease='rc.1'), '3.4.5-rc.1')
        self.assertEqual(format_version(3, 4, 5, build='build.4'), '3.4.5+build.4')
        self.assertEqual(format_version(3, 4, 5, 'rc.1', 'build.4'), '3.4.5-rc.1+build.4')

    def test_should_bump_major(self):
        self.assertEqual(bump_major('3.4.5'), '4.0.0')

    def test_should_bump_minor(self):
        self.assertEqual(bump_minor('3.4.5'), '3.5.0')

    def test_should_bump_patch(self):
        self.assertEqual(bump_patch('3.4.5'), '3.4.6')

    def test_should_ignore_extensions_for_bump(self):
        self.assertEqual(bump_patch('3.4.5-rc1+build4'), '3.4.6')

    def test_should_get_max(self):
        self.assertEqual(max_ver('3.4.5', '4.0.2'), '4.0.2')

    def test_should_get_min(self):
        self.assertEqual(min_ver('3.4.5', '4.0.2'), '3.4.5')

    def test_should_get_min_same(self):
        self.assertEqual(min_ver('3.4.5', '3.4.5'), '3.4.5')

    def test_should_get_more_rc1(self):
        self.assertEqual(
            compare("1.0.0-rc1", "1.0.0-rc0"),
            1)

    def test_should_bump_prerelease(self):
        self.assertEqual(bump_prerelease('3.4.5-rc.9'),
                         '3.4.5-rc.10')
        self.assertEqual(bump_prerelease('3.4.5-0009.dev'),
                         '3.4.5-0010.dev')
        self.assertEqual(bump_prerelease('3.4.5'),
                         '3.4.5-rc.1')

    def test_should_ignore_build_on_prerelease_bump(self):
        self.assertEqual(bump_prerelease('3.4.5-rc.1+build.4'),
                         '3.4.5-rc.2')

    def test_should_bump_build(self):
        self.assertEqual(bump_build('3.4.5-rc.1+build.9'),
                         '3.4.5-rc.1+build.10')
        self.assertEqual(bump_build('3.4.5-rc.1+0009.dev'),
                         '3.4.5-rc.1+0010.dev')
        self.assertEqual(bump_build('3.4.5-rc.1'),
                         '3.4.5-rc.1+build.1')
        self.assertEqual(bump_build('3.4.5'),
                         '3.4.5+build.1')


if __name__ == '__main__':
    unittest.main()
