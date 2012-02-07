# -*- coding: utf-8 -*-

from unittest import TestCase

from semver import compare
from semver import match
from semver import parse


class TestSemver(TestCase):
    def test_should_parse_version(self):
        self.assertEquals(
            parse("1.2.3-alpha.1.2+build.11.e0f985a"),
            {'major': 1,
             'minor': 2,
             'patch': 3,
             'prerelease': 'alpha.1.2',
             'build': 'build.11.e0f985a'})

    def test_should_get_less(self):
        self.assertEquals(
            compare("1.0.0", "2.0.0"),
            -1)

    def test_should_get_greater(self):
        self.assertEquals(
            compare("2.0.0", "1.0.0"),
            1)

    def test_should_match_simple(self):
        self.assertEquals(
            match("2.3.7", ">=2.3.6"),
            True)

    def test_should_no_match_simple(self):
        self.assertEquals(
            match("2.3.7", ">=2.3.8"),
            False)
