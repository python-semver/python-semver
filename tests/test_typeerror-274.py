import sys

import pytest

import semver

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


def ensure_binary(s, encoding="utf-8", errors="strict"):
    """
    Coerce ``s`` to bytes.

    * `str` -> encoded to `bytes`
    * `bytes` -> `bytes`

    :param s: the string to convert
    :type s: str | bytes
    :param encoding: the encoding to apply, defaults to "utf-8"
    :type encoding: str
    :param errors: set a different error handling scheme;
      other possible values are `ignore`, `replace`, and
      `xmlcharrefreplace` as well as any other name
      registered with :func:`codecs.register_error`.
      Defaults to "strict".
    :type errors: str
    :raises TypeError: if ``s`` is not str or bytes type
    :return: the converted string
    :rtype: str
    """
    if isinstance(s, str):
        return s.encode(encoding, errors)
    elif isinstance(s, bytes):
        return s
    else:
        raise TypeError("not expecting type '%s'" % type(s))


def test_should_work_with_string_and_unicode():
    result = semver.compare("1.1.0", b"1.2.2")
    assert result == -1
    result = semver.compare(b"1.1.0", "1.2.2")
    assert result == -1


class TestEnsure:
    # From six project
    # grinning face emoji
    UNICODE_EMOJI = "\U0001F600"
    BINARY_EMOJI = b"\xf0\x9f\x98\x80"

    def test_ensure_binary_raise_type_error(self):
        with pytest.raises(TypeError):
            semver.ensure_str(8)

    def test_errors_and_encoding(self):
        ensure_binary(self.UNICODE_EMOJI, encoding="latin-1", errors="ignore")
        with pytest.raises(UnicodeEncodeError):
            ensure_binary(self.UNICODE_EMOJI, encoding="latin-1", errors="strict")

    def test_ensure_binary_raise(self):
        converted_unicode = ensure_binary(
            self.UNICODE_EMOJI, encoding="utf-8", errors="strict"
        )
        converted_binary = ensure_binary(
            self.BINARY_EMOJI, encoding="utf-8", errors="strict"
        )

        # PY3: str -> bytes
        assert converted_unicode == self.BINARY_EMOJI and isinstance(
            converted_unicode, bytes
        )
        # PY3: bytes -> bytes
        assert converted_binary == self.BINARY_EMOJI and isinstance(
            converted_binary, bytes
        )

    def test_ensure_str(self):
        converted_unicode = semver.ensure_str(
            self.UNICODE_EMOJI, encoding="utf-8", errors="strict"
        )
        converted_binary = semver.ensure_str(
            self.BINARY_EMOJI, encoding="utf-8", errors="strict"
        )

        # PY3: str -> str
        assert converted_unicode == self.UNICODE_EMOJI and isinstance(
            converted_unicode, str
        )
        # PY3: bytes -> str
        assert converted_binary == self.UNICODE_EMOJI and isinstance(
            converted_unicode, str
        )
