Quick Installation of PyMuPDF Binaries Version
======================================================
These installation files support MuPDF versions with the same major and minor version number. They deliver the same functionality as PyMuPDF with the same major, minor and pathch level - just in a precompiled form.

This installation alternative mainly exists for historical reasons: you can now download your appropriate wheel from PyMuPDF's releases directory https://github.com/rk700/PyMuPDF/releases and install it using PIP. Only in case you do not use PIP, these binaries will provide any value to you.

Pre-requisites
---------------
Windows (x86 or x64) version XP or higher.
Each zip file contains the intended Python version encoded in its name, so -

``pymupdf-<version>-pyXY-<platform>.zip``

means: this is the setup version "<version>" for Python version X.Y on "<platform>", where platform is one of ``x86`` or ``x64``.

Python versions prepared include 2.7 and 3.4 through 3.7 (same as the wheels).

Process
--------
Unzip the zip file at a place of your choice. Open a command prompt in the sub directory that containts the ``setup.py`` file and enter

``python setup.py install``

... and you are done.

The ``setup.py`` script will check whether you are using the correct Python version and bitness.

We have also added an md5-based check to detect download and configuration errors.

Remark
-------
Setup files support the Python launcher introduced with Python 3.3. If you have the launcher, you can therefore always execute ``py setup.py install`` -- even for Python versions older than 3.3.

If you have several parallel installations you can provide them with their own PyMuPDF version in exactly this way.

Generating your own Binaries
============================
If you want to generate your own ``_fitz.pyd``, follow the instructions on `this <https://github.com/rk700/PyMuPDF/wiki/Windows-Binaries-Generation>`_ Wiki page. It is a description of what has been done to provide this material to you.
