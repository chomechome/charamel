"""
Charamel: Fast Universal Encoding Detection, Unicode-Flavoured 🍭
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Licensed under Apache 2.0
"""
import codecs

import pytest

from charamel import Encoding


@pytest.mark.parametrize('encoding', Encoding)
def test_exists(encoding):
    assert codecs.lookup(encoding.value)


@pytest.mark.parametrize(
    ('encoding', 'expected'),
    [
        ('utf8', Encoding.UTF_8),
        ('utf_8', Encoding.UTF_8),
        ('utf-8', Encoding.UTF_8),
        ('UTF8', Encoding.UTF_8),
        ('UTF_8', Encoding.UTF_8),
        ('UTF-8', Encoding.UTF_8),
        ('iso-8859-1', Encoding.LATIN_1),
        ('windows_1251', Encoding.CP_1251),
        ('windows-1251', Encoding.CP_1251),
        ('maccentraleurope', Encoding.MAC_LATIN_2),
    ],
)
def test_normalization(encoding, expected):
    assert Encoding(encoding) is expected
