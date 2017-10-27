# PyMuPDF Optional Material Version 1.11.1 Supporting MuPDF Version 1.11

![logo](https://github.com/rk700/PyMuPDF/blob/master/demo/pymupdf.jpg)

This repository contains **Windows-specific** material for [PyMuPDF](https://github.com/rk700/PyMuPDF), the Python bindings for accessing PDF files with MuPDF.

Its purpose is to slim down the PyMuPDF repository to only contain material vital to create PyMuPDF in your Python installation under Windows.

Apart from a compiled HTML documentation file for Windows, this repository offers ways to install PyMuPDF on Windows without having to compile or to download anything else.

Directory ``binary_setups``
----------------------------
Contains zip files for installing PyMuPDF on your Windows system.

In order to reduce space requirements and upload time, we will confine ourselves to a subset of supported Python versions: from 2017-10-18, we will restrict binary's upload to Python versions 2.7 and 3.4 or up. Python 3.4 is the last version that supports Win XP, so we will probably keep this, too.

If you want a version not covered here, please record an issue.

The files follow the naming convention ``pymupdf-1.11.1-pyXY-platform.zip``, where XY stands for the major and minor Python version (i.e. '27' is for any Python 2.7) and ``platform`` is the **bitness** of your Python (**not** the one of your Windows).

Over time, we will be publishing more versions.

All setups with a ``platform`` of 'x86' should work on any Windows version XP SP2 or higher, whether x86 or x64. Please remember, that Python only supports Windows XP with versions up to 3.4.

Setups with a platform of 'x64' do require a Windows x64 version (again, versions XP SP2 or up).

If you do not want to download the complete repository (a 20 MB matter after all), e.g. because you are only interested in one specific version, **click** on the zip file for a specific Python version. Apart from some complaint ("... too big to display ..." etc.) Github should offer you a **Download** button, which you can use to download it (should be considerably below 3 MB).

Or just **click** (not right-click, etc.) on one of the following links.

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

**New:** Support for standard Python Wheels
--------------------------------------------
If you prefer, you now can instead download wheels from the following list, and use `pip install` for installation:

[PyMuPDF-1.11.1-cp27-cp27m-win32.whl](https://github.com/JorjMcKie/PyMuPDF-wheels/blob/master/PyMuPDF-1.11.1-cp27-cp27m-win32.whl)

[PyMuPDF-1.11.1-cp27-cp27m-win_amd64.whl](https://github.com/JorjMcKie/PyMuPDF-wheels/blob/master/PyMuPDF-1.11.1-cp27-cp27m-win_amd64.whl)

[PyMuPDF-1.11.1-cp34-cp34m-win32.whl](https://github.com/JorjMcKie/PyMuPDF-wheels/blob/master/PyMuPDF-1.11.1-cp34-cp34m-win32.whl)

[PyMuPDF-1.11.1-cp34-cp34m-win_amd64.whl](https://github.com/JorjMcKie/PyMuPDF-wheels/blob/master/PyMuPDF-1.11.1-cp34-cp34m-win_amd64.whl)

[PyMuPDF-1.11.1-cp35-cp35m-win32.whl](https://github.com/JorjMcKie/PyMuPDF-wheels/blob/master/PyMuPDF-1.11.1-cp35-cp35m-win32.whl)

[PyMuPDF-1.11.1-cp35-cp35m-win_amd64.whl](https://github.com/JorjMcKie/PyMuPDF-wheels/blob/master/PyMuPDF-1.11.1-cp35-cp35m-win_amd64.whl)

[PyMuPDF-1.11.1-cp36-cp36m-win32.whl](https://github.com/JorjMcKie/PyMuPDF-wheels/blob/master/PyMuPDF-1.11.1-cp36-cp36m-win32.whl)

[PyMuPDF-1.11.1-cp36-cp36m-win_amd64.whl](https://github.com/JorjMcKie/PyMuPDF-wheels/blob/master/PyMuPDF-1.11.1-cp36-cp36m-win_amd64.whl)

Directory ``doc``
------------------
Contains a **CHM based documentation file**. PyMuPDF itself comes with PDF and HTML based help. If you wish to use a compiled HTML (CHM) Windows help, you will find it [here](https://github.com/JorjMcKie/PyMuPDF-optional-material/blob/master/doc/PyMuPDF.chm).

# License
Material in this repository is licensed under the GNU GENERAL PUBLIC LICENSE Version 3 (or later), a copy of which is contained in file ``COPYING GNU GPL V3``.

This is the same license as the one of PyMuPDF.

For the binary file(s), the GNU AFFERO GENERAL PUBLIC LICENSE V3 also applies - just as it would if you generated your own MuPDF binary. A copy of this license is contained in file ``COPYING GNU AFFERO GPL V3``.

Please make sure you are aware of these licenses when using this software.
