"""
🌏 Charamel: Truly Universal Encoding Detection in Python 🌎
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Licensed under Apache 2.0
"""
import functools
import gzip
import pathlib
import struct
from typing import Any, Dict, List, Sequence

from charamel.encoding import Encoding

RESOURCE_DIRECTORY = pathlib.Path(__file__).parent.absolute()
WEIGHT_DIRECTORY = RESOURCE_DIRECTORY / 'weights'


def _unpack(file: pathlib.Path, pattern: str) -> List[Any]:
    """
    Unpack struct values from file

    Args:
        file: File that stores struct-packed values
        pattern: Struct pattern

    Returns:
        List of unpacked values
    """
    with gzip.open(file, 'rb') as data:
        return [values[0] for values in struct.iter_unpack(pattern, data.read())]


@functools.lru_cache(maxsize=None)
def _load_biases() -> Dict[str, float]:
    """
    Load all linear model bias values

    Returns:
        Mapping from encoding names to their biases
    """
    biases = {}
    with gzip.open(RESOURCE_DIRECTORY / 'biases.gzip', 'rb') as data:
        for line in data:
            encoding, bias = line.decode().split()
            biases[encoding] = float(bias)

    return biases


@functools.lru_cache(maxsize=len(Encoding))
def _load_weights(encoding: Encoding) -> List[float]:
    """
    Load feature weights for a single encodings

    Args:
        encoding: Character encoding

    Returns:
        List of encoding feature weights
    """
    return _unpack(WEIGHT_DIRECTORY / f'{encoding}.gzip', pattern='>e')


@functools.lru_cache(maxsize=None)
def load_features() -> Dict[int, int]:
    """
    Load byte-level feature names and indices

    Returns:
        Mapping from features to their indices in weight matrix
    """
    features = _unpack(RESOURCE_DIRECTORY / 'features.gzip', pattern='>H')
    return {feature: index for index, feature in enumerate(features)}


def load_biases(encodings: Sequence[Encoding]) -> Dict[Encoding, float]:
    """
    Load linear model bias values for given encodings

    Args:
        encodings: List of encodings

    Returns:
        Mapping from encodings to their biases
    """
    biases = _load_biases()
    return {encoding: biases[encoding] for encoding in encodings}


def load_weights(encodings: Sequence[Encoding]) -> Dict[Encoding, List[float]]:
    """
    Load feature weights for specified encodings

    Args:
        encodings: List of encodings

    Returns:
        Mapping from encoding to its feature weights
    """
    return {encoding: _load_weights(encoding) for encoding in encodings}
