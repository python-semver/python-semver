"""Regression tests for bump_build() with digitless build metadata.

Related to :gh:`466`. While investigating how the ``token`` parameter of
:meth:`semver.version.Version.bump_build` is used, it turned out that
``bump_build()`` silently returns an *unchanged* version when the build
metadata contains no digits at all (for example ``1.2.3+alpha``).

That contradicts the documented contract that bumping raises the
respective part of the version: the returned object is identical to the
original one, so callers cannot tell that anything was bumped.

The analogous problem for the prerelease part was fixed in :gh:`460`
by appending ``.0`` when the last identifier is not numeric. These
tests require the same behavior for the build part.

Note: build metadata does not take part in SemVer precedence, so the
assertions compare the resulting build strings (and string
representations) instead of using :meth:`Version.compare`.
"""

from semver import Version


def test_bump_build_digitless_metadata_should_append_0():
    """bump_build() must raise a digitless build, not return it unchanged."""
    v = Version.parse("1.2.3+alpha")
    bumped = v.bump_build()
    assert bumped.build == "alpha.0", (
        f"Expected build 'alpha.0', but got {bumped.build!r}"
    )
    assert str(bumped) == "1.2.3+alpha.0"


def test_bump_build_digitless_metadata_should_return_new_version():
    """bump_build() must not silently return an equal version."""
    v = Version.parse("1.2.3+alpha")
    bumped = v.bump_build()
    assert bumped is not v
    assert bumped.build != v.build
    assert bumped.build == "alpha.0"


def test_bump_build_digitless_multi_identifier_should_append_0():
    """The last identifier is raised, also for dotted digitless builds."""
    v = Version.parse("1.2.3+exp.sha")
    assert str(v.bump_build()) == "1.2.3+exp.sha.0"


def test_bump_build_numeric_ending_unchanged():
    """Builds with a numeric last identifier keep the incrementing behavior."""
    v = Version.parse("1.2.3+build.9")
    assert str(v.bump_build()) == "1.2.3+build.10"
    v2 = Version.parse("1.2.3+alpha.1")
    assert str(v2.bump_build()) == "1.2.3+alpha.2"


def test_bump_build_token_ignored_for_existing_digitless_build():
    """The token only constructs a build when none exists.

    An existing (digitless) build must still be raised, not replaced
    by the token or returned unchanged.
    """
    v = Version.parse("1.2.3+alpha")
    bumped = v.bump_build("b")
    assert str(bumped) == "1.2.3+alpha.0"


def test_bump_build_digitless_bump_is_repeatable():
    """Repeated bumping of a digitless build keeps raising it."""
    v = Version.parse("1.2.3+alpha")
    assert str(v.bump_build().bump_build()) == "1.2.3+alpha.1"


def test_bump_build_no_build_uses_token_unchanged():
    """Without any build, the token logic is unchanged (sanity check)."""
    assert str(Version.parse("1.2.3").bump_build()) == "1.2.3+build.1"
    assert str(Version.parse("1.2.3").bump_build("b")) == "1.2.3+b.1"
    assert str(Version.parse("1.2.3").bump_build("")) == "1.2.3+1"
