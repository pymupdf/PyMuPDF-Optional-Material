.. _FAQ:

==============================
Collection of Recipes
==============================

A collection of recipes in "How-To" format for using PyMuPDF. We aim to extend this section over time. Where appropriate we will refer to the corresponding `Wiki <https://github.com/rk700/PyMuPDF/wiki>`_ pages, but some duplication may still occur.

----------

Images
-------

----------

How to Increase :index:`Image Resolution <pair: image; resolution>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The image of a document page is represented by a :ref:`Pixmap`, and the simplest way to create a pixmap is via method :meth:`Page.getPixmap`.

This method has many options for influencing the result. The most important among them is the :ref:`Matrix`, which lets you :index:`zoom`, rotate, distort or mirror the outcome.

:meth:`Page.getPixmap` by default will use the :ref:`Identity` matrix, which does nothing.

In the following, we apply a :index:`zoom factor <pair: resolution;zoom>` of 2 to each dimension, which will generate an image with a four times better resolution for us.

>>> zoom_x = 2.0                       # horizontal zoom
>>> zomm_y = 2.0                       # vertical zoom
>>> mat = fitz.Matrix(zoom_x, zomm_y)  # zoom factor 2 in each dimension
>>> pix = page.getPixmap(matrix = mat) # use 'mat' instead of the identity matrix

The resulting pixmap will be 4 times bigger than normal.

----------

How to Create :index:`Partial Pixmaps` (Clips)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You do not always need the full image of a page. This may be the case e.g. when you display the image in a GUI and would like to zoom into a part of the page.

Let's assume your GUI window has room to display a full document page, but you now want to fill this room with the bottom right quarter of your page, thus using a four times better resolution.

.. image:: img-clip.jpg

>>> mat = fitz.Matrix(2, 2)                  # zoom factor 2 in each direction
>>> rect = page.rect                         # page rectangle
>>> mp = rect.tl + (rect.br - rect.tl) * 0.5 # center of rect
>>> clip = fitz.Rect(mp, rect.br)            # clipping area we want
>>> pix = page.getPixmap(matrix = mat, clip = clip)

In the above we construct ``clip`` by specifying two diagonally opposite points: the middle point ``mp`` of the page rectangle, and its bottom right, ``rect.br``.

----------

How to :index:`Suppress <pair: suppress; annotation>` Annotation Images
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Normally, the pixmap of a page also includes the images of any annotations. There currently is now direct way to suppress this.

But it can be achieved using a little circumvention like in `this <https://github.com/JorjMcKie/PyMuPDF-Utilities/blob/master/show-no-annots.py>`_ script.

----------

.. index::
   triple: extract;image;non-PDF
   single: convertToPDF

How to Extract Images: Non-PDF Documents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You have basically two options:

1. Convert your document to a PDF, and then use any of the PDF-only extraction methods. This snippet will convert a document to PDF:

    >>> pdfbytes = doc.convertToPDF()
    >>> pdf = fitz.open("pdf", pdfbytes)
    >>> # now use 'pdf' like any PDF document

2. Use :meth:`Page.getText` with the "dict" parameter. This will extract all text and images shown on the page, formatted as a Python dictionary. Every image will occur in an image block, containing meta information and the binary image data. For details of the dictionary's structure, see :ref:`TextPage`. This creates a list of all images shown on a page:

    >>> d = page.getText("dict")
    >>> blocks = d["blocks"]
    >>> imgblocks = [b for b in blocks if b["type"] == 1]

----------

.. index::
   triple: extract;image;PDF
   single: extractImage

How to Extract Images: PDF Documents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Like any other "object" in a PDF, embedded images are identified by a cross reference number (xref, an integer). If you know this number, you have two ways to access the image's data. The following assumes you have opened a PDF under the name "doc":

1. Create a :ref:`Pixmap` of the image with instruction ``pix = fitz.Pixmap(doc, xref)``. This method is **very** fast (single digit micro-seconds). The pixmap's properties (width, height, ...) will reflect the ones of the image. As usual, you can save it as a PNG via method :meth:`Pixmap.writePNG` (or get the corresponding binary data :meth:`Pixmap.getPNGData`). There is no way to tell which image format the embedded original has.

2. Extract the image with instruction ``img = doc.extractImage(xref)``. This is a dictionary containing the binary image data as ``img["image"]``. A number of meta data are also provided - mostly the same as you would find in the pixmap of the image. The major difference is string ``img["ext"]``, which specifies the image format: apart from "png", strings like "jpeg", "bmp", "tiff", etc. can also occur. Use this string as the file extension if you want to store the image. The execution speed of this method should be compared to the combined speed of the statements ``pix = fitz.Pixmap(doc, xref);pix.getPNGData()``. If the embedded image is in PNG format, the speed of :meth:`Document.extractImage` is about the same (and the binary image data is identical). Otherwise, this method is **thousands of times faster**, and in most cases the **image data is much smaller**, too.

Question remains: **"How do I know those cross reference numbers 'xref' of images?"**.

a. **"Inspect the page objects"** Loop through the document's page number list and execute ``imglist = doc.getPageImageList(pno)`` for each page number "pno". This yields a list of lists. Each item "img" in "imglist" contains the xref of an image shown on that page as ``img[0]``. This xref can then be used with one of the above methods. Use this method for valid (undamaged) documents. Note however, that the same image may be referenced multiple times (by different pages), so you might want to provide a mechanism avoiding multiple extracts.
b. **"No need to know"** Loop through the list of **all xrefs** of the document and perform a :meth:`Document.extractImage` for each one. If the returned dictionary is empty, then continue - this xref is no image. Use this method if the PDF is damaged (unusable pages). Note that a PDF often contains "pseudo-images" ("stencil masks") with the special purpose to specify the transparency of some other image. You may want to provide logic to exclude those from extraction.

For both extraction approaches, there exist ready-to-use general purpose scripts: `extract-imga.py <https://github.com/JorjMcKie/PyMuPDF-Utilities/blob/master/extract-imga.py>`_, and `extract-imgb.py <https://github.com/JorjMcKie/PyMuPDF-Utilities/blob/master/extract-imgb.py>`_.


----------

How to Handle Stencil Masks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Some images in PDFs are accompanied by **stencil masks**. In their simplest form stencil masks represent alpha (transparency) bytes stored as seperate images. In order to reconstruct the original of an image which has a stencil mask, it must be "enriched" with transparency bytes taken from its stencil mask.

Whether an image does have such a stencil mask can be recognized in one of two ways in PyMuPDF:

1. An item of :meth:`Document.getPageImageList` has the general format ``[xref, smask, ...]``, where ``xref`` is the image's cross reference number and ``smask``, if positive, is the cross reference number of a stencil mask.
2. The (dictionary) results of :meth:`Document.extractImage` have a key ``"smask"``, which also contains any stencil mask's cross reference number if positive.

If ``smask == 0`` then the image encountered via xref can be processed as it is.

To recover the original image using PyMuPDF, the procedure depicted as follows must be executed:

.. image:: img-stencil.jpg

>>> pix1 = fitz.Pixmap(doc, xref)    # (1) pixmap of image w/o alpha
>>> pix2 = fitz.Pixmap(doc, smask)   # (2) stencil pixmap
>>> pix = fitz.Pixmap(pix1)          # (3) copy of pix1, empty alpha channel added
>>> pix.setAlpha(pix2.samples)       # (4) fill alpha channel

Step (1) creates a pixmap of the "netto" image. Step (2) does the same with the stencil mask. Please note that the :attr:`Pixmap.samples` attribute of ``pix2`` contains the alpha bytes that must be stored in the final pixmap. This is what happens in step (3) and (4).

The scripts `extract-imga.py <https://github.com/JorjMcKie/PyMuPDF-Utilities/blob/master/extract-imga.py>`_, and `extract-imgb.py <https://github.com/JorjMcKie/PyMuPDF-Utilities/blob/master/extract-imgb.py>`_ above also contain this logic.

----------

.. index::
   triple: picture;embed;PDF
   single: showPDFpage;insertImage;embeddedFileAdd

How to Make a PDF of All your Pictures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
We show two scripts that take a list of image files and put them all in one PDF.

The first one converts each image to a PDF page with the same dimensions::

 import os, fitz
 import PySimpleGUI as psg                    # for showing progress bar
 doc = fitz.open()                            # PDF with the pictures
 imgdir = "D:/2012_10_05"                     # where the pics are
 imglist = os.listdir(imgdir)                 # list of them
 imgcount = len(imglist)                      # pic count
 
 for i, f in enumerate(imglist):
     img = fitz.open(os.path.join(imgdir, f)) # open pic as document
     rect = img[0].rect                       # pic dimension
     pdfbytes = img.convertToPDF()            # make a PDF stream
     img.close()                              # no longer needed
     imgPDF = fitz.open("pdf", pdfbytes)      # open stream as PDF
     page = doc.newPage(width = rect.width,   # new page with ...
                        height = rect.height) # pic dimension
     page.showPDFpage(rect, imgPDF, 0)        # image fills the page
     psg.EasyProgressMeter("Import Images",   # show our progress
         i+1, imgcount)
 
 doc.save("all-my-pics.pdf")

This will generate a PDF marginally larger than the combined pictures's size. Some numbers on performance:

The above script needed about 1 minute on my machine for 149 pictures with a total size of 514 MB (and about the same resulting PDF size).

.. image:: img-import-progress.jpg

An alternative would be using :meth:`Page.insertImage` in the for loop:

>>> ...
>>> for f in imglist:
        pix = fitz.Pixmap(os.path.join(imgdir, f)) # make a pixmap from pic
        rect = pix.irect.rect
        page = doc.newPage(width = rect.width,
                           height = rect.height)
        page.insertImage(rect, pixmap = pix)
>>> ...

This will produce the same type of file, but it stores **images uncompressed**. So the ``deflate = True`` must be used to achieve a reasonable file size, which hugely increases the runtime for large numbers of images. So this alternative **cannot be recommended**.

Another approach is to just embed the images and abdicate displaying them as pages. You would then need a suitable PDF viewer that can display and / or detach embedded files::

 import os, fitz
 import PySimpleGUI as psg                    # for showing progress bar
 doc = fitz.open()                            # PDF with the pictures
 imgdir = "D:/2012_10_05"                     # where the pictures are
 rect = fitz.PaperRect("a4") + (36, 36, -36, -36)  # protocol area in PDF page
 imglist = os.listdir(imgdir)                 # list of pictures
 imgcount = len(imglist)                      # pic count
 imglist.sort()                               # nicely sort them
 # make protocol text
 text = "Contains the following %i files from '%s':\n\n" % (imgcount, imgdir)
 text += ", ".join(imglist)
 for i, f in enumerate(imglist):
     img = open(os.path.join(imgdir,f), "rb").read()    # make pic stream
     doc.embeddedFileAdd(img, f, filename=f,            # and embed it
                         ufilename=f, desc=f)
     psg.EasyProgressMeter("Embedding Files", # show our progress
         i+1, imgcount)
 
 page = doc.newPage()                         # at least 1 page is needed,
 page.insertTextbox(rect, text)               # so put protocol text in it
 doc.save("all-my-pics-embedded.pdf")

.. image:: img-embed-progress.jpg

This is by far the fastest method, and it also produces the smallest possible output file size. The above pictures needed 20 seonds on my machine and yielded a PDF size of 510 MB.

.. note:: This method can also be used to embed **arbitrary files** - not just images.

.. note:: We strongly recommend using the awesome package `PySimpleGUI <https://pypi.org/project/PySimpleGUI/>`_ to display a progress meter for tasks that may run for an extended time, like this one. It's pure Python, uses Tkinter (no additional GUI package) and requires just one more line of code!

----------

.. index::
   triple: vector;image;SVG
   single: showPDFpage
   single: insertImage
   single: embeddedFileAdd

How to Create Vector Images
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The usual way to create an image from a document page is :meth:`Page.getPixmap`. A pixmap represents a raster image, so you must decide on its quality (i.e. resolution) at creation time. It cannot be increased later.

PyMuPDF also offers a way to create a **vector image** of a page in SVG format (scalable vector graphics, defined in XML syntax). SVG images remain precise across zooming levels - of course with the exception of any embedded raster graphic elements.

Instruction ``svg = page.getSVGimage(matrix = fitz.Identity)`` delivers a UTF-8 string ``svg`` which can be stored with extension ".svg".

----------

Text
-----

----------

.. index::
   triple: extract;text;rectangle

How to Extract Text from within a Rectangle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Please refer to this `Wiki page <https://github.com/rk700/PyMuPDF/wiki/How-to-extract-text-from-a-rectangle>`_ of the repository.

----------

.. index::
    pair: text;reading order

How to Extract Text in Natural Reading Order
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One of the common issues with PDF text extraction is, that text may not appear in any particular reading order.

Responsible for this effect is the PDF creator (software or human). For example, page headers may have been inserted in a separate step - after the document had been produced. In such a case, the header text will appear at the end of a page text extraction (allthough it will be correctly shown by PDF viewer software).

PyMuPDF has several means to re-establish some reading sequence or even to re-generate a layout close to the original.

As a starting point take the above mentioned `script <https://github.com/rk700/PyMuPDF/wiki/How-to-extract-text-from-a-rectangle>`_ and then use the full page rectangle.

----------

How to :index:`Extract Tables <pair: extract; table>` from Documents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you see a table in a document, you are not normally looking at something like an embedded Excel or other identifyable object. It usually is just text, formatted to appear as appropriate.

Extracting a tabular data from such a page area therefore means that you must find a way to **(1)** graphically indicate table and column borders, and **(2)** then extract text based on this information.

The wxPython GUI script `wxTableExtract.py <https://github.com/rk700/PyMuPDF/blob/master/examples/wxTableExtract.py>`_ strives to exactly do that. You may want to have a look at it and adjust it to your liking.

----------

General
--------

How to Open with :index:`a Wrong File Extension <pair: wrong; file extension>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you have a document which does not have the right file extension for its type, you can still correctly open it.

Assume that "some.file" is actually an XPS. Open it like so:

>>> doc = fitz.open("some.file", filetype = "xps")

.. note:: MuPDF itself does not try to determine the file type from the file data. You are responsible for supplying it in some way - either implicitely via the file extension, or explicitely as shown. Also consult the :ref:`Document` chapter for a full description.

----------

How to :index:`Embed or Attach Files <triple: attach;embed;file>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
PDF supports incorporating arbitrary data. This can be done in one of two ways: "embedding" or "attaching". PyMuPDF supports both options.

1. Attached Files: data are **attached to a page** by way of a *FileAttachment* annotation with this statement: ``annot = page.addFileAnnot(pos, ...)``, for details see :meth:`Page.addFileAnnot`. The first parameter "pos" is the :ref:`Point`, where a "PushPin" icon should be placed on the page.

2. Embedded Files: data are embedded on the **document level** via method :meth:`Document.embeddedFileAdd`.

The basic differences between these options are **(1)** you need edit permission to embed a file, but only annotation permission to attach, **(2)** like all annotations, attachments are visible on a page, embedded files are not.

There exist several example scripts: `embedded-list.py <https://github.com/rk700/PyMuPDF/blob/master/examples/embedded-list.py>`_, `new-annots.py <https://github.com/rk700/PyMuPDF/blob/master/demo/new-annots.py>`_.

Also look at the sections above and at chapter :ref:`Appendix 3`.

----------

.. index::
   pair: delete;pages
   pair: rearrange;pages

How to Delete and Re-Arrange Pages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
With PyMuPDF you have all options to copy, move, delete or re-arrange the pages of a PDF. Intuitive methods exist that allow you to do this on a page-by-page level, like the :meth:`Document.copyPage` method.

Or you alternatively prepare a complete new page layout in form of a Python sequence, that contains the page numbers you want, in the sequence you want, and as many times as you want each page. The following may illustrate what can be done with :meth:`Document.select`:

``doc.select([1, 1, 1, 5, 4, 9, 9, 9, 0, 2, 2, 2])``

Now let's prepare a PDF for double-sided printing (on a printer not directly supporting this):

The number of pages is given by ``len(doc)`` (equal to ``doc.pageCount``). The following lists represent the even and the odd page numbers, respectively:

>>> p_even = [p in range(len(doc)) if p % 2 == 0]
>>> p_odd  = [p in range(len(doc)) if p % 2 == 1]

This snippet creates the respective sub documents which can then be used to print the document:

>>> doc.select(p_even)    # only the even pages left over
>>> doc.save("even.pdf")  # save the "even" PDF
>>> doc.close()           # recycle the file
>>> doc = fitz.open(doc.name) # re-open
>>> doc.save(p_odd)       # and do the same with the odd pages
>>> doc.save("odd.pdf")

For more information also have a look at this Wiki `article <https://github.com/rk700/PyMuPDF/wiki/Rearranging-Pages-of-a-PDF>`_.

----------

How to Join PDFs 
~~~~~~~~~~~~~~~~~~
It is easy to join PDFs with method :meth:`Document.insertPDF`. Given open PDF documents, you can copy page ranges from one to the other. You can select the point where the copied pages should be placed, you can revert the page sequence and also change page rotation. This Wiki `article <https://github.com/rk700/PyMuPDF/wiki/Inserting-Pages-from-other-PDFs>`_ contains a full description.

The GUI script `PDFjoiner.py <https://github.com/rk700/PyMuPDF/blob/master/examples/PDFjoiner.py>`_ uses this method to join a list of files while also joining the respective table of contents segments. It looks like this:

.. image:: img-pdfjoiner.png 

----------

How to Add Pages
~~~~~~~~~~~~~~~~~~
There two methods for adding new pages to a PDF: :meth:`Document.insertPage` and :meth:`Document.newPage` (and they share a common code base).

**newPage**

:meth:`Document.newPage` returns the created :ref:`Page` object. Here is the constructor showing defaults::

 >>> doc = fitz.open(...)              # some new or existing PDF document
 >>> page = doc.newPage(to = -1,       # insertion point: end of document
                        width = 595,   # page dimension: A4 portrait
                        height = 842)

The above could also have been achieved with the short form ``page = doc.newPage()``. The ``to`` parameter specifies the document's page number (0-based) **in front of which** to insert.

To create a page in *landscape* format, just exchange the width and height values.

Use this to create the page with another pre-defined paper format:

>>> w, h = fitz.PaperSize("letter-l")        # 'Letter' landscape
>>> page = doc.newPage(width = w, height = h)

The convenience function :meth:`PaperSize` knows over 40 industry standard paper formats to choose from. To see them, inspect dictionary :attr:`paperSizes`. Pass the desired dictionary key to :meth:`PaperSize` to retrieve the paper dimensions. Upper and lower case is supported. If you append "-L" to the format name, the landscape version is returned.

**insertPage**

:meth:`Document.insertPage` also inserts a new page and accepts the same parameters ``to``, ``width`` and ``height``. But it lets you also insert arbitrary text into the new page and returns the number of inserted lines::

 >>> doc = fitz.open(...)              # some new or existing PDF document
 >>> n = doc.insertPage(to = -1,       # default insertion point
                        text = None,   # string or sequence of strings
                        fontsize = 11,
                        width = 595,
                        height = 842,
                        fontname = "Helvetica", # default font
                        fontfile = None,        # any font file name
                        color = (0, 0, 0))      # text color (RGB)

The text parameter can be a (sequence of) string (assuming UTF-8 encoding). Insertion will start at :ref:`Point` (50, 72), which is one inch below top of page and 50 points from the left. The number of inserted text lines is returned. See the method definiton for more details.

----------

