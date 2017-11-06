# PyMuPDF Optional Material Version 1.11.1 Supporting MuPDF Version 1.11

![logo](https://github.com/rk700/PyMuPDF/blob/master/demo/pymupdf.jpg)

This repository contains **Windows-specific** material for [PyMuPDF](https://github.com/rk700/PyMuPDF), the Python bindings for MuPDF.

Apart from a CHM documentation file, this repository contains binary installation files (in a self-made ZIP format).

## Directory ``binary_setups``
Contains ZIP files for installing PyMuPDF on your Windows system.

PyMuPDF supports all Python versions 2.7 and up. To limit space requirements and network traffic, only a subset is recorded here, however. Please enter an [issue here](https://github.com/rk700/PyMuPDF/issues), to request another version.

The ZIP files follow the naming convention ``pymupdf-1.11.1-pyXY-platform.zip``, where XY stands for the major and minor Python version (i.e. '27' is for any Python 2.7) and ``platform`` is the **bitness** of your Python (**not** the one of your Windows).

All 'x86' setups should work on any Windows version XP SP2 or higher, whether x86 or x64. Please remember, that Python's support for Windows XP ends with version 3.4.

Setups with a platform of 'x64' do require Windows x64.

You are probably interested in only one or two specific versions: **left-click** on the respective ZIP or WHL file. Apart from some complaint ("... too big to display ..." etc.) Github should then offer you a **Download** button.

Link|Description
----|-------------
[pymupdf-1.11.1-py27-x64.zip](https://github.com/JorjMcKie/PyMuPDF-optional-material/blob/master/binary_setups/pymupdf-1.11.1-py27-x64.zip)|Python 2.7 64bit
[pymupdf-1.11.1-py27-x86.zip](https://github.com/JorjMcKie/PyMuPDF-optional-material/blob/master/binary_setups/pymupdf-1.11.1-py27-x86.zip)|Python 2.7 32bit
[pymupdf-1.11.1-py34-x64.zip](https://github.com/JorjMcKie/PyMuPDF-optional-material/blob/master/binary_setups/pymupdf-1.11.1-py34-x64.zip)|Python 3.4 64bit
[pymupdf-1.11.1-py34-x86.zip](https://github.com/JorjMcKie/PyMuPDF-optional-material/blob/master/binary_setups/pymupdf-1.11.1-py34-x86.zip)|Python 3.4 32bit
[pymupdf-1.11.1-py35-x64.zip](https://github.com/JorjMcKie/PyMuPDF-optional-material/blob/master/binary_setups/pymupdf-1.11.1-py35-x64.zip)|Python 3.5 64bit
[pymupdf-1.11.1-py35-x86.zip](https://github.com/JorjMcKie/PyMuPDF-optional-material/blob/master/binary_setups/pymupdf-1.11.1-py35-x86.zip)|Python 3.5 32bit
[pymupdf-1.11.1-py36-x64.zip](https://github.com/JorjMcKie/PyMuPDF-optional-material/blob/master/binary_setups/pymupdf-1.11.1-py36-x64.zip)|Python 3.6 64bit
[pymupdf-1.11.1-py36-x86.zip](https://github.com/JorjMcKie/PyMuPDF-optional-material/blob/master/binary_setups/pymupdf-1.11.1-py36-x86.zip)|Python 3.6 32bit
[pymupdf-1.11.1-py37-x64.zip](https://github.com/JorjMcKie/PyMuPDF-optional-material/blob/master/binary_setups/pymupdf-1.11.1-py37-x64.zip)|Python 3.7 64bit
[pymupdf-1.11.1-py37-x86.zip](https://github.com/JorjMcKie/PyMuPDF-optional-material/blob/master/binary_setups/pymupdf-1.11.1-py37-x86.zip)|Python 3.7 32bit

## **New:** Support for standard Python Wheels
If you prefer, you can download wheels from the following links, and use

`pip install PyMuPDF-<...>.whl --upgrade`

to install:

[PyMuPDF-1.11.1-cp27-cp27m-win32.whl](https://github.com/JorjMcKie/PyMuPDF-wheels/blob/master/PyMuPDF-1.11.1-cp27-cp27m-win32.whl)

[PyMuPDF-1.11.1-cp27-cp27m-win_amd64.whl](https://github.com/JorjMcKie/PyMuPDF-wheels/blob/master/PyMuPDF-1.11.1-cp27-cp27m-win_amd64.whl)

[PyMuPDF-1.11.1-cp34-cp34m-win32.whl](https://github.com/JorjMcKie/PyMuPDF-wheels/blob/master/PyMuPDF-1.11.1-cp34-cp34m-win32.whl)

[PyMuPDF-1.11.1-cp34-cp34m-win_amd64.whl](https://github.com/JorjMcKie/PyMuPDF-wheels/blob/master/PyMuPDF-1.11.1-cp34-cp34m-win_amd64.whl)

[PyMuPDF-1.11.1-cp35-cp35m-win32.whl](https://github.com/JorjMcKie/PyMuPDF-wheels/blob/master/PyMuPDF-1.11.1-cp35-cp35m-win32.whl)

[PyMuPDF-1.11.1-cp35-cp35m-win_amd64.whl](https://github.com/JorjMcKie/PyMuPDF-wheels/blob/master/PyMuPDF-1.11.1-cp35-cp35m-win_amd64.whl)

[PyMuPDF-1.11.1-cp36-cp36m-win32.whl](https://github.com/JorjMcKie/PyMuPDF-wheels/blob/master/PyMuPDF-1.11.1-cp36-cp36m-win32.whl)

[PyMuPDF-1.11.1-cp36-cp36m-win_amd64.whl](https://github.com/JorjMcKie/PyMuPDF-wheels/blob/master/PyMuPDF-1.11.1-cp36-cp36m-win_amd64.whl)

[PyMuPDF-1.11.1-cp37-cp37m-win32.whl](https://github.com/JorjMcKie/PyMuPDF-wheels/blob/master/PyMuPDF-1.11.1-cp37-cp37m-win32.whl)

[PyMuPDF-1.11.1-cp37-cp37m-win_amd64.whl](https://github.com/JorjMcKie/PyMuPDF-wheels/blob/master/PyMuPDF-1.11.1-cp37-cp37m-win_amd64.whl)

## Directory ``doc``
Contains a **CHM based documentation file**. PyMuPDF itself comes with PDF and HTML based help. If you wish to use a compiled HTML Windows help, left-click [here](https://github.com/JorjMcKie/PyMuPDF-optional-material/blob/master/doc/PyMuPDF.chm).

# License
Material in this repository is licensed under the GNU GENERAL PUBLIC LICENSE Version 3 (or later), a copy of which is contained in file ``COPYING GNU GPL V3``.

This is the same license as the one of PyMuPDF.

For the binary files, the GNU AFFERO GENERAL PUBLIC LICENSE V3 for MuPDF also applies - just as it would if you generated your own MuPDF binary. A copy of this license is contained in file ``COPYING GNU AFFERO GPL V3``.

Please make sure you are aware of these licenses when using this software.
