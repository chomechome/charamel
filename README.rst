.. image:: https://raw.githubusercontent.com/chomechome/charamel/master/docs/static/logo.png
  :width: 720px

------------

.. image:: https://img.shields.io/pypi/v/charamel.svg
    :target: https://pypi.python.org/pypi/charamel
    :alt: Package version

.. image:: https://img.shields.io/pypi/l/charamel.svg
    :target: https://pypi.python.org/pypi/charamel
    :alt: Package license

.. image:: https://img.shields.io/pypi/pyversions/charamel.svg
    :target: https://pypi.python.org/pypi/charamel
    :alt: Python versions

.. image:: https://travis-ci.org/chomechome/charamel.svg?branch=master
    :target: https://travis-ci.org/chomechome/charamel
    :alt: TravisCI status

.. image:: https://codecov.io/github/chomechome/charamel/coverage.svg?branch=master
    :target: https://codecov.io/github/chomechome/charamel
    :alt: Code coverage

.. image:: https://codeclimate.com/github/chomechome/charamel/badges/gpa.svg?branch=master
    :target: https://codeclimate.com/github/chomechome/charamel
    :alt: Code quality


------------

============================================
Truly Universal Encoding Detection in Python
============================================

**Charamel** is a pure Python universal character encoding library that supports **all** of `Python character encodings <https://docs.python.org/3.6/library/codecs.html#standard-encodings>`_.
The library is based on machine learning and trained to handle more than 60 languages.
All that with no external dependencies. Ain't it sweet? 🍭

------------
Installation
------------

::

    $ pip install charamel

--------
Features
--------

* 🌈 Powered by machine learning
* ✨ No dependencies
* ⚡ Faster than other pure Python libraries
* 🐍 Supports all `98 Python encodings <https://docs.python.org/3.6/library/codecs.html#standard-encodings>`_
* 🌍 Works on 60+ languages

-----
Usage
-----

API is centered around `Detector` class, with `detect` method being responsible for basic encoding detection:

.. code-block:: python

    >>> from charamel import Detector
    >>> detector = Detector()
    >>> content = b'El espa\xf1ol o castellano del lat\xedn hablado'
    >>> detector.detect(content)
    <Encoding.ISO_8859_14: 'iso8859_14'>

This returns the most likely encoding that can decode the byte string. Let's try it out:

.. code-block:: python

    >>> from charamel import Encoding
    >>> content.decode(Encoding.ISO_8859_14)
    'El español o castellano del latín hablado'

To get multiple likely encodings along with confidences in range `[0, 1]`, use `probe` method:

.. code-block:: python

    >>> detector.probe(content, top=3)
    [(<Encoding.ISO_8859_14: 'iso8859_14'>, 0.9964286725192874),
     (<Encoding.CP_1258: 'cp1258'>, 0.9919203166700203),
     (<Encoding.ISO_8859_3: 'iso8859_3'>, 0.9915028923264849)]

`Detector` can be configured to use a subset of encodings. Less possible encodings lead to faster detection:

.. code-block:: python

    >>> detector = Detector(encodings=[Encoding.UTF_8, Encoding.BIG_5])

Another useful `Detector` parameter is `min_confidence`. Basically, this parameter regulates how conservative the `Detector` will be.
Confidence for encodings that are returned by `detect` and `probe` methods must be greater that `min_confidence`:

.. code-block:: python

    >>> detector = Detector(min_confidence=0.5)

If no encoding confidences exceed `min_confidence`, `detect` will return `None` and `probe` will return an empty list.

---------
Benchmark
---------

Below is the comparison between **Charamel** and other available Python encoding detection libraries:

+-----------------------------------------------------------------------------+---------------------+-------------------+------------------+------------------+------------+------------+-------------------------+
| Detector                                                                    | Supported Encodings | Sec / File (Mean) | Sec / File (99%) | Sec / File (Max) |   KB / Sec | Accuracy   | Accuracy on Supported   |
+=============================================================================+=====================+===================+==================+==================+============+============+=========================+
| `Chardet <https://github.com/chardet/chardet>`_ v3.0.4                      |                  26 |          0.027438 |         0.373184 |         3.06614  |        210 | 60%        | 97%                     |
+-----------------------------------------------------------------------------+---------------------+-------------------+------------------+------------------+------------+------------+-------------------------+
| `Cchardet <https://github.com/PyYoshi/cChardet>`_ v2.1.6                    |                  40 |          0.000386 |         0.003917 |         0.062274 |      14964 | 66%        | 78%                     |
+-----------------------------------------------------------------------------+---------------------+-------------------+------------------+------------------+------------+------------+-------------------------+
| `Charset-Normalizer <https://github.com/Ousret/charset_normalizer>`_ v1.3.4 |                  89 |          0.123885 |         0.496293 |         0.70198  |         47 | 77%        | 78%                     |
+-----------------------------------------------------------------------------+---------------------+-------------------+------------------+------------------+------------+------------+-------------------------+
| `Charamel <https://github.com/chomechome/charamel>`_ v0.1.0                 |                  98 |          0.008679 |         0.039195 |         0.121243 |        665 | 97%        | 97%                     |
+-----------------------------------------------------------------------------+---------------------+-------------------+------------------+------------------+------------+------------+-------------------------+

How to run this benchmark (requires Python 3.6+):

::

    $ git clone git@github.com:chomechome/charamel.git
    $ cd charamel
    $ pip install poetry>=1.0.5
    $ make benchmark

It also produces a detailed breakdown of all represented encodings:

.. raw:: html
   :url: https://raw.githubusercontent.com/chomechome/charamel/master/docs/breakdown.html
