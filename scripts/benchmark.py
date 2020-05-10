"""
Charamel: Fast Universal Encoding Detection, Unicode-Flavoured 🍭
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Licensed under Apache 2.0
"""
import collections
import logging
import statistics
import sys
import time
import warnings
from typing import Any, Dict, List

import cchardet
import chardet
import charset_normalizer
import tabulate
import termcolor

import charamel
from tests.fixtures import iter_fixtures
from tests.utils import is_correct_encoding

LOGGER = logging.getLogger('benchmark')

CHARAMEL_DETECTOR = charamel.Detector()

DOUBLE_LINE = termcolor.colored('=' * 80, 'blue')
TOTAL = 'Total'
ASTERISK = ' *'


def _get_detector_name(module: Any) -> str:
    name = '-'.join(word.capitalize() for word in module.__name__.split('_'))
    return f'{name} v{module.__version__}'


CHARDET = _get_detector_name(chardet)
C_CHARDET = _get_detector_name(cchardet)
CHARSET_NORMALIZER = _get_detector_name(charset_normalizer)
CHARAMEL = _get_detector_name(charamel)

DETECTORS = {
    CHARDET: lambda c: chardet.detect(c)['encoding'],
    C_CHARDET: lambda c: cchardet.detect(c)['encoding'],
    CHARSET_NORMALIZER: lambda c: charset_normalizer.detect(c)['encoding'],
    CHARAMEL: lambda c: CHARAMEL_DETECTOR.detect(c),
}
SUPPORTED_ENCODINGS = {
    CHARDET: {
        charamel.Encoding.ASCII,
        charamel.Encoding.UTF_8,
        charamel.Encoding.UTF_16,
        charamel.Encoding.UTF_32,
        charamel.Encoding.BIG_5,
        charamel.Encoding.GB_2312,
        charamel.Encoding.HZ,
        charamel.Encoding.EUC_JP,
        charamel.Encoding.SHIFT_JIS,
        charamel.Encoding.CP_932,
        charamel.Encoding.ISO_2022_JP,
        charamel.Encoding.EUC_KR,
        charamel.Encoding.ISO_2022_KR,
        charamel.Encoding.KOI_8_R,
        charamel.Encoding.MAC_CYRILLIC,
        charamel.Encoding.CP_855,
        charamel.Encoding.CP_866,
        charamel.Encoding.ISO_8859_5,
        charamel.Encoding.CP_1251,
        charamel.Encoding.ISO_8859_5,
        charamel.Encoding.CP_1251,
        charamel.Encoding.LATIN_1,
        charamel.Encoding.CP_1252,
        charamel.Encoding.ISO_8859_7,
        charamel.Encoding.CP_1253,
        charamel.Encoding.ISO_8859_8,
        charamel.Encoding.CP_1255,
        charamel.Encoding.TIS_620,
    },
    C_CHARDET: {
        charamel.Encoding.UTF_8,
        charamel.Encoding.UTF_16_BE,
        charamel.Encoding.UTF_16_LE,
        charamel.Encoding.UTF_32_BE,
        charamel.Encoding.UTF_32_LE,
        charamel.Encoding.ISO_8859_6,
        charamel.Encoding.CP_1256,
        charamel.Encoding.ISO_8859_5,
        charamel.Encoding.CP_1251,
        charamel.Encoding.BIG_5,
        charamel.Encoding.GB_18030,
        charamel.Encoding.HZ,
        charamel.Encoding.ISO_8859_2,
        charamel.Encoding.ISO_8859_13,
        charamel.Encoding.ISO_8859_16,
        charamel.Encoding.CP_1250,
        charamel.Encoding.CP_852,
        charamel.Encoding.CP_1250,
        charamel.Encoding.ISO_8859_2,
        charamel.Encoding.CP_852,
        charamel.Encoding.LATIN_1,
        charamel.Encoding.ISO_8859_15,
        charamel.Encoding.CP_1252,
        charamel.Encoding.ASCII,
        charamel.Encoding.ISO_8859_3,
        charamel.Encoding.ISO_8859_4,
        charamel.Encoding.ISO_8859_13,
        charamel.Encoding.ISO_8859_13,
        charamel.Encoding.CP_1252,
        charamel.Encoding.CP_1257,
        charamel.Encoding.LATIN_1,
        charamel.Encoding.ISO_8859_4,
        charamel.Encoding.ISO_8859_9,
        charamel.Encoding.ISO_8859_13,
        charamel.Encoding.ISO_8859_15,
        charamel.Encoding.CP_1252,
        charamel.Encoding.LATIN_1,
        charamel.Encoding.ISO_8859_15,
        charamel.Encoding.CP_1252,
        charamel.Encoding.LATIN_1,
        charamel.Encoding.CP_1252,
        charamel.Encoding.ISO_8859_7,
        charamel.Encoding.CP_1253,
        charamel.Encoding.ISO_8859_8,
        charamel.Encoding.CP_1255,
        charamel.Encoding.ISO_8859_2,
        charamel.Encoding.CP_1250,
        charamel.Encoding.LATIN_1,
        charamel.Encoding.ISO_8859_9,
        charamel.Encoding.ISO_8859_15,
        charamel.Encoding.CP_1252,
        charamel.Encoding.LATIN_1,
        charamel.Encoding.ISO_8859_3,
        charamel.Encoding.ISO_8859_9,
        charamel.Encoding.ISO_8859_15,
        charamel.Encoding.CP_1252,
        charamel.Encoding.ISO_2022_JP,
        charamel.Encoding.SHIFT_JIS,
        charamel.Encoding.EUC_JP,
        charamel.Encoding.ISO_2022_KR,
        charamel.Encoding.EUC_KR,
        charamel.Encoding.CP_949,
        charamel.Encoding.ISO_8859_4,
        charamel.Encoding.ISO_8859_10,
        charamel.Encoding.ISO_8859_13,
        charamel.Encoding.ISO_8859_4,
        charamel.Encoding.ISO_8859_10,
        charamel.Encoding.ISO_8859_13,
        charamel.Encoding.ISO_8859_3,
        charamel.Encoding.ISO_8859_2,
        charamel.Encoding.ISO_8859_13,
        charamel.Encoding.ISO_8859_16,
        charamel.Encoding.CP_1250,
        charamel.Encoding.CP_852,
        charamel.Encoding.LATIN_1,
        charamel.Encoding.ISO_8859_9,
        charamel.Encoding.ISO_8859_15,
        charamel.Encoding.CP_1252,
        charamel.Encoding.ISO_8859_2,
        charamel.Encoding.ISO_8859_16,
        charamel.Encoding.CP_1250,
        charamel.Encoding.CP_852,
        charamel.Encoding.ISO_8859_5,
        charamel.Encoding.KOI_8_R,
        charamel.Encoding.CP_1251,
        charamel.Encoding.MAC_CYRILLIC,
        charamel.Encoding.CP_866,
        charamel.Encoding.CP_855,
        charamel.Encoding.CP_1250,
        charamel.Encoding.ISO_8859_2,
        charamel.Encoding.CP_852,
        charamel.Encoding.ISO_8859_2,
        charamel.Encoding.ISO_8859_16,
        charamel.Encoding.CP_1250,
        charamel.Encoding.CP_852,
    },
    CHARSET_NORMALIZER: {
        charamel.Encoding.ASCII,
        charamel.Encoding.BIG_5,
        charamel.Encoding.BIG_5_HKSCS,
        charamel.Encoding.CP_037,
        charamel.Encoding.CP_1026,
        charamel.Encoding.CP_1125,
        charamel.Encoding.CP_1140,
        charamel.Encoding.CP_1250,
        charamel.Encoding.CP_1251,
        charamel.Encoding.CP_1252,
        charamel.Encoding.CP_1253,
        charamel.Encoding.CP_1254,
        charamel.Encoding.CP_1255,
        charamel.Encoding.CP_1256,
        charamel.Encoding.CP_1257,
        charamel.Encoding.CP_1258,
        charamel.Encoding.CP_273,
        charamel.Encoding.CP_424,
        charamel.Encoding.CP_437,
        charamel.Encoding.CP_500,
        charamel.Encoding.CP_775,
        charamel.Encoding.CP_850,
        charamel.Encoding.CP_852,
        charamel.Encoding.CP_855,
        charamel.Encoding.CP_857,
        charamel.Encoding.CP_858,
        charamel.Encoding.CP_860,
        charamel.Encoding.CP_861,
        charamel.Encoding.CP_862,
        charamel.Encoding.CP_863,
        charamel.Encoding.CP_864,
        charamel.Encoding.CP_865,
        charamel.Encoding.CP_866,
        charamel.Encoding.CP_869,
        charamel.Encoding.CP_932,
        charamel.Encoding.CP_949,
        charamel.Encoding.CP_950,
        charamel.Encoding.EUC_JIS_2004,
        charamel.Encoding.EUC_JIS_X_0213,
        charamel.Encoding.EUC_JP,
        charamel.Encoding.EUC_KR,
        charamel.Encoding.GB_18030,
        charamel.Encoding.GB_2312,
        charamel.Encoding.GB_K,
        charamel.Encoding.HZ,
        charamel.Encoding.ISO_2022_JP,
        charamel.Encoding.ISO_2022_JP_1,
        charamel.Encoding.ISO_2022_JP_2,
        charamel.Encoding.ISO_2022_JP_3,
        charamel.Encoding.ISO_2022_JP_EXT,
        charamel.Encoding.ISO_2022_KR,
        charamel.Encoding.ISO_8859_10,
        charamel.Encoding.ISO_8859_11,
        charamel.Encoding.ISO_8859_13,
        charamel.Encoding.ISO_8859_14,
        charamel.Encoding.ISO_8859_15,
        charamel.Encoding.ISO_8859_16,
        charamel.Encoding.ISO_8859_2,
        charamel.Encoding.ISO_8859_3,
        charamel.Encoding.ISO_8859_4,
        charamel.Encoding.ISO_8859_5,
        charamel.Encoding.ISO_8859_6,
        charamel.Encoding.ISO_8859_7,
        charamel.Encoding.ISO_8859_8,
        charamel.Encoding.ISO_8859_9,
        charamel.Encoding.ISO_2022_JP_2004,
        charamel.Encoding.JOHAB,
        charamel.Encoding.KOI_8_R,
        charamel.Encoding.KZ_1048,
        charamel.Encoding.LATIN_1,
        charamel.Encoding.MAC_CYRILLIC,
        charamel.Encoding.MAC_GREEK,
        charamel.Encoding.MAC_ICELAND,
        charamel.Encoding.MAC_LATIN_2,
        charamel.Encoding.MAC_ROMAN,
        charamel.Encoding.MAC_TURKISH,
        charamel.Encoding.PTCP_154,
        charamel.Encoding.SHIFT_JIS,
        charamel.Encoding.SHIFT_JIS_2004,
        charamel.Encoding.SHIFT_JIS_X_0213,
        charamel.Encoding.TIS_620,
        charamel.Encoding.UTF_16,
        charamel.Encoding.UTF_16_BE,
        charamel.Encoding.UTF_16_LE,
        charamel.Encoding.UTF_32,
        charamel.Encoding.UTF_32_BE,
        charamel.Encoding.UTF_32_LE,
        charamel.Encoding.UTF_7,
        charamel.Encoding.UTF_8,
    },
    CHARAMEL: set(charamel.Encoding),
}


def format_percent(count: int, total: int) -> str:
    return f'{round(100 * count / total)}%'


def create_encoding_accuracy_breakdown(hits: Dict[str, Dict[str, int]]) -> str:
    headers = ['Encoding', TOTAL, *DETECTORS]
    breakdown = []

    for encoding, statistic in sorted(hits.items()):
        line = [encoding]
        total = statistic[TOTAL]
        line.append(total)
        for detector in DETECTORS:
            count = statistic[detector]
            if encoding not in SUPPORTED_ENCODINGS[detector]:
                asterisk = ASTERISK
            else:
                asterisk = ''

            accuracy = count / total
            if accuracy >= 0.9:
                color = 'green'
            elif accuracy >= 0.8:
                color = 'yellow'
            else:
                color = 'red'
            line.append(
                termcolor.colored(
                    f'{count} ({format_percent(count, total)}){asterisk}', color
                )
            )
        breakdown.append(line)

    return tabulate.tabulate(breakdown, headers, tablefmt='pretty')


def create_detector_metrics(times: Dict[str, List[float]], hits) -> str:
    headers = [
        'Detector',
        'Supported Encodings',
        'Seconds / File (Mean)',
        'Seconds / File (95%)',
        'Accuracy',
        'Accuracy (Supported Encodings)',
    ]
    breakdown = []

    total = sum(statistic[TOTAL] for statistic in hits.values())
    for detector in DETECTORS:
        seconds_per_file_mean = statistics.mean(times[detector])
        seconds_per_file_95 = sorted(times[detector])[int(0.95 * len(times[detector]))]
        correct = sum(statistic[detector] for statistic in hits.values())
        total_supported = sum(
            statistic[TOTAL]
            for encoding, statistic in hits.items()
            if encoding in SUPPORTED_ENCODINGS[detector]
        )
        correct_supported = sum(
            statistic[detector]
            for encoding, statistic in hits.items()
            if encoding in SUPPORTED_ENCODINGS[detector]
        )
        breakdown.append(
            [
                detector,
                len(SUPPORTED_ENCODINGS[detector]),
                round(seconds_per_file_mean, 6),
                round(seconds_per_file_95, 6),
                format_percent(correct, total),
                format_percent(correct_supported, total_supported),
            ]
        )

    return tabulate.tabulate(breakdown, headers, tablefmt='pretty')


def main():
    logging.basicConfig(format='%(message)s', level=logging.INFO, stream=sys.stdout)
    warnings.simplefilter('ignore', UserWarning)

    LOGGER.info(DOUBLE_LINE)
    LOGGER.info(termcolor.colored('Encoding detector benchmark'.center(80), 'blue'))
    LOGGER.info(DOUBLE_LINE)
    fixtures = list(iter_fixtures())

    times = collections.defaultdict(list)
    hits = collections.defaultdict(collections.Counter)
    total = len(fixtures)

    for i, (path, encoding) in enumerate(fixtures, start=1):
        hits[encoding][TOTAL] += 1
        content = path.read_bytes()
        expected = content.decode(encoding)
        for detector, detect in DETECTORS.items():
            start = time.time()
            detected = detect(content)
            end = time.time()
            times[detector].append(end - start)
            hits[encoding][detector] += is_correct_encoding(content, detected, expected)

        LOGGER.info(
            f'{path} {termcolor.colored("[" + format_percent(i, total) + "]", "yellow")}'
        )

    LOGGER.info(DOUBLE_LINE)
    for line in create_detector_metrics(times, hits).splitlines():
        LOGGER.info(line)

    LOGGER.info(DOUBLE_LINE)
    for line in create_encoding_accuracy_breakdown(hits).splitlines():
        LOGGER.info(line)
    LOGGER.info(f'{ASTERISK} - not officially supported for detector')


if __name__ == '__main__':
    main()
