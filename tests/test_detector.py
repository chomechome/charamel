"""
🌏 Charamel: Truly Universal Encoding Detection in Python 🌎
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Licensed under Apache 2.0
"""
import pytest

from charamel import Detector, Encoding
from tests.fixtures import FIXTURE_DIRECTORY, iter_fixtures
from tests.utils import expectedly_fail, is_correct_encoding


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
        ('김성식', Encoding.EUC_KR),
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
        ('👍', Encoding.UTF_8),
        ('\x000', Encoding.UTF_16),
        ('<\xa0', Encoding.ISO_8859_7),
        ('\x1b', Encoding.ISO_2022_JP),
        ('\x0f', Encoding.ISO_2022_KR),
    ],
)
def test_decode(detector, text, encoding):
    content = text.encode(encoding)
    encoding = detector.detect(content)
    assert is_correct_encoding(content, encoding, text)


@pytest.mark.parametrize(
    ('content', 'expected'),
    [(b'\xc4\xe3\xba\xc3', {Encoding.GB_K, Encoding.GB_2312, Encoding.GB_18030})],
)
def test_probe(detector, content, expected):
    probes = detector.probe(content)
    assert {enc for enc, _ in probes} == expected


_KNOWN_FAILURES = {
    FIXTURE_DIRECTORY / Encoding.BIG_5 / 'coolloud.org.tw.xml',
    FIXTURE_DIRECTORY / Encoding.BIG_5 / 'upsaid.com.xml',
    FIXTURE_DIRECTORY / Encoding.CP_932 / 'hardsoft.at.webry.info.xml',
    FIXTURE_DIRECTORY / Encoding.CP_932 / 'www2.chuo-u.ac.jp-suishin.xml',
    FIXTURE_DIRECTORY / Encoding.ISO_8859_11 / 'th.txt',
    FIXTURE_DIRECTORY / Encoding.UTF_16_BE / 'af.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_16_BE / 'bom-utf-16-be.srt',
    FIXTURE_DIRECTORY / Encoding.UTF_16_BE / 'br.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_16_BE / 'ca.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_16_BE / 'da.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_16_BE / 'et.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_16_BE / 'eu.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_16_BE / 'fi.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_16_BE / 'gl.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_16_BE / 'ms.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_16_BE / 'no.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_16_BE / 'sv.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_16_LE / 'bom-utf-16-le.srt',
    FIXTURE_DIRECTORY / Encoding.UTF_16_LE / 'da.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_16_LE / 'fi.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_16_LE / 'id.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_16_LE / 'sq.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_16_LE / 'tl.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_32 / 'bom-utf-32-be.srt',
    FIXTURE_DIRECTORY / Encoding.UTF_32_BE / 'af.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_32_BE / 'br.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_32_BE / 'ca.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_32_BE / 'da.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_32_BE / 'et.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_32_BE / 'eu.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_32_BE / 'fi.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_32_BE / 'gl.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_32_BE / 'id.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_32_BE / 'ms.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_32_BE / 'no.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_32_BE / 'sq.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_32_BE / 'sv.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_32_BE / 'tl.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_32_LE / 'af.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_32_LE / 'br.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_32_LE / 'ca.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_32_LE / 'et.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_32_LE / 'eu.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_32_LE / 'gl.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_32_LE / 'id.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_32_LE / 'ms.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_32_LE / 'no.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_32_LE / 'sq.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_32_LE / 'sv.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_32_LE / 'tl.xml',
    FIXTURE_DIRECTORY / Encoding.UTF_7 / 'ze.xml',
}


def _iter_fixtures_with_known_failures():
    for path, encoding in iter_fixtures():
        if path in _KNOWN_FAILURES:
            yield expectedly_fail(path, encoding, reason='Known detection failure')
        else:
            yield path, encoding


@pytest.mark.parametrize(('path', 'encoding'), _iter_fixtures_with_known_failures())
def test_files(detector, path, encoding):
    with path.open('rb') as f:
        content = f.read()

    expected = content.decode(encoding)
    encoding = detector.detect(content)
    assert is_correct_encoding(content, encoding, expected)
