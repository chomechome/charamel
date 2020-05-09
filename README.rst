
 ██████╗██╗  ██╗ █████╗ ██████╗  █████╗ ███╗   ███╗███████╗██╗
██╔════╝██║  ██║██╔══██╗██╔══██╗██╔══██╗████╗ ████║██╔════╝██║
██║     ███████║███████║██████╔╝███████║██╔████╔██║█████╗  ██║
██║     ██╔══██║██╔══██║██╔══██╗██╔══██║██║╚██╔╝██║██╔══╝  ██║
╚██████╗██║  ██║██║  ██║██║  ██║██║  ██║██║ ╚═╝ ██║███████╗███████╗
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝



========================================================
Charamel: Fast Universal Encoding Detection in Python 🍭
========================================================


.. image:: https://img.shields.io/pypi/v/charamel.svg
    :target: https://pypi.python.org/pypi/charamel
    :alt: Package version

.. image:: https://img.shields.io/pypi/l/charamel.svg
    :target: https://pypi.python.org/pypi/charamel
    :alt: Package license

.. image:: https://img.shields.io/pypi/pyversions/charamel.svg
    :target: https://pypi.python.org/pypi/charamel
    :alt: Python versions

.. image:: https://travis-ci.org/chomechome/pychardet.svg?branch=master
    :target: https://travis-ci.org/chomechome/pychardet
    :alt: TravisCI status

---------------

Usage:
    >>> import charamel
    >>> content = b'El espa\xf1ol o castellano del lat\xedn hablado'
    >>> detector = charamel.Detector()
    >>> encoding = detector.detect(content)
    >>> encoding
    <Encoding.ISO_8859_14: 'iso8859_14'>
    >>> content.decode(encoding)
    'El español o castellano del latín hablado'
