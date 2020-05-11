"""
🌏 Charamel: Truly Universal Encoding Detection in Python 🌎
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Licensed under Apache 2.0
"""
import re
from typing import Optional

import pytest

from charamel import Encoding


def normalize(text: str) -> str:
    """
    Normalize symbols from different character sets

    tilda: ~
    big5: ∼
    cp932, cp950: ～
    shift_jis: 〜

    dash: -
    gb2312: ―
    gb18030: —
    shift_jis: −
    cp932: －

    Args:
        text: Decoded text

    Returns:
        Text with normalized characters
    """
    for pattern, replacement in [
        (r'[∼～〜]', '~'),
        (r'[―—−－]', '-'),
    ]:
        text = re.sub(pattern, replacement, text)

    return text


def is_correct_encoding(
    content: bytes, encoding: Optional[Encoding], expected: str
) -> bool:
    """
    Check that decoded byte content is equal to expected unicode text

    Args:
        content: Encoded text
        encoding: Detected encoding or `None`
        expected: Expected unicode text

    Returns:
        Whether encoding decodes `content` correctly
    """
    if encoding is None:
        return False

    try:
        actual = content.decode(encoding)
        return normalize(actual) == normalize(expected)
    except ValueError:
        return False


def skip(*values, reason: str = ''):
    """
    Skip `pytest.mark.parametrize` test item

    Args:
        values: Test item arguments
        reason: Reason to skip this item

    Returns:
        Skipped test item
    """
    return pytest.param(*values, marks=pytest.mark.skip(reason=reason))
