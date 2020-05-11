"""
🌏 Charamel: Truly Universal Encoding Detection in Python 🌎
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Licensed under Apache 2.0
"""
import pathlib
from typing import Iterator, Tuple

from charamel import Encoding

FIXTURE_DIRECTORY = pathlib.Path(__file__).parent.absolute()


def iter_fixtures() -> Iterator[Tuple[pathlib.Path, Encoding]]:
    """
    Iterate over all test files

    Returns:
        Iterator over file paths and their corresponding encodings
    """
    for extension in 'txt', 'xml', 'html', 'csv', 'srt':
        for path in FIXTURE_DIRECTORY.glob(f'**/*.{extension}'):
            encoding = path.parts[-2]
            yield path, Encoding(encoding)
