.. image:: https://raw.githubusercontent.com/chomechome/charamel/master/docs/static/logo.png
  :width: 720px

=================================================
🍭 Fast Universal Encoding Detection in Python 🍭
=================================================


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


-------

**Charamel** is a truly universal character encoding library that aims to support `all Python character encodings <https://docs.python.org/3.6/library/codecs.html#standard-encodings>`_.

------------
Installation
------------

::

    $ pip install charamel

-----------
Basic Usage
-----------

.. code-block:: python

    >>> from charamel import Detector, Encoding
    >>> detector = Detector()
    >>> content = b'El espa\xf1ol o castellano del lat\xedn hablado'
    >>> detector.detect(content)
    <Encoding.ISO_8859_14: 'iso8859_14'>
    >>> content.decode(Encoding.ISO_8859_14)
    'El español o castellano del latín hablado'
