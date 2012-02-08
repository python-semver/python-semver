# -*- coding: utf-8 -*-

import re


def parse(version):
    """
    Parse version to major, minor, patch, pre-release, build parts.
    """
    regex = re.compile(r"^([0-9]+)"     # major
                       + r"\.([0-9]+)"  # minor
                       + r"\.([0-9]+)"  # patch
                       + r"(\-[0-9A-Za-z]+(\.[0-9A-Za-z]+)*)?"    # pre-release
                       + r"(\+[0-9A-Za-z]+(\.[0-9A-Za-z]+)*)?$")  # build
    match = regex.match(version)
    if match is None:
        raise ValueError('{0} is not valid SemVer string'.format(version))

    rv = {
        'major': int(match.group(1)),
        'minor': int(match.group(2)),
        'patch': int(match.group(3)),
    }

    if match.group(4):
        rv['prerelease'] = match.group(4).lstrip('-')

    if match.group(6):
        rv['build'] = match.group(6).lstrip('+')

    return rv


def compare(ver1, ver2):
    def compare_by_keys(d1, d2, keys):
        for key in keys:
            v = cmp(d1.get(key), d2.get(key))
            if v != 0:
                return v
        return 0

    v1, v2 = parse(ver1), parse(ver2)

    return compare_by_keys(
        v1, v2, ['major', 'minor', 'patch', 'prerelease', 'build'])


def match(version, match_expr):
    prefix = match_expr[:2]
    if prefix in ('>=', '<=', '=='):
        match_version = match_expr[2:]
    elif prefix[0] in ('>', '<', '='):
        prefix = prefix[0]
        match_version = match_expr[1:]
    else:
        raise ValueError("match_expr parameter should be in format <op><ver>, "
                         "where <op> is one of ['<', '>', '==', '<=', '>=']. "
                         "You provided: {}".format(match_expr))

    possibilities_dict = {
        '>': (1,),
        '<': (-1,),
        '==': (0,),
        '>=': (0, 1),
        '<=': (-1, 0)
    }

    possibilities = possibilities_dict[prefix]
    cmp_res = compare(version, match_version)

    return cmp_res in possibilities
