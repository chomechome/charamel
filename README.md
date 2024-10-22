<img alt="logo" src="https://raw.githubusercontent.com/chomechome/charamel/master/docs/static/logo.png"/>

------------

<img alt="Package version" src="https://img.shields.io/pypi/v/charamel.svg"/> <img alt="Package license" src="https://img.shields.io/pypi/l/charamel.svg"/> <img alt="Python versions" src="https://img.shields.io/pypi/pyversions/charamel.svg"/> <img alt="TravisCI status" src="https://travis-ci.org/chomechome/charamel.svg?branch=master"/> <img alt="Code coverage" src="https://codecov.io/github/chomechome/charamel/coverage.svg?branch=master"/> <img alt="Code quality" src="https://codeclimate.com/github/chomechome/charamel/badges/gpa.svg?branch=master"/>

------------

Truly Universal Encoding Detection in Python
============================================

**Charamel** is a pure Python universal character encoding library that supports **all** of [Python character encodings](https://docs.python.org/3.6/library/codecs.html#standard-encodings).
The library is based on machine learning and trained to handle more than 60 languages.
All that with no external dependencies. Ain't it sweet? 🍭

Installation
------------

```shell script
$ pip install charamel
```

Features
--------

* 🌈 Powered by machine learning
* 📦 No dependencies
* ⚡ Faster than other pure Python libraries
* 🐍 Supports all [98 Python encodings](https://docs.python.org/3.6/library/codecs.html#standard-encodings)
* 🌍 Works on 60+ languages
* 🔎 97% accuracy

-----
Usage
-----

API is centered around `Detector` class, with `detect` method being responsible for basic encoding detection:

```python
>>> from charamel import Detector
>>> detector = Detector()
>>> content = b'El espa\xf1ol o castellano del lat\xedn hablado'
>>> detector.detect(content)
<Encoding.ISO_8859_14: 'iso8859_14'>
```

This returns the most likely encoding that can decode the byte string. Let's try it out:

```python
>>> from charamel import Encoding
>>> content.decode(Encoding.ISO_8859_14)
'El español o castellano del latín hablado'
```

To get multiple likely encodings along with confidences in range `[0, 1]`, use `probe` method:

```python
>>> detector.probe(content, top=3)
[(<Encoding.ISO_8859_14: 'iso8859_14'>, 0.9964286725192874),
 (<Encoding.CP_1258: 'cp1258'>, 0.9919203166700203),
 (<Encoding.ISO_8859_3: 'iso8859_3'>, 0.9915028923264849)]
```

`Detector` can be configured to use a subset of encodings. Less possible encodings lead to faster detection:

```python
>>> detector = Detector(encodings=[Encoding.UTF_8, Encoding.BIG_5])
```

Another useful `Detector` parameter is `min_confidence`. Basically, this parameter regulates how conservative the `Detector` will be.
Confidence for encodings that are returned by `detect` and `probe` methods must be greater that `min_confidence`:

```python
>>> detector = Detector(min_confidence=0.5)
```

If no encoding confidences exceed `min_confidence`, `detect` will return `None` and `probe` will return an empty list.

Benchmark
---------

Below is the comparison between **Charamel** and other available Python encoding detection libraries:

| Detector                                                                  |   Supported Encodings |   Sec / File (Mean) |   Sec / File (99%) |   Sec / File (Max) |   KB / Sec | Accuracy   | Accuracy on Supported   |
|---------------------------------------------------------------------------|-----------------------|---------------------|--------------------|--------------------|------------|------------|-------------------------|
| [Chardet](https://github.com/chardet/chardet) v3.0.4                      |                    26 |            0.029259 |           0.416156 |           3.115    |        220 | 61%        | 97%                     |
| [Cchardet](https://github.com/PyYoshi/cChardet) v2.1.6                    |                    40 |            0.000383 |           0.003913 |           0.062855 |      16811 | 67%        | 79%                     |
| [Charset-Normalizer](https://github.com/Ousret/charset_normalizer) v1.3.4 |                    89 |            0.126674 |           0.502882 |           1.41848  |         51 | 77%        | 78%                     |
| [Charamel v1.0.0](https://github.com/chomechome/charamel)                 |                    98 |            0.009053 |           0.04277  |           0.120667 |        712 | 97%        | 97%                     |


How to run this benchmark (requires Python 3.6+):

```shell script
$ git clone git@github.com:chomechome/charamel.git
$ cd charamel
$ pip install poetry>=1.0.5
$ make benchmark
```

It also produces a detailed breakdown for all represented encodings:

 \* - not officially support for detector

| Encoding        |   Total | Chardet v3.0.4   | Cchardet v2.1.6   | Charset-Normalizer v1.3.4   | Charamel v1.0.0   |
|-----------------|---------|------------------|-------------------|-----------------------------|-------------------|
| ascii           |       8 | 7 (88%)          | 8 (100%)          | 7 (88%)                     | 8 (100%)          |
| big5            |      33 | 33 (100%)        | 33 (100%)         | 32 (97%)                    | 31 (94%)          |
| big5hkscs       |       9 | 6 (67%) *        | 6 (67%) *         | 8 (89%)                     | 9 (100%)          |
| cp037           |      14 | 0 (0%) *         | 0 (0%) *          | 12 (86%)                    | 14 (100%)         |
| cp1006          |       4 | 4 (100%) *       | 4 (100%) *        | 4 (100%) *                  | 4 (100%)          |
| cp1026          |      14 | 0 (0%) *         | 0 (0%) *          | 10 (71%)                    | 14 (100%)         |
| cp1125          |       5 | 4 (80%) *        | 4 (80%) *         | 5 (100%)                    | 5 (100%)          |
| cp1140          |      14 | 0 (0%) *         | 0 (0%) *          | 12 (86%)                    | 14 (100%)         |
| cp1250          |      23 | 7 (30%) *        | 22 (96%)          | 11 (48%)                    | 23 (100%)         |
| cp1251          |      45 | 44 (98%)         | 45 (100%)         | 45 (100%)                   | 45 (100%)         |
| cp1252          |      36 | 36 (100%)        | 30 (83%)          | 18 (50%)                    | 36 (100%)         |
| cp1253          |       6 | 4 (67%)          | 6 (100%)          | 6 (100%)                    | 6 (100%)          |
| cp1254          |      16 | 15 (94%) *       | 13 (81%) *        | 12 (75%)                    | 16 (100%)         |
| cp1255          |      29 | 29 (100%)        | 29 (100%)         | 29 (100%)                   | 29 (100%)         |
| cp1256          |       8 | 6 (75%) *        | 7 (88%)           | 8 (100%)                    | 8 (100%)          |
| cp1257          |      13 | 7 (54%) *        | 10 (77%)          | 6 (46%)                     | 13 (100%)         |
| cp1258          |      15 | 14 (93%) *       | 12 (80%) *        | 12 (80%)                    | 15 (100%)         |
| cp273           |      14 | 0 (0%) *         | 0 (0%) *          | 7 (50%)                     | 14 (100%)         |
| cp424           |       4 | 0 (0%) *         | 0 (0%) *          | 4 (100%)                    | 4 (100%)          |
| cp437           |      11 | 4 (36%) *        | 4 (36%) *         | 9 (82%)                     | 11 (100%)         |
| cp500           |      14 | 0 (0%) *         | 0 (0%) *          | 7 (50%)                     | 14 (100%)         |
| cp720           |       6 | 4 (67%) *        | 4 (67%) *         | 6 (100%) *                  | 6 (100%)          |
| cp737           |       4 | 4 (100%) *       | 4 (100%) *        | 4 (100%) *                  | 4 (100%)          |
| cp775           |      11 | 4 (36%) *        | 4 (36%) *         | 8 (73%)                     | 11 (100%)         |
| cp850           |      14 | 4 (29%) *        | 4 (29%) *         | 11 (79%)                    | 14 (100%)         |
| cp852           |      14 | 4 (29%) *        | 12 (86%)          | 6 (43%)                     | 14 (100%)         |
| cp855           |      26 | 26 (100%)        | 26 (100%)         | 26 (100%)                   | 26 (100%)         |
| cp856           |       4 | 4 (100%) *       | 4 (100%) *        | 4 (100%) *                  | 4 (100%)          |
| cp857           |      14 | 4 (29%) *        | 4 (29%) *         | 11 (79%)                    | 14 (100%)         |
| cp858           |      14 | 4 (29%) *        | 4 (29%) *         | 11 (79%)                    | 14 (100%)         |
| cp860           |       7 | 4 (57%) *        | 4 (57%) *         | 6 (86%)                     | 7 (100%)          |
| cp861           |       9 | 4 (44%) *        | 4 (44%) *         | 8 (89%)                     | 9 (100%)          |
| cp862           |       4 | 4 (100%) *       | 4 (100%) *        | 4 (100%)                    | 4 (100%)          |
| cp863           |       7 | 4 (57%) *        | 4 (57%) *         | 6 (86%)                     | 7 (100%)          |
| cp864           |       4 | 4 (100%) *       | 4 (100%) *        | 4 (100%)                    | 4 (100%)          |
| cp865           |      12 | 4 (33%) *        | 4 (33%) *         | 10 (83%)                    | 12 (100%)         |
| cp866           |      23 | 23 (100%)        | 23 (100%)         | 23 (100%)                   | 23 (100%)         |
| cp869           |       4 | 4 (100%) *       | 4 (100%) *        | 4 (100%)                    | 4 (100%)          |
| cp874           |       8 | 6 (75%) *        | 7 (88%) *         | 8 (100%) *                  | 8 (100%)          |
| cp875           |       4 | 0 (0%) *         | 0 (0%) *          | 3 (75%) *                   | 4 (100%)          |
| cp932           |      11 | 11 (100%)        | 8 (73%) *         | 11 (100%)                   | 9 (82%)           |
| cp949           |       6 | 6 (100%) *       | 6 (100%)          | 6 (100%)                    | 6 (100%)          |
| cp950           |       6 | 6 (100%) *       | 6 (100%) *        | 6 (100%)                    | 6 (100%)          |
| euc_jis_2004    |      29 | 8 (28%) *        | 8 (28%) *         | 20 (69%)                    | 29 (100%)         |
| euc_jisx0213    |      29 | 8 (28%) *        | 8 (28%) *         | 20 (69%)                    | 29 (100%)         |
| euc_jp          |      56 | 39 (70%)         | 38 (68%)          | 53 (95%)                    | 56 (100%)         |
| euc_kr          |      38 | 38 (100%)        | 38 (100%)         | 37 (97%)                    | 38 (100%)         |
| gb18030         |      48 | 6 (12%) *        | 47 (98%)          | 33 (69%)                    | 48 (100%)         |
| gb2312          |      26 | 25 (96%)         | 24 (92%) *        | 23 (88%)                    | 26 (100%)         |
| gbk             |      10 | 5 (50%) *        | 9 (90%) *         | 9 (90%)                     | 10 (100%)         |
| hz              |       6 | 6 (100%)         | 6 (100%)          | 5 (83%)                     | 6 (100%)          |
| iso2022_jp      |      10 | 10 (100%)        | 10 (100%)         | 9 (90%)                     | 10 (100%)         |
| iso2022_jp_1    |      26 | 8 (31%) *        | 8 (31%) *         | 25 (96%)                    | 26 (100%)         |
| iso2022_jp_2    |      29 | 8 (28%) *        | 8 (28%) *         | 28 (97%)                    | 29 (100%)         |
| iso2022_jp_2004 |      21 | 8 (38%) *        | 8 (38%) *         | 20 (95%)                    | 21 (100%)         |
| iso2022_jp_3    |      21 | 8 (38%) *        | 8 (38%) *         | 20 (95%)                    | 21 (100%)         |
| iso2022_jp_ext  |      26 | 8 (31%) *        | 8 (31%) *         | 25 (96%)                    | 26 (100%)         |
| iso2022_kr      |       8 | 8 (100%)         | 8 (100%)          | 8 (100%)                    | 8 (100%)          |
| iso8859_10      |      14 | 9 (64%) *        | 13 (93%)          | 7 (50%)                     | 14 (100%)         |
| iso8859_11      |       9 | 6 (67%) *        | 8 (89%) *         | 9 (100%)                    | 8 (89%)           |
| iso8859_13      |      16 | 7 (44%) *        | 14 (88%)          | 6 (38%)                     | 16 (100%)         |
| iso8859_14      |      14 | 14 (100%) *      | 11 (79%) *        | 12 (86%)                    | 14 (100%)         |
| iso8859_15      |      18 | 14 (78%) *       | 14 (78%)          | 12 (67%)                    | 18 (100%)         |
| iso8859_16      |      13 | 8 (62%) *        | 11 (85%)          | 7 (54%)                     | 13 (100%)         |
| iso8859_2       |      28 | 7 (25%) *        | 27 (96%)          | 16 (57%)                    | 28 (100%)         |
| iso8859_3       |      13 | 10 (77%) *       | 10 (77%)          | 9 (69%)                     | 13 (100%)         |
| iso8859_4       |      15 | 9 (60%) *        | 14 (93%)          | 7 (47%)                     | 15 (100%)         |
| iso8859_5       |      39 | 39 (100%)        | 39 (100%)         | 39 (100%)                   | 39 (100%)         |
| iso8859_6       |       6 | 4 (67%) *        | 6 (100%)          | 6 (100%)                    | 6 (100%)          |
| iso8859_7       |      17 | 16 (94%)         | 17 (100%)         | 17 (100%)                   | 17 (100%)         |
| iso8859_8       |       5 | 5 (100%)         | 5 (100%)          | 4 (80%)                     | 5 (100%)          |
| iso8859_9       |      18 | 14 (78%) *       | 15 (83%)          | 13 (72%)                    | 18 (100%)         |
| johab           |       5 | 4 (80%) *        | 4 (80%) *         | 5 (100%)                    | 5 (100%)          |
| koi8_r          |      26 | 26 (100%)        | 26 (100%)         | 26 (100%)                   | 26 (100%)         |
| koi8_t          |       4 | 4 (100%) *       | 4 (100%) *        | 4 (100%) *                  | 4 (100%)          |
| koi8_u          |       5 | 4 (80%) *        | 4 (80%) *         | 4 (80%) *                   | 5 (100%)          |
| kz1048          |       5 | 4 (80%) *        | 4 (80%) *         | 5 (100%)                    | 5 (100%)          |
| latin_1         |      29 | 29 (100%)        | 26 (90%)          | 24 (83%)                    | 29 (100%)         |
| mac_cyrillic    |      25 | 25 (100%)        | 25 (100%)         | 23 (92%)                    | 25 (100%)         |
| mac_greek       |       7 | 4 (57%) *        | 4 (57%) *         | 6 (86%)                     | 7 (100%)          |
| mac_iceland     |      15 | 4 (27%) *        | 4 (27%) *         | 9 (60%)                     | 15 (100%)         |
| mac_latin2      |      16 | 4 (25%) *        | 11 (69%) *        | 6 (38%)                     | 16 (100%)         |
| mac_roman       |      15 | 4 (27%) *        | 4 (27%) *         | 9 (60%)                     | 15 (100%)         |
| mac_turkish     |      15 | 4 (27%) *        | 4 (27%) *         | 9 (60%)                     | 15 (100%)         |
| ptcp154         |       5 | 4 (80%) *        | 4 (80%) *         | 5 (100%)                    | 5 (100%)          |
| shift_jis       |      40 | 40 (100%)        | 40 (100%)         | 38 (95%)                    | 40 (100%)         |
| shift_jis_2004  |      21 | 8 (38%) *        | 8 (38%) *         | 15 (71%)                    | 21 (100%)         |
| shift_jisx0213  |      21 | 8 (38%) *        | 8 (38%) *         | 15 (71%)                    | 21 (100%)         |
| tis_620         |      13 | 12 (92%)         | 12 (92%) *        | 13 (100%)                   | 13 (100%)         |
| utf_16          |      40 | 40 (100%)        | 40 (100%) *       | 33 (82%)                    | 40 (100%)         |
| utf_16_be       |      42 | 0 (0%) *         | 0 (0%)            | 35 (83%)                    | 30 (71%)          |
| utf_16_le       |      43 | 0 (0%) *         | 0 (0%)            | 35 (81%)                    | 37 (86%)          |
| utf_32          |      42 | 42 (100%)        | 42 (100%) *       | 22 (52%)                    | 41 (98%)          |
| utf_32_be       |      41 | 0 (0%) *         | 0 (0%)            | 20 (49%)                    | 27 (66%)          |
| utf_32_le       |      40 | 0 (0%) *         | 0 (0%)            | 20 (50%)                    | 28 (70%)          |
| utf_7           |      40 | 4 (10%) *        | 4 (10%) *         | 20 (50%)                    | 39 (98%)          |
| utf_8           |     101 | 100 (99%)        | 100 (99%)         | 78 (77%)                    | 101 (100%)        |
| utf_8_sig       |      42 | 42 (100%) *      | 42 (100%) *       | 0 (0%) *                    | 42 (100%)         |
