Quick Installation of PyMuPDF Binaries Version 1.11.1
======================================================
These installation files support MuPDF version 1.11 published 2017-04-11. They deliver the same functionality as PyMuPDF v1.11.1 - just in a precompiled form.

Pre-requisites
---------------
Windows (x86 or x64) version XP or higher.
Each zip file contains the intended Python version encoded in its name, so -

``pymupdf-1.11.1-pyXY-platform.zip``

means: this is the setup for Python version X.Y on ``platform``, where platform is one of ``x86`` or ``x64``.

Letter d is a technical file identifier.

Python versions prepared include 2.7 and 3.4 through 3.6.

Unfortunately, each binary file ``_fitz.pyd`` "knows" the Python version it must run under. So we need to create a separate one for each Python version we want to cover. If you need support for another Python, just let us know.

Process
--------
Unzip the zip file at a place of your choice. Open a command prompt in the sub directory that containts the ``setup.py`` file and enter

``python setup.py install``

... and you are done.

For Windows, this is the easiest and fastest way to install PyMuPDF: you need nothing else, **no** compiler, **no** Visual Studio, **no** MuPDF, not even PyMuPDF.

The ``setup.py`` script will check whether you are using the correct Python version and bitness.

We have also added an md5-based check to detect download and configuration errors.

Remark
-------
Setup files support the Python launcher introduced with Python 3.3. If you have the launcher, you can therefore always execute ``py setup.py install``, even for Python versions older than 3.3.

If you have several parallel installations you can provide them with their own PyMuPDF version in exactly this way.

Generating your own Binaries
============================
If you want to generate your own ``_fitz.pyd``, follow the instructions on `this <https://github.com/rk700/PyMuPDF/wiki/Windows-Binaries-Generation>`_ Wiki page. It is a description of what has been done to provide this material to you.
