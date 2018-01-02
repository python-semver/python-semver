"""
Python helper for Semantic Versioning (http://semver.org/)
"""

import collections
import re

__version__ = '2.7.9'
__author__ = 'Kostiantyn Rybnikov'
__author_email__ = 'k-bx@k-bx.com'

_REGEX = re.compile(
        r"""
        ^
        (?P<major>(?:0|[1-9][0-9]*))
        (\.
        (?P<minor>(?:0|[1-9][0-9]*)))?
        (\.
        (?P<patch>(?:0|[1-9][0-9]*)))?
        (\-(?P<prerelease>
            (?:0|[1-9A-Za-z-][0-9A-Za-z-]*)
            (\.(?:0|[1-9A-Za-z-][0-9A-Za-z-]*))*
        ))?
        (\+(?P<build>
            [0-9A-Za-z-]+
            (\.[0-9A-Za-z-]+)*
        ))?
        $
        """, re.VERBOSE)

_LAST_NUMBER = re.compile(r'(?:[^\d]*(\d+)[^\d]*)+')

if not hasattr(__builtins__, 'cmp'):
    def cmp(a, b):
        return (a > b) - (a < b)

class semver:
  def __init__(self, version):
    '''
    param version: string, tuple or list
    param strict: when True (default) different buildversions compare equal
    '''
    version = self.parse(version)
    self._set_attrs(version)

  def _set_attrs(self, version):
    # make nice attrs
    self.major      = version['major']
    self.minor      = version['minor']
    self.patch      = version['patch']
    self.prerelease = version['prerelease']
    self.build      = version['build']

  def __str__(self):
    v = str("%d.%d.%d" % (
      self.major,
      self.minor,
      self.patch,
    ))

    v = v + "-%s" % (self.prerelease) if self.prerelease is not None else v
    v = v + "+%s" % (self.build) if self.build is not None else v

    return v

  # v2
  def parse(self, *args):
    '''
    parse string "1.2.3", tuple (1,2,3), list [1,2,3]
    '''
    if type(args[0]) is str:
      version = args[0]
    elif type(args[0]) is tuple or type(args[0]) is list:
      try:
         version = str(args[0][0])
         version = version + ".%s" % (args[0][1])
         version = version + ".%s" % (args[0][2])
         version = version + "-%s" % (args[0][3])
         version = version + "+%s" % (args[0][4])
      except IndexError as e:
         pass

    return parse(version)
  
  # v2
  def compare(self, v1, v2, strict=True):
    return compare(v1, v2, strict)

  # v3
  def cmp(self, v2, strict=True):
    '''
    compare self to other semverobj
    '''
    return compare(self.format(), v2.format(), strict)

  # v2, v3
  def match(self, expr):
    version = self.format()
    return match(version, expr)

  # v2
  def max_ver(self, v1, v2):
    return self.max(v1, v2)

  # v2
  def min_ver(self, v1, v2):
    return self.min(v1, v2)

  # v3
  def max(self, v1, v2):
    return max_ver(v1, v2)

  # v3
  def min(self, v1, v2):
    return min_ver(v1, v2)

  # v2
  def format_version(self, major, minor, patch, prerelease=None, build=None):
    return self.format(major, minor, patch, prerelease, build)

  # v3
  def format(self, *args):
    # accept args as (), [] and {}
    if len(args) > 0:
      v = self.parse(args[0])
      self._set_attrs(v)

    return format_version(
      self.major,
      self.minor,
      self.patch,
      self.prerelease,
      self.build
    )       
        

def parse(version):
    """Parse version to major, minor, patch, pre-release, build parts.

    :param version: version string
    :return: dictionary with the keys 'build', 'major', 'minor', 'patch',
             and 'prerelease'. The prerelease or build keys can be None
             if not provided
    :rtype: dict
    """
    match = _REGEX.match(version)
    if match is None:
        raise ValueError('%s is not valid SemVer string' % version)

    version_parts = match.groupdict()

    version_parts['major'] = int(version_parts['major'])
    version_parts['minor'] = int(version_parts['minor']) if version_parts['minor'] is not None else 0
    version_parts['patch'] = int(version_parts['patch']) if version_parts['patch'] is not None else 0

    return version_parts


class VersionInfo(collections.namedtuple(
        'VersionInfo', 'major minor patch prerelease build')):
    """
    :param int major: version when you make incompatible API changes.
    :param int minor: version when you add functionality in
                      a backwards-compatible manner.
    :param int patch: version when you make backwards-compatible bug fixes.
    :param str prerelease: an optional prerelease string
    :param str build: an optional build string

    >>> import semver
    >>> ver = semver.parse('3.4.5-pre.2+build.4')
    >>> ver
    {'build': 'build.4', 'major': 3, 'minor': 4, 'patch': 5,
    'prerelease': 'pre.2'}
    """
    __slots__ = ()

    def __eq__(self, other):
        if not isinstance(other, (VersionInfo, dict)):
            return NotImplemented
        return _compare_by_keys(self._asdict(), _to_dict(other)) == 0

    def __ne__(self, other):
        if not isinstance(other, (VersionInfo, dict)):
            return NotImplemented
        return _compare_by_keys(self._asdict(), _to_dict(other)) != 0

    def __lt__(self, other):
        if not isinstance(other, (VersionInfo, dict)):
            return NotImplemented
        return _compare_by_keys(self._asdict(), _to_dict(other)) < 0

    def __le__(self, other):
        if not isinstance(other, (VersionInfo, dict)):
            return NotImplemented
        return _compare_by_keys(self._asdict(), _to_dict(other)) <= 0

    def __gt__(self, other):
        if not isinstance(other, (VersionInfo, dict)):
            return NotImplemented
        return _compare_by_keys(self._asdict(), _to_dict(other)) > 0

    def __ge__(self, other):
        if not isinstance(other, (VersionInfo, dict)):
            return NotImplemented
        return _compare_by_keys(self._asdict(), _to_dict(other)) >= 0
 
def _to_dict(obj):
    if isinstance(obj, VersionInfo):
        return obj._asdict()
    return obj


def parse_version_info(version):
    """Parse version string to a VersionInfo instance.

    :param version: version string
    :return: a :class:`VersionInfo` instance
    :rtype: :class:`VersionInfo`
    """
    parts = parse(version)
    version_info = VersionInfo(
            parts['major'], parts['minor'], parts['patch'],
            parts['prerelease'], parts['build'])

    return version_info


def _nat_cmp(a, b):
    def convert(text):
        return int(text) if re.match('^[0-9]+$', text) else text

    def split_key(key):
        return [convert(c) for c in key.split('.')]

    def cmp_prerelease_tag(a, b):
        if isinstance(a, int) and isinstance(b, int):
            return cmp(a, b)
        elif isinstance(a, int):
            return -1
        elif isinstance(b, int):
            return 1
        else:
            return cmp(a, b)

    a, b = a or '', b or ''
    a_parts, b_parts = split_key(a), split_key(b)
    for sub_a, sub_b in zip(a_parts, b_parts):
        cmp_result = cmp_prerelease_tag(sub_a, sub_b)
        if cmp_result != 0:
            return cmp_result
    else:
        return cmp(len(a), len(b))


def _compare_by_keys(d1, d2, strict=True):
    # v is zero when all parts match
    for key in ['major', 'minor', 'patch']:
        v = cmp(d1.get(key), d2.get(key))
        if v:
            return v

    # parts are equal, test prerelease
    rc1, rc2 = d1.get('prerelease'), d2.get('prerelease')
    rccmp = _nat_cmp(rc1, rc2)

    if rccmp:
      if not rc1:
        return 1
      elif not rc2:
        return -1
      else:
        return rccmp

    # compare buildnumber if not strict and all numbers are equal
    if False == strict:
       b1, b2 = d1.get('build'), d2.get('build')
       bcmp = _nat_cmp(b2, b1)
       return bcmp
    
    # seems equal
    return 0

def compare(ver1, ver2, strict=True):
    """Compare two versions

    :param ver1: version string 1
    :param ver2: version string 2
    :return: The return value is negative if ver1 < ver2,
             zero if ver1 == ver2 and strictly positive if ver1 > ver2
    :rtype: int
    """

    v1, v2 = parse(ver1), parse(ver2)

    return _compare_by_keys(v1, v2, strict)


def match(version, match_expr):
    """Compare two versions through a comparison

    :param str version: a version string
    :param str match_expr: operator and version; valid operators are
          <   smaller than
          >   greater than
          >=  greator or equal than
          <=  smaller or equal than
          ==  equal
          !=  not equal
    :return: True if the expression matches the version, otherwise False
    :rtype: bool
    """
    prefix = match_expr[:2]
    if prefix in ('>=', '<=', '==', '!='):
        match_version = match_expr[2:]
    elif prefix and prefix[0] in ('>', '<'):
        prefix = prefix[0]
        match_version = match_expr[1:]
    else:
        raise ValueError("match_expr parameter should be in format <op><ver>, "
                         "where <op> is one of "
                         "['<', '>', '==', '<=', '>=', '!=']. "
                         "You provided: %r" % match_expr)

    possibilities_dict = {
        '>': (1,),
        '<': (-1,),
        '==': (0,),
        '!=': (-1, 1),
        '>=': (0, 1),
        '<=': (-1, 0)
    }

    possibilities = possibilities_dict[prefix]
    cmp_res = compare(version, match_version)

    return cmp_res in possibilities


def max_ver(ver1, ver2):
    """Returns the greater version of two versions

    :param ver1: version string 1
    :param ver2: version string 2
    :return: the greater version of the two
    :rtype: :class:`VersionInfo`
    """
    cmp_res = compare(ver1, ver2)
    if cmp_res == 0 or cmp_res == 1:
        return ver1
    else:
        return ver2


def min_ver(ver1, ver2):
    """Returns the smaller version of two versions

    :param ver1: version string 1
    :param ver2: version string 2
    :return: the smaller version of the two
    :rtype: :class:`VersionInfo`
    """
    cmp_res = compare(ver1, ver2)
    if cmp_res == 0 or cmp_res == -1:
        return ver1
    else:
        return ver2


def format_version(major, minor, patch, prerelease=None, build=None):
    """Format a version according to the Semantic Versioning specification

    :param str major: the required major part of a version
    :param str minor: the required minor part of a version
    :param str patch: the required patch part of a version
    :param str prerelease: the optional prerelease part of a version
    :param str build: the optional build part of a version
    :return: the formatted string
    :rtype: str
    """
    version = "%d.%d.%d" % (major, minor, patch)
    if prerelease is not None:
        version = version + "-%s" % prerelease

    if build is not None:
        version = version + "+%s" % build

    return version


def _increment_string(string):
    """
    Look for the last sequence of number(s) in a string and increment, from:
    http://code.activestate.com/recipes/442460-increment-numbers-in-a-string/#c1
    """
    match = _LAST_NUMBER.search(string)
    if match:
        next_ = str(int(match.group(1)) + 1)
        start, end = match.span(1)
        string = string[:max(end - len(next_), start)] + next_ + string[end:]
    return string


def bump_major(version):
    """Raise the major part of the version

    :param: version string
    :return: the raised version string
    :rtype: str
    """
    verinfo = parse(version)
    return format_version(verinfo['major'] + 1, 0, 0)


def bump_minor(version):
    """Raise the minor part of the version

    :param: version string
    :return: the raised version string
    :rtype: str
    """
    verinfo = parse(version)
    return format_version(verinfo['major'], verinfo['minor'] + 1, 0)


def bump_patch(version):
    """Raise the patch part of the version

    :param: version string
    :return: the raised version string
    :rtype: str
    """
    verinfo = parse(version)
    return format_version(verinfo['major'], verinfo['minor'],
                          verinfo['patch'] + 1)


def bump_prerelease(version, token='rc'):
    """Raise the prerelease part of the version

    :param version: version string
    :param token: defaults to 'rc'
    :return: the raised version string
    :rtype: str
    """
    verinfo = parse(version)
    verinfo['prerelease'] = _increment_string(
        verinfo['prerelease'] or (token or 'rc') + '.0'
    )
    return format_version(verinfo['major'], verinfo['minor'], verinfo['patch'],
                          verinfo['prerelease'])


def bump_build(version, token='build'):
    """Raise the build part of the version

    :param version: version string
    :param token: defaults to 'build'
    :return: the raised version string
    :rtype: str
    """
    verinfo = parse(version)
    verinfo['build'] = _increment_string(
        verinfo['build'] or (token or 'build') + '.0'
    )
    return format_version(verinfo['major'], verinfo['minor'], verinfo['patch'],
                          verinfo['prerelease'], verinfo['build'])


def finalize_version(version):
    """Remove any prerelease and build metadata from the version

    :param version: version string
    :return: the finalized version string
    :rtype: str
    """
    verinfo = parse(version)
    return format_version(verinfo['major'], verinfo['minor'], verinfo['patch'])
