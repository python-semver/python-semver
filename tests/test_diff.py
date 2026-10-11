# Adapted from node-semver v7.7.2 test/functions/diff.js:
# https://github.com/npm/node-semver/blob/v7.7.2/test/functions/diff.js
# The ISC License
#
# Copyright (c) Isaac Z. Schlueter and Contributors
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
# IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import pytest

from semver import Version


@pytest.mark.parametrize(
    "left,right,expected",
    [
        ("1.2.3", "0.2.3", "major"),
        ("0.2.3", "1.2.3", "major"),
        ("1.4.5", "0.2.3", "major"),
        ("1.2.3", "2.0.0-pre", "premajor"),
        ("2.0.0-pre", "1.2.3", "premajor"),
        ("1.2.3", "1.3.3", "minor"),
        ("1.0.1", "1.1.0-pre", "preminor"),
        ("1.2.3", "1.2.4", "patch"),
        ("1.2.3", "1.2.4-pre", "prepatch"),
        ("0.0.1", "0.0.1-pre", "patch"),
        ("0.0.1", "0.0.1-pre-2", "patch"),
        ("1.1.0", "1.1.0-pre", "minor"),
        ("1.1.0-pre-1", "1.1.0-pre-2", "prerelease"),
        ("1.0.0", "1.0.0", None),
        ("1.0.0-1", "1.0.0-1", None),
        ("0.0.2-1", "0.0.2", "patch"),
        ("0.0.2-1", "0.0.3", "patch"),
        ("0.0.2-1", "0.1.0", "minor"),
        ("0.0.2-1", "1.0.0", "major"),
        ("0.1.0-1", "0.1.0", "minor"),
        ("1.0.0-1", "1.0.0", "major"),
        ("1.0.0-1", "1.1.1", "major"),
        ("1.0.0-1", "2.1.1", "major"),
        ("1.0.1-1", "1.0.1", "patch"),
        ("0.0.0-1", "0.0.0", "major"),
        ("1.0.0-1", "2.0.0", "major"),
        ("1.0.0-1", "2.0.0-1", "premajor"),
        ("1.0.0-1", "1.1.0-1", "preminor"),
        ("1.0.0-1", "1.0.1-1", "prepatch"),
        ("1.7.2-1", "1.8.1", "minor"),
        ("1.1.1-pre", "2.1.1-pre", "premajor"),
        ("1.1.1-pre", "2.1.1", "major"),
        ("1.2.3-1", "1.2.3", "patch"),
        ("1.4.0-1", "2.3.5", "major"),
        ("1.6.1-5", "1.7.2", "minor"),
        ("2.0.0-1", "2.1.1", "major"),
        ("1.0.0-alpha", "1.1.1", "major"),
        ("1.0.1-rc.1", "1.0.1", "patch"),
        ("1.2.3-alpha+one", "2.3.4-beta+two", "premajor"),
        ("1.2.3-alpha+one", "1.3.4-beta+two", "preminor"),
        ("1.2.3-alpha+one", "1.2.4-beta+two", "prepatch"),
        ("1.2.3-alpha.2", "1.2.3-alpha.10", "prerelease"),
        ("1.2.3-alpha.1", "1.2.3-alpha.1.1", "prerelease"),
        ("1.2.3+one", "1.2.3+two", None),
        ("1.2.3", "1.2.3+one", None),
        ("1.2.3-alpha+one", "1.2.3-alpha+two", None),
    ],
)
def test_diff(left, right, expected):
    left, right = Version.parse(left), Version.parse(right)
    before = left.to_tuple(), right.to_tuple()
    assert left.diff(right) == expected
    assert right.diff(left) == expected
    assert (left.to_tuple(), right.to_tuple()) == before


@pytest.mark.parametrize(
    "other",
    [Version(2), "2.0.0", b"2.0.0", {"major": "2"}, (2,), [2, 0]],
)
def test_diff_accepts_comparable(other):
    assert Version(1).diff(other) == "major"


@pytest.mark.parametrize(
    "other",
    [
        "1.2.3-rc.1+two",
        b"1.2.3-rc.1+two",
        {"major": 1, "minor": 2, "patch": 3, "prerelease": "rc.1", "build": "two"},
        (1, 2, 3, "rc.1", "two"),
        [1, 2, 3, "rc.1", "two"],
    ],
)
def test_diff_converts_all_parts(other):
    assert Version.parse("1.2.3-rc.1+one").diff(other) is None
    assert Version(1, 2, 3).diff(other) == "patch"


@pytest.mark.parametrize("other", [None, 1, 1.5, object(), {1, 2, 3}])
def test_diff_rejects_unsupported_types(other):
    with pytest.raises(
        TypeError, match="Expected str, bytes, dict, tuple, list, or Version"
    ):
        Version(1).diff(other)


@pytest.mark.parametrize("other", ["bad", b"bad", "1.02.3", b"\xff"])
def test_diff_rejects_invalid_strings(other):
    with pytest.raises(ValueError):
        Version(1).diff(other)


@pytest.mark.parametrize(
    "other",
    [{}, {"unknown": 1}, (1, 2, 3, 4, 5, 6), [], [None]],
)
def test_diff_rejects_invalid_collection_shape(other):
    with pytest.raises(TypeError):
        Version(1).diff(other)


@pytest.mark.parametrize("other", [{"major": -1}, ("bad",), [1, -2]])
def test_diff_rejects_invalid_collection_value(other):
    with pytest.raises(ValueError):
        Version(1).diff(other)


def test_diff_accepts_subclasses_without_reconstructing_instances():
    class DerivedVersion(Version):
        def __init__(self, major, *, label):
            super().__init__(major)
            self.label = label

        def compare(self, other):
            raise AssertionError("diff must use SemVer precedence")

    class SiblingVersion(Version):
        pass

    derived = DerivedVersion(1, label="custom")
    for other in (Version(2), DerivedVersion(2, label="other"), SiblingVersion(2)):
        assert derived.diff(other) == "major"
        assert other.diff(derived) == "major"
    assert derived.label == "custom"


def test_diff_uses_subclass_conversion_hooks():
    class DerivedVersion(Version):
        @classmethod
        def parse(cls, version, **kwargs):
            return super().parse(version[1:], **kwargs)

    assert DerivedVersion(1).diff("v2.0.0") == "major"
    assert DerivedVersion(1).diff(b"v2.0.0") == "major"
    assert DerivedVersion(1).diff({"major": 2}) == "major"
    assert DerivedVersion(1).diff((2,)) == "major"
    assert DerivedVersion(1).diff([2]) == "major"
