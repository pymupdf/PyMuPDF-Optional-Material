.. raw:: pdf

    PageBreak

=========
Tutorial
=========
This tutorial will show you the use of PyMuPDF, MuPDF in Python, step by step.

Because MuPDF supports not only PDF, but also XPS, OpenXPS, CBZ, CBR, FB2 and EPUB formats, so does PyMuPDF [#f1]_. Nevertheless we will only talk about PDF files for the sake of brevity. At places where indeed only PDF files are supported, this will be mentioned explicitely.

Importing the Bindings
==========================
The Python bindings to MuPDF are made available by this import statement:

>>> import fitz

You can check your version by printing the docstring:

>>> print (fitz.__doc__)
PyMuPDF 1.9.1: Python bindings for the MuPDF 1.9a library,
built on 2016-07-01 13:06:02

Opening a Document
======================
To access a supported document, it must be opened with the following statement:

>>> doc = fitz.open(filename)     # or fitz.Document(filename)

This creates a :ref:`Document` object ``doc``. ``filename`` must be a Python string specifying the name of an existing file.

It is also possible to open a document from memory data, or to create a new, empty PDF. See :ref:`Document` for details.

A document contains many attributes and functions. Among them are meta information (like "author" or "subject"), number of total pages, outline and encryption information.

Some :ref:`Document` Methods and Attributes
=============================================

=========================== ==========================================
**Method / Attribute**      **Description**
=========================== ==========================================
:attr:`Document.pageCount`  number of pages (*int*)
:attr:`Document.metadata`   metadata (*dict*)
:meth:`Document.getToC`     table of contents (*list*)
:meth:`Document.loadPage`   read a page (:ref:`Page`)
=========================== ==========================================

Accessing Meta Data
========================
PyMuPDF fully supports standard metadata. :attr:`Document.metadata` is a Python dictionary with the following keys. It is available for **all document types**, though not all entries may contain data in every single case. For details of their meanings and formats consult the respective manuals, e.g. :ref:`AdobeManual` for PDF. Further information can also be found in chapter :ref:`Document`. The meta data fields are strings (or ``None``) if not otherwise indicated. Also be aware that not all of them always contain meaningful data.

============== ==============================
**Key**        **Value**
============== ==============================
producer       producer (producing software)
format         PDF format, e.g. 'PDF-1.4'
encryption     encryption method used
author         author
modDate        date of last modification
keywords       keywords
title          title
creationDate   date of creation
creator        creating application
subject        subject
============== ==============================

.. note:: Apart from these standard metadata, **PDF documents** starting from version 1.4 may also contain so-called *"metadata streams"*. Information in such streams is coded in XML. PyMuPDF deliberately contains no XML components, so we do not directly support access to information contained therein. But you can extract the stream as a whole, inspect or modify it using a package like `lxml <https://pypi.org/project/lxml/>`_ and then store the result back into the PDF. If you want, you can also delete these data altogether.

.. note:: There are two utility scripts in the repository that `import <https://github.com/rk700/PyMuPDF/blob/master/examples/csv2meta.py>`_ resp. `export <https://github.com/rk700/PyMuPDF/blob/master/examples/meta2csv.py>`_ metadata from resp. to CSV files.

Working with Outlines
=========================
The easiest way to get all outlines (also called "bookmarks") of a document, is creating a *table of contents*:

>>> toc = doc.getToC()

This will return a Python list of lists ``[[lvl, title, page, ...], ...]``.

``lvl`` is the hierarchy level of the entry (starting from 1), ``title`` is the entry's title, and ``page`` the page number (1-based!). Other parameters describe details of the bookmark target.

.. note:: There are two utility scripts in the repository that `import <https://github.com/rk700/PyMuPDF/blob/master/examples/csv2toc.py>`_ resp. `export <https://github.com/rk700/PyMuPDF/blob/master/examples/toc2csv.py>`_ table of contents from resp. to CSV files.

Working with Pages
======================
:ref:`Page` handling is at the core of MuPDF's functionality.

* You can render a page into a raster or vector image, optionally zooming, rotating, shifting or shearing it.

* You can extract a page's text in several formats and search for strings.

First, a page object must be created. This is a method of :ref:`Document`:

>>> page = doc.loadPage(n)        # represents page n of the document (0-based)
>>> page = doc[n]                 # short form

``n`` may be any positive or negative integer ``< doc.pageCount``. Negative numbers count backwards from the end, so ``doc[-1]`` is the last page, like with Python lists.

Some typical uses of :ref:`Page`\s follow:

Inspecting the Links of a Page
------------------------------------
Links are shown as "hot areas" when a document is displayed with some software. If you click while your cursor shows a hand symbol, you will usually be taken to the taget that is encoded in that link. Here is how to get all links and their types. 

>>> # get all links on a page
>>> links = page.getLinks()

``links`` is a Python list of dictionaries. For details see :meth:`Page.getLinks`.

Rendering a Page
-----------------------
This example creates a **raster** image of a page's content:

>>> pix = page.getPixmap()

``pix`` is a :ref:`Pixmap` object that contains an RGBA image of the page, ready to be used. This method offers lots of variations for controlling the image: resolution, colorspace, transparency, rotation, mirroring, shifting, shearing, etc.

.. note:: You can also create **vector** images of a page using :meth:`Page.getSVGimage`. Refer to this `Wiki <https://github.com/rk700/PyMuPDF/wiki/Vector-Image-Support>`_ for details.

Saving the Page Image in a File
-----------------------------------
We can simply store the image in a PNG file:

>>> pix.writePNG("test.png")

Displaying the Image in Dialog Managers
-------------------------------------------
We can also use it in GUI dialog managers. :attr:`Pixmap.samples` represents an area of bytes of all the pixels as a Python bytes object. Here are some examples, find more `here <https://github.com/rk700/PyMuPDF/tree/master/examples>`_.

wxPython
~~~~~~~~~~~~~

>>> bitmap = wx.BitmapFromBufferRGBA(pix.width, pix.height, pix.samples)

Tkinter
~~~~~~~~~~
Please also see section 3.19 of the `Pillow documentation <https://Pillow.readthedocs.io>`_.

>>> from PIL import Image, ImageTk
>>> img = Image.frombytes("RGBA", [pix.width, pix.height], pix.samples)
>>> tkimg = ImageTk.PhotoImage(img)


PyQt4, PyQt5, PySide
~~~~~~~~~~~~~~~~~~~~~
Please also see section 3.16 of the `Pillow documentation <https://Pillow.readthedocs.io>`_.

>>> from PIL import Image, ImageQt
>>> img = Image.frombytes("RGBA", [pix.width, pix.height], pix.samples)
>>> qtimg = ImageQt.ImageQt(img)

Extracting Text
----------------
We can also extract all text of a page in one chunk of string:

>>> text = page.getText(type)

Use one of the following strings for ``type`` to obtain different formats:

* ``"text"``: (default) plain text with line breaks. No formatting, no text position details.

* ``"html"``: creates a full visual version of the page including any images, which can be displayed in browsers.

* ``"json"``: same information level as HTML. Use a JSON module to interpret.

* ``"xhtml"``: text information level as the TEXT version, but includes images and can also be displayed in browsers.

* ``"xml"``: contains no images, but full position and font information about each single text character. Use an XML module to interpret.

To give you an idea about the output of these alternatives, we did text example extracts. See :ref:`Appendix2`.

Searching for Text
-------------------
You can find out, exactly where on a page a certain string appears:

>>> areas = page.searchFor("mupdf", hit_max = 16)

This delivers a list of up to 16 rectangles (see :ref:`Rect`), each of which surrounds one occurrence of the string "mupdf" (case insensitive). You could use this information to e.g. highlight those areas or create a cross reference of the document.

Please also do have a look at chapter :ref:`cooperation` and at demo programs `demo.py <https://github.com/rk700/PyMuPDF/blob/master/demo/demo.py>`_ and `demoy-lowlevel.py <https://github.com/rk700/PyMuPDF/blob/master/demo/demo-lowlevel.py>`_. Among other things they contain details on how the :ref:`TextPage`, :ref:`Device` and :ref:`DisplayList` classes can be used for a more direct control, e.g. when performance considerations suggest it.

PDF Maintenance
==================
PyMuPDF provides several features to **modify PDF** documents.

:meth:`Document.save()` always stores a PDF in its current (potentially modified) state on disk.

Apart from your changes, there are less obvious ways for a PDF to becoming "modified":

* During open, integrity checks are used to determine the health of the PDF structure. Any errors will be corrected as far as possible to present a repaired document in memory for further processing. If this is the case, the document is regarded as being modified.

* After a document has been decrypted, the document in memory has changed and also counts as being modified.

In these two cases, :meth:`Document.save()` will store a repaired, resp. decrypted version, and saving **must occur to a new file**.

The following describe some more intentional ways to manipulate PDF documents. This description is by no means exhaustive: much more can be found in the following chapters.

Modifying, Creating, Re-arranging and Deleting Pages
-------------------------------------------------------
There are several ways to manipulate the page tree of a PDF:

Methods :meth:`Document.deletePage` and :meth:`Document.deletePageRange` delete pages.

Methods :meth:`Document.copyPage` and :meth:`Document.movePage` copy or move a page to another location within the document.

:meth:`Document.insertPage` and :meth:`Document.newPage` insert pages.

Method :meth:`Document.select` shrinks a PDF down to selected pages. It accepts a sequence of integers as argument. These integers must be in range ``0 <= i < pageCount``. When executed, all pages **missing** in this list will be deleted. Remaining pages will occur **in the sequence specified and as many times (!) as specified**.

So you can easily create new PDFs with the first or last 10 pages, only the odd or only the even pages (for doing double-sided printing), pages that **do** or **don't** contain a certain text, reverse the page sequence, ... whatever you may think of.

The saved new document will contain all still valid links, annotations and bookmarks.

Pages themselves can moreover be modified by a range of methods (e.g. page rotation, annotation and link maintenance, text and image insertion).

Joining and Splitting PDF Documents
------------------------------------

Method :meth:`Document.insertPDF` inserts pages from another PDF at a specified place of the current one. Here is a simple **joiner** example (``doc1`` and ``doc2`` being openend PDFs):

>>> # append complete doc2 to the end of doc1
>>> doc1.insertPDF(doc2)

Here is how to split ``doc1``. This creates a new document of its first and last 10 pages (could also be done using :meth:`Document.select`):

>>> doc2 = fitz.open()                 # new empty PDF
>>> doc2.insertPDF(doc1, to_page = 9)  # first 10 pages
>>> doc2.insertPDF(doc1, from_page = len(doc1) - 10) # last 10 pages
>>> doc2.save(...)

More can be found in the :ref:`Document` chapter. Also have a look at `PDFjoiner.py <https://github.com/rk700/PyMuPDF/blob/master/examples/PDFjoiner.py>`_.

Embedding Data
---------------

PDFs can be used as containers for abitrary data (exeutables, other PDFs, text files, etc.) much like ZIP archives.

PyMuPDF fully supports this feature via :ref:`Document` ``embeddedFile*`` methods and attributes. For some detail read :ref:`Appendix 3`, consult the Wiki on `embedding files <https://github.com/rk700/PyMuPDF/wiki/Dealing-with-Embedded-Files>`_, or the example scripts `embedded-copy.py <https://github.com/rk700/PyMuPDF/blob/master/examples/embedded-copy.py>`_, `embedded-export.py <https://github.com/rk700/PyMuPDF/blob/master/examples/embedded-export.py>`_, `embedded-import.py <https://github.com/rk700/PyMuPDF/blob/master/examples/embedded-import.py>`_, and `embedded-list.py <https://github.com/rk700/PyMuPDF/blob/master/examples/embedded-list.py>`_.


Saving
-------

As mentioned above, :meth:`Document.save` will **always** save the document in its current state.

You can write changes back to the **original PDF** by specifying ``incremental = True``. This process is (usually) **extremely fast**, since changes are **appended to the original file** without completely rewriting it.

:meth:`Document.save` supports all options of MuPDF's command line utility ``mutool clean``, see the following table (corresponding ``mutool clean`` option is indicated as "mco").

=================== ========= ==================================================
**Option**          **mco**   **Effect**
=================== ========= ==================================================
garbage = 1         g         garbage collect unused objects
garbage = 2         gg        in addition to 1, compact xref tables
garbage = 3         ggg       in addition to 2, merge duplicate objects
garbage = 4         gggg      in addition to 3, skip duplicate streams
clean = 1           s         clean content streams
deflate = 1         z         deflate uncompressed streams
ascii = 1           a         convert binary data to ASCII format
linear = 1          l         create a linearized version
expand = 1          i         decompress images
expand = 2          f         decompress fonts
expand = 255        d         decompress all
incremental = 1     n/a       append changes to the original
=================== ========= ==================================================

For example, ``mutool clean -ggggz file.pdf`` yields excellent compression results. It corresponds to ``doc.save(filename, garbage=4, deflate=1)``.

Closing
=========
It is often desirable to "close" a document to relinquish control of the underlying file to the OS, while your program continues.

This can be achieved by the :meth:`Document.close` method. Apart from closing the underlying file, buffer areas associated with the document will be freed.

Example: Dynamically Cleaning up Corrupt PDF Documents
========================================================
This shows a potential use of PyMuPDF with another Python PDF library (`pdfrw <https://pypi.python.org/pypi/pdfrw/0.3>`_).

If a clean, non-corrupt or decompressed PDF is needed, one could dynamically invoke PyMuPDF to recover from problems like so:
::
 import sys
 from pdfrw import PdfReader
 import fitz
 from io import BytesIO

 #---------------------------------------
 # 'tolerant' PDF reader
 #---------------------------------------
 def reader(fname):
     ifile = open(fname, "rb")
     idata = ifile.read()                    # put in memory
     ifile.close()
     ibuffer = BytesIO(idata)                # convert to stream
     try:
         return PdfReader(ibuffer)           # let us try
     except:                                 # problem! heal it with PyMuPDF
         doc = fitz.open("pdf", idata)       # open and save a corrected
         c = doc.write(garbage = 4)          # version in memory
         doc.close()
         doc = idata = None                  # free storage
         ibuffer = BytesIO(c)                # convert to stream
         return PdfReader(ibuffer)           # let pdfrw retry
 #---------------------------------------
 # Main program
 #---------------------------------------
 pdf = reader("pymupdf.pdf")
 print pdf.Info
 # do further processing


With the command line utility ``pdftk`` (`available <https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/>`_ for Windows only) a similar result can be achieved, see `here <http://www.overthere.co.uk/2013/07/22/improving-pypdf2-with-pdftk/>`_. However, you must invoke it as a separate process via ``subprocess.Popen``, using stdin and stdout as communication vehicles.

Further Reading
================
Also have a look at PyMuPDF's `Wiki <https://github.com/rk700/PyMuPDF/wiki>`_ pages. Especially those named in the sidebar under title **"Recipies"** cover over 15 topics written in "How-To" style.

.. rubric:: Footnotes

.. [#f1] PyMuPDF lets you also open several image file types just like normal documents. See section :ref:`ImageFiles` in chapter :ref:`Pixmap` for more comments.