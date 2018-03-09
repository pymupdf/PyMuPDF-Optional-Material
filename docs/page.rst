.. _Page:

================
Page
================

Class representing a document page. A page object is created by :meth:`Document.loadPage` or, equivalently, via indexing the document like ``doc[n]`` - it has no independent constructor.

There is a parent-child relationship between a document and its pages. If the document is closed or deleted, all page objects (and their respective children, too) in existence will become unusable. If a page property or method is being used, an exception is raised saying that the page object is "orphaned".

Several page methods have a :ref:`Document` counterpart for convenience. At the end of this chapter you will find a synopsis.

Methods ``insertText()``, ``insertTextbox()`` and ``draw*()`` are for PDF pages only. They provide "stand-alone" shortcut versions for the same-named methods of the :ref:`Shape` class. For detailed descriptions have a look in that chapter.

* In contrast to :ref:`Shape`, the results of page methods are not interconnected: they do not share properties like colors, line width / dashing, morphing, etc.
* Each page ``draw*()`` method invokes a :meth:`Shape.finish` and then a :meth:`Shape.commit` and consequently accepts the combined arguments of both these methods.
* Text insertion methods (``insertText()`` and ``insertTextbox()``) do not need :meth:`Shape.finish` and therefore only invoke :meth:`Shape.commit`.

================================ =========================================
**Method / Attribute**           **Short Description**
================================ =========================================
:meth:`Page.bound`               rectangle of the page
:meth:`Page.deleteAnnot`         PDF only: delete an annotation
:meth:`Page.deleteLink`          PDF only: delete a link
:meth:`Page.drawBezier`          PDF only: draw a cubic Bézier curve
:meth:`Page.drawCircle`          PDF only: draw a circle
:meth:`Page.drawCurve`           PDF only: draw a special Bézier curve
:meth:`Page.drawLine`            PDF only: draw a line
:meth:`Page.drawOval`            PDF only: draw an oval / ellipse
:meth:`Page.drawPolyline`        PDF only: connect a point sequence
:meth:`Page.drawRect`            PDF only: draw a rectangle
:meth:`Page.drawSector`          PDF only: draw a circular sector
:meth:`Page.drawSquiggle`        PDF only: draw a squiggly line
:meth:`Page.drawZigzag`          PDF only: draw a zig-zagged line
:meth:`Page.getFontList`         PDF only: get list of used fonts
:meth:`Page.getImageList`        PDF only: get list of used images
:meth:`Page.getLinks`            get all links
:meth:`Page.getPixmap`           create a :ref:`Pixmap`
:meth:`Page.getSVGimage`         create a page image in SVG format
:meth:`Page.getText`             extract the page's text
:meth:`Page.getTextBlocks`       extract text blocks as a Python list
:meth:`Page.getTextWords`        extract text words as a Python list
:meth:`Page.insertImage`         PDF only: insert an image
:meth:`Page.insertLink`          PDF only: insert a new link
:meth:`Page.insertText`          PDF only: insert text
:meth:`Page.insertTextbox`       PDF only: insert a text box
:meth:`Page.loadLinks`           return the first link on a page
:meth:`Page.newShape`            PDF only: start a new :ref:`Shape`
:meth:`Page.searchFor`           search for a string
:meth:`Page.setRotation`         PDF only: set page rotation
:meth:`Page.setCropBox`          PDF only: modify the visible page
:meth:`Page.showPDFpage`         PDF only: display PDF page image
:meth:`Page.updateLink`          PDF only: modify a link
:attr:`Page.CropBoxPosition`     displacement of the /CropBox
:attr:`Page.CropBox`             the page's /CropBox
:attr:`Page.MediaBoxSize`        bottom-right point of /MediaBox
:attr:`Page.MediaBox`            the page's /MediaBox
:attr:`Page.firstAnnot`          first :ref:`Annot` on the page
:attr:`Page.firstLink`           first :ref:`Link` on the page
:attr:`Page.number`              page number
:attr:`Page.parent`              owning document object
:attr:`Page.rect`                rectangle (mediabox) of the page
:attr:`Page.rotation`            PDF only: page rotation
================================ =========================================

**Class API**

.. class:: Page

   .. method:: bound()

      Determine the rectangle (before transformation) of the page. Same as property :attr:`Page.rect` below. For PDF documents this **usually** also coincides with objects ``/MediaBox`` and ``/CropBox``, but not always. The best description hence is probably "``/CropBox``, relocated such that top-left coordinates are (0, 0)". Also see attributes :attr:`Page.CropBox` and :attr:`Page.MediaBox`.

      :rtype: :ref:`Rect`

   .. method:: deleteAnnot(annot)

      PDF only: Delete the specified annotation from the page and (for all document types) return the next one.

      :arg annot: the annotation to be deleted.
      :type annot: :ref:`Annot`

      :rtype: :ref:`Annot`
      :returns: the next annotation of the deleted one.

   .. method:: deleteLink(linkdict)

      PDF only: Delete the specified link from the page. The parameter must be a dictionary of format as provided by the ``getLinks()`` method (see below).

      :arg dict linkdict: the link to be deleted.

   .. method:: insertLink(linkdict)

      PDF only: Insert a new link on this page. The parameter must be a dictionary of format as provided by the ``getLinks()`` method (see below).

      :arg dict linkdict: the link to be inserted.

   .. method:: updateLink(linkdict)

      PDF only: Modify the specified link. The parameter must be a dictionary of format as provided by the ``getLinks()`` method (see below).

      :arg dict linkdict: the link to be modified.

   .. method:: getLinks()

      Retrieves **all** links of a page.

      :rtype: list
      :returns: A list of dictionaries. The entries are in the order as specified during PDF generation. For a description of the dictionary entries see below. Always use this method if you intend to make changes to the links of a page.

   .. method:: insertText(point, text = text, fontsize = 11, fontname = "Helvetica", fontfile = None, idx = 0, color = (0, 0, 0), rotate = 0, morph = None, overlay = True)

      PDF only: Insert text.

   .. method:: insertTextbox(rect, buffer, fontsize = 11, fontname = "Helvetica", fontfile = None, idx = 0, color = (0, 0, 0), expandtabs = 8, align = TEXT_ALIGN_LEFT, charwidths = None, rotate = 0, morph = None, overlay = True)

      PDF only: Insert text into the specified rectangle.

   .. method:: drawLine(p1, p2, color = (0, 0, 0), width = 1, dashes = None, roundCap = True, overlay = True, morph = None)

      PDF only: Draw a line from :ref:`Point` objects ``p1`` to ``p2``.

   .. method:: drawZigzag(p1, p2, breadth = 2, color = (0, 0, 0), width = 1, dashes = None, roundCap = True, overlay = True, morph = None)

      PDF only: Draw a zigzag line from :ref:`Point` objects ``p1`` to ``p2``.

   .. method:: drawSquiggle(p1, p2, breadth = 2, color = (0, 0, 0), width = 1, dashes = None, roundCap = True, overlay = True, morph = None)

      PDF only: Draw a squiggly (wavy, undulated) line from :ref:`Point` objects ``p1`` to ``p2``.

   .. method:: drawCircle(center, radius, color = (0, 0, 0), fill = None, width = 1, dashes = None, roundCap = True, overlay = True, morph = None)

      PDF only: Draw a circle around ``center`` with a radius of ``radius``.

   .. method:: drawOval(rect, color = (0, 0, 0), fill = None, width = 1, dashes = None, roundCap = True, overlay = True, morph = None)

      PDF only: Draw an oval (ellipse) within the given rectangle.

   .. method:: drawSector(center, point, angle, color = (0, 0, 0), fill = None, width = 1, dashes = None, roundCap = True, fullSector = True, overlay = True, closePath = False, morph = None)

      PDF only: Draw a circular sector, optionally connecting the arc to the circle's center (like a piece of pie).

   .. method:: drawPolyline(points, color = (0, 0, 0), fill = None, width = 1, dashes = None, roundCap = True, overlay = True, closePath = False, morph = None)

      PDF only: Draw several connected lines defined by a sequence of points.


   .. method:: drawBezier(p1, p2, p3, p4, color = (0, 0, 0), fill = None, width = 1, dashes = None, roundCap = True, overlay = True, closePath = False, morph = None)

      PDF only: Draw a cubic Bézier curve from ``p1`` to ``p4`` with the control points ``p2`` and ``p3``.

   .. method:: drawCurve(p1, p2, p3, color = (0, 0, 0), fill = None, width = 1, dashes = None, roundCap = True, overlay = True, closePath = False, morph = None)

      PDF only: This is a special case of ``drawBezier()``.


   .. method:: drawRect(rect, color = (0, 0, 0), fill = None, width = 1, dashes = None, roundCap = True, overlay = True, morph = None)

      PDF only: Draw a rectangle.

      .. note:: An efficient way to background-color a PDF page with the old Python paper color is ``page.drawRect(page.rect, color = py_color, fill = py_color, overlay = False)``, where ``py_color = getColor("py_color")``.

   .. method:: insertImage(rect, filename = None, pixmap = None, overlay = True)

      PDF only: Fill the given rectangle with an image. Width and height need not have the same proportions as the image: it will be adjusted to fit. The image is either taken from a pixmap or from a file - **exactly one** of these parameters **must** be specified.

      :arg rect: where to put the image on the page. ``rect`` must be finite, not empty and be completely contained in the page's rectangle.
      :type rect: :ref:`Rect`

      :arg str filename: name of an image file (all MuPDF supported formats - see :ref:`Pixmap` chapter).

      :arg pixmap: pixmap containing the image. When inserting the same image multiple times, this should be the preferred option, because the overhead of opening the image and decompressing its content will occur every time with the filename option.
      :type pixmap: :ref:`Pixmap`

      For a description of the other parameters see :ref:`CommonParms`.

      This example puts the same image on every page of a document:

      >>> doc = fitz.open(...)
      >>> rect = fitz.Rect(0, 0, 50, 50)   # put thumbnail in upper left corner
      >>> pix = fitz.Pixmap("some.jpg")    # an image file
      >>> for page in doc:
              page.insertImage(rect, pixmap = pix)
      >>> doc.save(...)

      Notes:
      
      1. If that same image had already been present in the PDF, then only a reference will be inserted. This of course considerably saves disk space and processing time. But to detect this fact, existing PDF images need to be compared with the new one. This is achieved by storing an MD5 code for each image in a table and only compare the new image's code against its entries. Generating this MD5 table, however, is done only when triggered by the first image insertion - which therefore may have an extended response time.

      2. You can use this method to provide a background image for the page, like a copyright, a watermark or a background color. Or you can combine it with ``searchFor()`` to achieve a textmarker effect.

      3. The image may be inserted uncompressed, e.g. if a ``Pixmap`` is used or if the image has an alpha channel. Therefore, consider using ``deflate = True`` when saving the file.

      4. The image content is stored in its original size - which may be much bigger than the size you want to get displayed. Consider decreasing the stored image size by using the pixmap option and then shrinking it or scaling it down (see :ref:`Pixmap` chapter). The file size savings can be very significant.

   .. method:: getText(output = 'text')

      Retrieves the text of a page. Depending on the output parameter, the results of the :ref:`TextPage` extract methods are returned.

      If ``'text'`` is specified, plain text is returned **in the order as specified during PDF creation** (which is not necessarily the normal reading order). This may not always look as expected, consider using (and probably modifying) the example program `PDF2TextJS.py <https://github.com/rk700/PyMuPDF/blob/master/examples/PDF2TextJS.py>`_. It tries to re-arrange text according to the Western reading layout convention "from top-left to bottom-right".

      :arg str output: A string indicating the requested text format, one of ``"text"`` (default), ``"html"``, ``"json"``, ``"xml"`` or ``"xhtml"``.

      :rtype: (unicode) string
      :returns: The page's text as one string.

      .. note:: Use this method to convert the document into a valid HTML version by wrapping it with appropriate header and trailer strings, see the following snippet. Creating XML, XHTML or JSON documents works in exactly the same way. For XML and JSON you may also include an arbitrary filename like so: ``fitz.ConversionHeader("xml", filename = doc.name)``. Also see :ref:`HTMLQuality`.

      >>> doc = fitz.open(...)
      >>> ofile = open(doc.name + ".html", "w")
      >>> ofile.write(fitz.ConversionHeader("html"))
      >>> for page in doc: ofile.write(page.getText("html"))
      >>> ofile.write(fitz.ConversionTrailer("html"))
      >>> ofile.close()

   .. method:: getTextBlocks(images = False)

      Extract all text blocks as a Python list. Provides basic positioning information without the need to interpret the output of :meth:`TextPage.extractJSON` or :meth:`TextPage.extractXML`. The block sequence is as specified in the document. All lines of a block are concatenated into one string, separated by ``\n``.

      :arg bool images: also extract image blocks. Default is false. This serves as a means to get complete page layout information. Only metadata, **not the image data** itself is extracted, see below (use the resp. :meth:`Page.getText` versions for accessing this information detail).

      :rtype: list
      :returns: a list whose items have the following entries.

                * ``x0, y0, x1, y1``: 4 floats defining the bbox of the block.
                * ``text``: concatenated text lines in the block *(str)*. If this is an image block, a text like this is contained: ``<image: DeviceRGB, width 511, height 379, bpc 8>`` (original image properties).
                * ``block_n``: 0-based block number *(int)*.
                * ``type``: block type *(int)*, 0 = text, 1 = image.

   .. method:: getTextWords()

      Extract all words as a Python list. Provides positioning information for each word without having to interpret the output of JSON or XML versions of :meth:`Page.getText`. The word sequence is as specified in the document. The accompanying bbox coordinates can be used to re-arrange the final text output to your liking. Block and line numbers help keeping track of the original position.

      :rtype: list
      :returns: a list whose items are lists with the following entries:

                * ``x0, y0, x1, y1``: 4 floats defining the bbox of the word.
                * ``word``: the word, spaces stripped off *(str)*. Note that any non-space character is accepted as part of a word - not only letters. So, ``Hello world!`` will yield the two words ``Hello`` and ``world!``.
                * ``block_n, line_n, word_n``: 0-based numbers for block, line and word *(int)*.

   .. method:: getFontList()

      PDF only: Return a list of fonts referenced by the page. Same as :meth:`Document.getPageFontList`.

   .. method:: getImageList()

      PDF only: Return a list of images referenced by the page. Same as :meth:`Document.getPageImageList`.

   .. method:: getSVGimage(matrix = fitz.Identity)

      Create an SVG image from the page. Only full page images are currently supported.

     :arg matrix: a :ref:`Matrix`, default is :ref:`Identity`.
     :type matrix: :ref:`Matrix`

     :returns: a UTF-8 encoded string that contains the image. Because SVG has XML syntax it can be saved in a text file with extension ``.svg``.

   .. method:: getPixmap(matrix = fitz.Identity, colorspace = fitz.csRGB, clip = None, alpha = True)

     Create a pixmap from the page. This is probably the most often used method to create pixmaps.

     :arg matrix: a :ref:`Matrix`, default is :ref:`Identity`.
     :type matrix: :ref:`Matrix`

     :arg colorspace: Defines the required colorspace, one of ``GRAY``, ``RGB`` or ``CMYK`` (case insensitive). Or specify a :ref:`Colorspace`, e.g. one of the predefined ones: :data:`csGRAY`, :data:`csRGB` or :data:`csCMYK`.
     :type colorspace: string, :ref:`Colorspace`

     :arg clip: restrict rendering to this area.
     :type clip: :ref:`IRect`

     :arg bool alpha: A bool indicating whether an alpha channel should be included in the pixmap. Choose ``False`` if you do not really need transparency. This will save a lot of memory (25% in case of RGB ... and pixmaps are typically **large**!), and also processing time in most cases. Also note an important difference in how the image will appear:

        * ``True``: pixmap's samples will be pre-cleared with ``0x00``, including the alpha byte. This will result in **transparent** areas where the page is empty.

        .. image:: img-alpha-1.png

        * ``False``: pixmap's samples will be pre-cleared with ``0xff``. This will result in **white** where the page has nothing to show.

        .. image:: img-alpha-0.png

     :rtype: :ref:`Pixmap`
     :returns: Pixmap of the page.

   .. method:: loadLinks()

      Return the first link on a page. Synonym of property ``firstLink``.

      :rtype: :ref:`Link`
      :returns: first link on the page (or ``None``).

   .. method:: setRotation(rot)

      PDF only: Sets the rotation of the page.

      :arg int rot: An integer specifying the required rotation in degrees. Should be an integer multiple of 90.

   .. method:: showPDFpage(rect, docsrc, pno = 0, keep_proportion = True, overlay = True, reuse_xref = 0, clip = None)

      PDF only: Display a page of another PDF as a **vector image** (otherwise similar to :meth:`Page.insertImage`). This is a multi-purpose method, use it to
      
      * create "n-up" versions of existing PDF files, combining several input pages into **one output page** (see example `4-up.py <https://github.com/rk700/PyMuPDF/blob/master/examples/4-up.py>`_),
      * create "posterized" PDF files, i.e. every input page is split up in parts which each create a separate output page (see `posterize.py <https://github.com/rk700/PyMuPDF/blob/master/examples/posterize.py>`_),
      * include PDF-based vector images like company logos, watermarks, etc., see `svg-logo.py <https://github.com/rk700/PyMuPDF/blob/master/examples/svg-logo.py>`_, which puts an SVG-based logo on each page (requires additional packages to deal with SVG-to-PDF conversions).

      :arg rect: where to place the image.
      :type rect: :ref:`Rect`

      :arg docsrc: source PDF document containing the page. Must be a different document object, but may be the same file.
      :type docsrc: :ref:`Document`

      :arg int pno: page number (0-based) to be shown.

      :arg bool keep_proportion: whether to maintain the width-height-ratio (default).

      :arg bool overlay: put image in foreground (default) or background.

      :arg int reuse_xref: if a source page should be shown multiple times, specify the returned xref number of the first display. This prevents duplicate source page copies, and thus improves performance and saves memory. Note that source document and page must still be provided!

      :arg clip: choose which part of the source page to show. Default is its ``/CropBox``.
      :type clip: :ref:`Rect`

      :returns: xref number of the stored page image if successful. Use this as the value of argument ``reuse_xref`` to show the same source page again.

      .. note:: The displayed source page is shown without any annotations or links.

      .. note:: Use the ``reuse_xref`` argument to prevent duplicates as follows. For a technical description of how this function is implemented, see :ref:`FormXObject`. The following example will put the same source page (probably a company logo or watermark) on every page of PDF ``doc``. The first execution actually inserts the source page, the subsequent ones will only insert pointers to it via its xref number.

      >>> # the first showPDFpage will include source page docsrc[pno],
      >>> # subsequents will reuse it via its xref.
      >>> xref = 0
      >>> for page in doc:
              xref = page.showPDFpage(rect, docsrc, pno,
                                      reuse_xref = xref)

   .. method:: newShape()

      PDF only: Create a new :ref:`Shape` object for the page.

      :rtype: :ref:`Shape`
      :returns: a new :ref:`Shape` to use for compound drawings. See description there.

   .. method:: searchFor(text, hit_max = 16)

      Searches for ``text`` on a page. Identical to :meth:`TextPage.search`.

      :arg str text: Text to searched for. Upper / lower case is ignored.

      :arg int hit_max: Maximum number of occurrences accepted.

      :rtype: list

      :returns: A list of :ref:`Rect` rectangles each of which surrounds one occurrence of ``text``.

   .. method:: setCropBox(r)

      PDF only: change the visible part of the page.

      :arg r: the new visible area of the page.
      :type r: :ref:`Rect`

      After execution, :attr:`Page.rect` will equal this rectangle shifted to the top-left position (0, 0). Example session:

      >>> page = doc.newPage()
      >>> page.rect
      fitz.Rect(0.0, 0.0, 595.0, 842.0)
      >>> page.CropBox
      fitz.Rect(0.0, 0.0, 595.0, 842.0)
      >>> page.setCropBox(fitz.Rect(100, 100, 400, 400))
      >>> page.rect
      fitz.Rect(0.0, 0.0, 300.0, 300.0)
      >>> page.CropBox
      fitz.Rect(100.0, 100.0, 400.0, 400.0)
      >>> page.MediaBox
      fitz.Rect(0.0, 0.0, 595.0, 842.0)
      >>> page.setCropBox(page.MediaBox)
      >>> page.rect
      fitz.Rect(0.0, 0.0, 595.0, 842.0)

   .. attribute:: rotation

      PDF only: contains the rotation of the page in degrees and ``-1`` for other document types.

      :type: int

   .. attribute:: CropBoxPosition

      Contains the displacement of the page's ``/CropBox`` for a PDF, otherwise the top-left coordinates of :attr:`Page.rect`.

      :type: :ref:`Point`

   .. attribute:: CropBox

      The page's ``/CropBox`` for a PDF, else :attr:`Page.rect`.

      :type: :ref:`Rect`

   .. attribute:: MediaBoxSize

      Contains the width and height of the page's ``/MediaBox`` for a PDF, otherwise the bottom-right coordinates of :attr:`Page.rect`.

      :type: :ref:`Point`

   .. attribute:: MediaBox

      The page's ``/MediaBox`` for a PDF, otherwise :attr:`Page.rect`.

      :type: :ref:`Rect`

    .. note:: For non-PDF documents (and for most PDF documents, too) you have ``page.rect == page.CropBox == page.MediaBox``. For some PDF documents however, the visible page may be a true subset of the ``/MediaBox``. In these cases the above attributes help to correctly position / evaluate page elements.

   .. attribute:: firstLink

      Contains the first :ref:`Link` of a page (or ``None``).

      :type: :ref:`Link`

   .. attribute:: firstAnnot

      Contains the first :ref:`Annot` of a page (or ``None``).

      :type: :ref:`Annot`

   .. attribute:: number

      The page number.

      :type: int

   .. attribute:: parent

      The owning document object.

      :type: :ref:`Document`


   .. attribute:: rect

      Contains the rectangle of the page. Same as result of :meth:`Page.bound()`.

      :type: :ref:`Rect`

-----

Description of ``getLinks()`` Entries
----------------------------------------
Each entry of the ``getLinks()`` list is a dictionay with the following keys:

* ``kind``:  (required) an integer indicating the kind of link. This is one of ``LINK_NONE``, ``LINK_GOTO``, ``LINK_GOTOR``, ``LINK_LAUNCH``, or ``LINK_URI``. For values and meaning of these names refer to :ref:`linkDest Kinds`.

* ``from``:  (required) a :ref:`Rect` describing the "hot spot" location on the page's visible representation (where the cursor changes to a hand image, usually).

* ``page``:  a 0-based integer indicating the destination page. Required for ``LINK_GOTO`` and ``LINK_GOTOR``, else ignored.

* ``to``:   either a ``fitz.Point``, specifying the destination location on the provided page, default is ``fitz.Point(0, 0)``, or a symbolic (indirect) name. If an indirect name is specified, ``page = -1`` is required and the name must be defined in the PDF in order for this to work. Required for ``LINK_GOTO`` and ``LINK_GOTOR``, else ignored.

* ``file``: a string specifying the destination file. Required for ``LINK_GOTOR`` and ``LINK_LAUNCH``, else ignored.

* ``uri``:  a string specifying the destination internet resource. Required for ``LINK_URI``, else ignored.

* ``xref``: an integer specifying the PDF cross reference entry of the link object. Do not change this entry in any way. Required for link deletion and update, otherwise ignored. For non-PDF documents, this entry contains ``-1``. It is also ``-1`` for **all** entries in the ``getLinks()`` list, if **any** of the links is not supported by MuPDF - see the note below.

Notes on Supporting Links
---------------------------
MuPDF's support for links has changed in **v1.10a**. These changes affect link types :data:`LINK_GOTO` and :data:`LINK_GOTOR`.

Reading (pertains to method ``getLinks()`` and the ``firstLink`` property chain)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If MuPDF detects a link to another file, it will supply either a ``LINK_GOTOR`` or a ``LINK_LAUNCH`` link kind. In case of ``LINK_GOTOR`` destination details may either be given as page number (eventually including position information), or as an indirect destination.

If an indirect destination is given, then this is indicated by ``page = -1``, and ``link.dest.dest`` will contain this name. The dictionaries in the ``getLinks()`` list will contain this information as the ``to`` value.

**Internal links are always** of kind ``LINK_GOTO``. If an internal link specifies an indirect destination, it **will always be resolved** and the resulting direct destination will be returned. Names are **never returned for internal links**, and undefined destinations will cause the link to be ignored.

Writing
~~~~~~~~~

PyMuPDF writes (updates, inserts) links by constructing and writing the appropriate PDF object **source**. This makes it possible to specify indirect destinations for ``LINK_GOTOR`` **and** ``LINK_GOTO`` link kinds (pre ``PDF 1.2`` file formats are **not supported**).

.. caution:: If a ``LINK_GOTO`` indirect destination specifies an undefined name, this link can later on not be found / read again with MuPDF / PyMuPDF. Other readers however **will** detect it, but flag it as erroneous.

Indirect ``LINK_GOTOR`` destinations can in general of course not be checked for validity and are therefore **always accepted**.

Homologous Methods of :ref:`Document` and :ref:`Page`
--------------------------------------------------------
This is an overview of homologous methods on the :ref:`Document` and on the :ref:`Page` level.

================================== =====================================
**Document Level**                 **Page Level**
================================== =====================================
Document.getPageFontlist(pno)      Page.getFontlist()
Document.getPageImageList(pno)     Page.getImageList()
Document.getPagePixmap(pno, ...)   Page.getPixmap(...)
Document.getPageText(pno, ...)     Page.getText(...)
Document.searchPageFor(pno, ...)   Page.searchFor(...)
Document._getPageXref(pno)         Page._getXref()
================================== =====================================

The page number ``pno`` is 0-based and can be any negative or positive number ``< len(doc)``. The document methods (left column) usually invoke their page counterparts via ``Document[pno].<method>``.