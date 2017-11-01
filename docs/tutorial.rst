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
::
 import fitz

You can check your version by printing the docstring:
::
 >>> print (fitz.__doc__)
 PyMuPDF 1.9.1: Python bindings for the MuPDF 1.9a library,
 built on 2016-07-01 13:06:02
 >>>

Opening a Document
======================
To access a supported document, it must be opened with the following statement:
::
 doc = fitz.open(filename)     # or fitz.Document(filename)

This will create ``doc`` as a :ref:`Document` object. ``filename`` must be a Python string or unicode object that specifies the name of an existing file.

It is also possible to open a document from memory data, i.e. without using a file, or create a new, empty PDF. See :ref:`Document` for details.

A document contains many attributes and functions. Among them are meta information (like "author" or "subject"), number of total pages, outline and encryption information.

Some :ref:`Document` Methods and Attributes
=============================================

=========================== ==========================================
**Method / Attribute**      **Description**
=========================== ==========================================
:attr:`Document.pageCount`  number of pages (int).
:attr:`Document.metadata`   metadata (dictionary).
:meth:`Document.getToC`     table of contents (list).
:meth:`Document.loadPage`   create a ``Page`` object.
=========================== ==========================================

Accessing Meta Data
========================
PyMuPDF fully supports standard metadata. :attr:`Document.metadata` is a Python dictionary with the following keys. It is available for all document types, though not all entries may contain data in every single case. For details of their meanings and formats consult the PDF manuals, e.g. :ref:`AdobeManual`. Further information can also be found in chapter :ref:`Document`. The meta data fields are strings (or ``None``) if not otherwise indicated. Be aware that not all of them necessarily contain meaningful data.

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

.. note:: Apart from these standard metadata, PDF documents of PDF version 1.4 or later may also contain so-called *"metadata streams"*. Information in metadata streams is coded in XML. As PyMuPDF deliberately contains no XML components, we do not directly support access to this type of data. It is however possible to extract XML metadata, modify them (e.g. with suitable editors or XML software) and restore results back in the PDF using PyMuPDF.

Working with Outlines
=========================
The easiest way to get all outlines of a document, is creating a table of contents:
::
 toc = doc.getToC()

This will return a Python list of lists ``[[lvl, title, page, ...], ...]``.

``lvl`` is the hierarchy level of the entry (starting from 1), ``title`` is the entry's title, and ``page`` the page number (1-based!). Other parameters describe details of the bookmark target.


Working with Pages
======================
Tasks that can be performed with a :ref:`Page` are at the core of MuPDF's functionality.
Among other things, you can render a page, optionally zooming, rotating, shifting or shearing it.
You can write it's image to files, extract text from it or search for text strings.

At first, a page object must be created:
::
 page = doc.loadPage(n)        # represents page n of the document (0-based)
 page = doc[n]                 # short form

The integer ``n`` above may be any number less than the total number of pages of the document. All negative values are allowed, e.g. ``doc[-1]`` means the last page, as with Python lists. ``doc[-500]`` is **always** valid for any document: to access the respective actual page, the total number of pages is added to -500 until the result is no longer negative.

Some typical uses of :ref:`Page` objects follow:

Inspecting the Links of a Page
------------------------------------
Here is how to get all links and their types:
::
 # get all links of the current page
 links = page.getLinks()

``links`` is a Python list containing Python dictionaries as entries. For details see :meth:`Page.getLinks`.

Rendering a Page
-----------------------
This example creates an image out of a page's content (default parameters shown):
::
 pix = page.getPixmap(matrix = fitz.Identity,
                      colorspace = "rgb",
                      alpha = True)
 
Now ``pix`` contains an RGB image of the page, ready to be used. The above method offers lots of variations for increasing image precision, colorspace selection, transparency exclusion, rotation, mirroring, shifting, shearing, etc.

Saving the Page Image in a File
-----------------------------------
We can simply store the image in a PNG file:
::
 pix.writePNG("test.png")

Displaying the Image in Dialog Managers
-------------------------------------------
We can also use the image in a dialog. :attr:`Pixmap.samples` represents the area of bytes of all the pixels as a Python bytes object. This area is directly usable by presumably most dialog managers. Here are two examples. Please also have a look at the examples directory of this repository.

**wxPython**:
::
 bitmap = wx.BitmapFromBufferRGBA(pix.width, # image width
             pix.height,                     # image height
             pix.samples)                    # bytes with pixel data

**Tkinter**:
::
 # the following requires: "from PIL import Image, ImageTk"
 img = Image.frombytes("RGBA", [pix.width, pix.height], pix.samples)
 photo = ImageTk.PhotoImage(img)

Now, ``photo`` can be used as an image in TK.

Extracting Text
----------------
We can also extract all text of a page in one chunk of string:
::
 text = page.getText("text")

For the parameter, the following values can be specified:

* ``text``: plain text with line breaks (default). No format and no position info.

* ``html``: line breaks, alignment, grouping in HTML syntax. No format and no position info.

* ``json``: full formatting info in JSON format (except colors and fonts) down to spans (see Appendix 2). Use a ``json`` module to interpret.

* ``xml``: full (except colors) formatting info in XML format down to each single character (!). Use an XML module to interpret.

To give you an idea about the output of these alternatives, we did text example extracts. See the Appendix 2.

Searching Text
---------------
You can find out, exactly where on a page a certain string appears like this:

>>> areas = page.searchFor("mupdf", hit_max = 16)

The variable ``areas`` will contain a list of up to 16 :ref:`Rect` rectangles, each of which surrounds one occurrence of string "mupdf" (case insensitive).

Please also do have a look at chapter :ref:`cooperation` and at demo program ``demo.py``. Among other things they contain details on how the :ref:`TextPage`, :ref:`TextSheet`, :ref:`Device` and :ref:`DisplayList` classes can be used for a more direct control, e.g. when performance considerations suggest it.

PDF Maintenance
==================
Since version 1.9, PyMuPDF provides several options to modify PDF documents (only).

The :meth:`Document.save()` method automatically stores a document in its current (potentially modified) state on disk.

Be aware that a PDF document can be modified unnoticed by the user in two ways:

* During open, integrity checks are used to determine the health of the PDF structure. Any errors will automatically be corrected to present a repaired document in memory for further processing. If this is the case, the document is regarded as being modified.

* After a document has been decrypted, the document in memory obviously has changed and also counts as being modified.

In these two cases, the save method will store a repaired and / or decrypted version, and saving **must occur to a new file**.

The following describe some more intentional ways to manipulate PDF documents. Beyond those mentioned here, you can also modify the table of contents and meta information.

Modifying, Creating, Re-arranging and Deleting Pages
-------------------------------------------------------
There are several ways to manipulate the page tree of a PDF:

Methods :meth:`Document.deletePage()` and :meth:`Document.deletePageRange()` delete a page (range) specified by zero-based number(s).

Methods :meth:`Document.copyPage()` and :meth:`Document.movePage()` copy or move a page to another location of the document.

:meth:`Document.insertPage()` inserts a new page, optionally containing some plain text.

Method :meth:`Document.select()` shrinks a document down to selected pages. It accepts a list of integers as argument. These integers must be in range ``0 <= i < pageCount``. When executed, all pages **not occurring** in this list will be deleted. Only pages that do occur will remain - **in the sequence specified and as many times as specified**.

So you can easily create new PDFs with the first or last 10 pages, only the odd or only the even pages (for doing double-sided printing), pages that **do** or **do not** contain a certain text, ... whatever you may think of.

The saved new document will contain all still valid links, annotations and bookmarks.

Pages can moreover be modified by a range of methods (e.g. annotation and link maintenance, text and image insertion).

Joining and Splitting PDF Documents
------------------------------------

Method :meth:`Document.insertPDF()` inserts (pages from) another PDF document at a specified place of the current one. Here is a simple example (``doc1`` and ``doc2`` are openend PDF documents):

>>> # append complete doc2 to the end of doc1
>>> doc1.insertPDF(doc2)

Here is how to split ``doc1``. This creates a new document of its first and last 10 pages:

>>> doc2 = fitz.open()
>>> doc2.insertPDF(doc1, to_page = 9)
>>> doc2.insertPDF(doc1, from_page = len(doc1) - 10)
>>> doc2.save(...)

More can be found in the :ref:`Document` chapter. Also have a look at ``PDFjoiner.py`` in
the repository's *example* directory.

Saving
-------

As mentioned above, ``save()`` will automatically **always** save the document in its current state, decrypted and / or repaired, and including all of your changes. The method's parameters offer you additional ways to (de-) compress or clean content and much more.

Since MuPDF 1.9, you can also write changes back to the original file by specifying ``incremental = True``. This process is (usually) **extremely fast**, since changes are **appended to the original file** - it will not be rewritten as a whole.

:meth:`Document.save` supports all options of MuPDF's command line utility ``mutool clean``, see the following table (corresponding ``mutool clean`` option is indicated as "mco").

=================== ========= ==================================================
**Option**          **mco**   **Effect**
=================== ========= ==================================================
garbage = 1         -g        garbage collect unused objects
garbage = 2         -gg       in addition to 1, compact xref tables
garbage = 3         -ggg      in addition to 2, merge duplicate objects
garbage = 4         -gggg     in addition to 3, check for duplicate streams
clean = 1           -s        clean content streams
deflate = 1         -z        deflate uncompressed streams
ascii = 1           -a        convert data to ASCII format
linear = 1          -l        create a linearized version (do not use yet)
expand = 1          -i        decompress images
expand = 2          -f        decompress fonts
expand = 255        -d        decompress all
incremental = 1     n/a       append changes to the original
=================== ========= ==================================================

Be ready to experiment a little if you want to fully exploit above options: like with ``mutool clean``, not all combinations may always work: there are just too many ill-constructed PDF files out there ...

We have found, that the combination ``mutool clean -gggg -z`` yields excellent compression results and is very stable. In PyMuPDF this corresponds to ``doc.save(filename, garbage=4, deflate=1)``.

Closing
=========
It is often desirable to "close" a document to relinquish control of the underlying file to the OS, while your program is still running.

This can be achieved by the :meth:`Document.close` method. Apart from closing the underlying file, buffer areas associated with the document will be freed (if the document has been created from memory data, only the buffer release will take place).

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

.. rubric:: Footnotes

.. [#f1] (Py-) MuPDF in addition lets you open and handle several image file types like normal documents. See section :ref:`ImageFiles` in chapter :ref:`Pixmap` for more comments.