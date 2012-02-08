# -*- coding: utf-8 -*-

import re

_REGEX = re.compile('^(?P<major>[0-9]+)'
                    '\.(?P<minor>[0-9]+)'
                    '\.(?P<patch>[0-9]+)'
                    '(\-(?P<prerelease>[0-9A-Za-z]+(\.[0-9A-Za-z]+)*))?'
                    '(\+(?P<build>[0-9A-Za-z]+(\.[0-9A-Za-z]+)*))?$')

def parse(version):
    """
    Parse version to major, minor, patch, pre-release, build parts.
    """
    match = _REGEX.match(version)
    if match is None:
        raise ValueError('%s is not valid SemVer string' % version)

    verinfo = match.groupdict()

    verinfo['major'] = int(verinfo['major'])
    verinfo['minor'] = int(verinfo['minor'])
    verinfo['patch'] = int(verinfo['patch'])

    return verinfo


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
    elif prefix and prefix[0] in ('>', '<', '='):
        prefix = prefix[0]
        match_version = match_expr[1:]
    else:
        raise ValueError("match_expr parameter should be in format <op><ver>, "
                         "where <op> is one of ['<', '>', '==', '<=', '>=']. "
                         "You provided: %r" % match_expr)

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
