"""
Charamel: Fast Universal Encoding Detection, Unicode-Flavoured 🍭
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Licensed under Apache 2.0
"""
import pytest

from charamel import Detector, Encoding
from tests.fixtures import iter_fixtures
from tests.utils import is_correct_encoding


@pytest.fixture(name='detector', scope='session')
def _get_detector():
    return Detector()


def test_no_encodings():
    with pytest.raises(ValueError, match='No encodings specified'):
        Detector(encodings=[])


@pytest.mark.parametrize('min_confidence', [-0.001, 1.001])
def test_incorrect_min_confidence(min_confidence):
    with pytest.raises(ValueError, match='min_confidence must be in range'):
        Detector(min_confidence=min_confidence)


@pytest.mark.parametrize(
    ('text', 'encoding'),
    [
        ('hello', Encoding.ASCII),
        ('русский', Encoding.UTF_8),
        ('മലയാളം', Encoding.UTF_8),
        ('ᠮᠠᠨᠵᡠ ᡤᡳᠰᡠᠨ', Encoding.UTF_8),
        ('國語', Encoding.UTF_8),
        ('मराठी', Encoding.UTF_8),
        ('মনিপুরি, মৈতৈলোল্, মৈতৈলোন্, মৈথৈ', Encoding.UTF_8),
        ('闽北语', Encoding.UTF_8),
        ('ဘာသာ မန်', Encoding.UTF_8),
        ('ᠮᠣᠨᠭᠭᠣᠯ ᠬᠡᠯᠡ', Encoding.UTF_8),
        ('ꆈꌠ꒿', Encoding.UTF_8),
        ('ଓଡ଼ିଆ', Encoding.UTF_8),
        ('ᐊᓂᔑᓈᐯᒧᐎᓐ', Encoding.UTF_8),
        ('ウチナーヤマトゥグチ', Encoding.UTF_8),
        ('† -', Encoding.UTF_8),
        ('Română', Encoding.UTF_8),
        ('anarâškielâ', Encoding.UTF_8),
        ('လိၵ်ႈတႆး', Encoding.UTF_8),
        ('འབྲས་ལྗོངས་', Encoding.UTF_8),
        ('schwyzerdütsch', Encoding.UTF_8),
        ('ትግርኛ', Encoding.UTF_8),
        ('ᠰᡞᠪᡝᡤᡞᠰᡠᠨ', Encoding.UTF_8),
        ('ꡖꡍꡂꡛ ꡌ', Encoding.UTF_8),
        ('Հայկական Այբուբեն', Encoding.UTF_8),
        ('⠃⠗⠁⠊⠇⠑', Encoding.UTF_8),
        ('𐒄𐒋𐒦𐒩𐒗𐒓', Encoding.UTF_8),
        ('𐊴𐊠𐊥𐊹𐊠𐊵', Encoding.UTF_8),
        ('ⰍⱛⰓⰊⰎⰎⰑⰂⱄⰜⰀ', Encoding.UTF_8),
        ('Кѷрїлловица', Encoding.UTF_8),
        ('𐐔𐐯𐑅𐐨𐑉𐐯𐐻', Encoding.UTF_8),
        ('𐑖𐑱𐑝𐑾𐑯', Encoding.UTF_8),
        ('ᚱᚢᚾᛟ', Encoding.UTF_8),
        ('français', Encoding.UTF_16),
        ('español', Encoding.UTF_32),
        ('你好', Encoding.BIG_5),
        ('你好', Encoding.BIG_5_HKSCS),
        ('你好', Encoding.GB_2312),
        ('你好', Encoding.GB_18030),
        ('你好', Encoding.GB_K),
        ('привет', Encoding.CP_1251),
        ('привет', Encoding.KOI_8_R),
        ('привет', Encoding.KOI_8_U),
        ('Carter’s Janitorial', Encoding.UTF_8),
        ('Carter’s Janitorial', Encoding.UTF_16),
        ('Carter’s Janitorial', Encoding.UTF_32),
        ('El español o castellano es una lengua romance', Encoding.UTF_8),
        ('El español o castellano es una lengua romance', Encoding.LATIN_1),
        ('El español o castellano es una lengua romance', Encoding.ISO_8859_14),
        ('Réseau Démographie de l\'Agence universitaire', Encoding.UTF_8),
        ('Réseau Démographie de l\'Agence universitaire', Encoding.LATIN_1),
        ('Réseau Démographie de l\'Agence universitaire', Encoding.ISO_8859_14),
        ('поетів до дня поезії', Encoding.UTF_8),
        ('поетів до дня поезії', Encoding.CP_1251),
        ('поетів до дня поезії', Encoding.KOI_8_U),
        ('¼ + ½', Encoding.UTF_8),
    ],
)
def test_decode(detector, text, encoding):
    content = text.encode(encoding)
    encoding = detector.detect(content)
    assert is_correct_encoding(content, encoding, text)


@pytest.mark.parametrize(
    ('path', 'encoding'), list(iter_fixtures()),
)
def test_files(detector, path, encoding):
    with path.open('rb') as f:
        content = f.read()

    expected = content.decode(encoding)
    encoding = detector.detect(content)
    assert is_correct_encoding(content, encoding, expected)
