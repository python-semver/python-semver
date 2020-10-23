from argparse import Namespace
from contextlib import contextmanager
from unittest.mock import patch

import pytest

from semver import (
    cmd_bump,
    cmd_check,
    cmd_compare,
    cmd_nextver,
    createparser,
    main,
    __main__,
)


@contextmanager
def does_not_raise(item):
    yield item


@pytest.mark.parametrize(
    "cli,expected",
    [
        (["bump", "major", "1.2.3"], Namespace(bump="major", version="1.2.3")),
        (["bump", "minor", "1.2.3"], Namespace(bump="minor", version="1.2.3")),
        (["bump", "patch", "1.2.3"], Namespace(bump="patch", version="1.2.3")),
        (
            ["bump", "prerelease", "1.2.3"],
            Namespace(bump="prerelease", version="1.2.3"),
        ),
        (["bump", "build", "1.2.3"], Namespace(bump="build", version="1.2.3")),
        # ---
        (["compare", "1.2.3", "2.1.3"], Namespace(version1="1.2.3", version2="2.1.3")),
        # ---
        (["check", "1.2.3"], Namespace(version="1.2.3")),
    ],
)
def test_should_parse_cli_arguments(cli, expected):
    parser = createparser()
    assert parser
    result = parser.parse_args(cli)
    del result.func
    assert result == expected


@pytest.mark.parametrize(
    "func,args,expectation",
    [
        # bump subcommand
        (cmd_bump, Namespace(bump="major", version="1.2.3"), does_not_raise("2.0.0")),
        (cmd_bump, Namespace(bump="minor", version="1.2.3"), does_not_raise("1.3.0")),
        (cmd_bump, Namespace(bump="patch", version="1.2.3"), does_not_raise("1.2.4")),
        (
            cmd_bump,
            Namespace(bump="prerelease", version="1.2.3-rc1"),
            does_not_raise("1.2.3-rc2"),
        ),
        (
            cmd_bump,
            Namespace(bump="build", version="1.2.3+build.13"),
            does_not_raise("1.2.3+build.14"),
        ),
        # compare subcommand
        (
            cmd_compare,
            Namespace(version1="1.2.3", version2="2.1.3"),
            does_not_raise("-1"),
        ),
        (
            cmd_compare,
            Namespace(version1="1.2.3", version2="1.2.3"),
            does_not_raise("0"),
        ),
        (
            cmd_compare,
            Namespace(version1="2.4.0", version2="2.1.3"),
            does_not_raise("1"),
        ),
        # check subcommand
        (cmd_check, Namespace(version="1.2.3"), does_not_raise(None)),
        (cmd_check, Namespace(version="1.2"), pytest.raises(ValueError)),
        # nextver subcommand
        (
            cmd_nextver,
            Namespace(version="1.2.3", part="major"),
            does_not_raise("2.0.0"),
        ),
        (
            cmd_nextver,
            Namespace(version="1.2", part="major"),
            pytest.raises(ValueError),
        ),
        (
            cmd_nextver,
            Namespace(version="1.2.3", part="nope"),
            pytest.raises(ValueError),
        ),
    ],
)
def test_should_process_parsed_cli_arguments(func, args, expectation):
    with expectation as expected:
        result = func(args)
        assert result == expected


def test_should_process_print(capsys):
    rc = main(["bump", "major", "1.2.3"])
    assert rc == 0
    captured = capsys.readouterr()
    assert captured.out.rstrip() == "2.0.0"


def test_should_process_raise_error(capsys):
    rc = main(["bump", "major", "1.2"])
    assert rc != 0
    captured = capsys.readouterr()
    assert captured.err.startswith("ERROR")


def test_should_raise_systemexit_when_called_with_empty_arguments():
    with pytest.raises(SystemExit):
        main([])


def test_should_raise_systemexit_when_bump_iscalled_with_empty_arguments():
    with pytest.raises(SystemExit):
        main(["bump"])


def test_should_process_check_iscalled_with_valid_version(capsys):
    result = main(["check", "1.1.1"])
    assert not result
    captured = capsys.readouterr()
    assert not captured.out


@pytest.mark.parametrize("package_name", ["", "semver"])
def test_main_file_should_call_cli_main(package_name):
    with patch("semver.__main__.cli.main") as mocked_main:
        with patch("semver.__main__.__package__", package_name):
            __main__.main()
            mocked_main.assert_called_once()
