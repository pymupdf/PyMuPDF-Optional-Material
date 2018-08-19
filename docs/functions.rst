============
Functions
============
The following are miscellaneous functions on a fairly low-level technical detail.

Some functions provide detail access to PDF structures. Others are stripped-down, high performance versions of functions providing more information.

Yet others are handy, general-purpose utilities.


==================================== ==============================================================
**Function**                         **Short Description**
==================================== ==============================================================
:attr:`Document.FontInfos`           PDF only: information on inserted fonts
:meth:`Annot._cleanContents`         PDF only: clean the annot's ``/Contents`` objects
:meth:`Annot._getXref`               PDF only: return xref of annotation
:meth:`ConversionHeader`             return header string for ``getText`` methods
:meth:`ConversionTrailer`            return trailer string for ``getText`` methods
:meth:`Document._delXmlMetadata`     PDF only: remove XML metadata
:meth:`Document._deleteObject`       PDF only: delete an object
:meth:`Document._getGCTXerrmsg`      retrieve C-level exception message
:meth:`Document._getNewXref`         PDF only: create and return a new XREF entry
:meth:`Document._getObjectString`    PDF only: return object definition "source"
:meth:`Document._getOLRootNumber`    PDF only: return / create xref of ``/Outline``
:meth:`Document._getPageObjNumber`   PDF only: return xref and generation number of a page
:meth:`Document._getPageXref`        PDF only: same as ``_getPageObjNumber()``
:meth:`Document._getXmlMetadataXref` PDF only: return XML metadata xref number
:meth:`Document._getXrefLength`      PDF only: return length of xref table
:meth:`Document._getXrefStream`      PDF only: return content of a stream object
:meth:`Document._getXrefString`      PDF only: return object definition "source"
:meth:`Document._updateObject`       PDF only: insert or update a PDF object
:meth:`Document._updateStream`       PDF only: replace the stream of an object
:meth:`Document.extractFont`         PDF only: extract embedded font
:meth:`Document.extractImage`        PDF only: extract embedded image
:meth:`Document.getCharWidths`       PDF only: return a list of glyph widths of a font
:meth:`getPDFnow`                    return the current timestamp in PDF format
:meth:`getPDFstr`                    return PDF-compatible string
:meth:`Page._cleanContents`          PDF only: clean the page's ``/Contents`` objects
:meth:`Page._getContents`            PDF only: return a list of content numbers
:meth:`Page._setContents`            PDF only: set page's /Contents object to specified xref
:meth:`Page._getXref`                PDF only: return xref of page
:meth:`Page.getDisplayList`          create the page's display list
:meth:`Page.insertFont`              PDF only: store a new font in the document
:meth:`Page.getTextBlocks`           extract text blocks as a Python list
:meth:`Page.getTextWords`            extract text words as a Python list
:meth:`Page.run`                     run a page through a device
:meth:`PaperSize`                    return width, height for a known paper format
:meth:`PaperRect`                    return rectangle for a known paper format
:attr:`paperSizes`                   dictionary of pre-defined paper formats
==================================== ==============================================================

   .. method:: PaperSize(s)

      Convenience function to return width and height of a known paper format code. These values are given in pixels for the standard resolution 72 pixels = 1 inch.
      
      Currently defined formats include **'A0'** through **'A10'**, **'B0'** through **'B10'**, **'C0'** through **'C10'**, **'Card-4x6'**, **'Card-5x7'**, **'Commercial'**, **'Executive'**, **'Invoice'**, **'Ledger'**, **'Legal'**, **'Legal-13'**, **'Letter'**, **'Monarch'** and **'Tabloid-Extra'**, each in either portrait or landscape format.

      A format name must be supplied as a string (case **in** \sensitive), optionally suffixed with "-L" (landscape) or "-P" (portrait). No suffix defaults to portrait.

      :arg str s: any format name from above (upper or lower case), like ``"A4"`` or ``"letter-l"``.

      :rtype: tuple
      :returns: ``(width, height)`` of the paper format. For an unknown format ``(-1, -1)`` is returned. Esamples: ``fitz.PaperSize("A4")`` returns ``(595, 842)`` and ``fitz.PaperSize("letter-l")`` delivers ``(792, 612)``.

-----

   .. method:: PaperRect(s)

      Convenience function to return a :ref:`Rect` for a known paper format.

      :arg str s: any format name supported by :meth:`PaperSize`.

      :rtype: :ref:`Rect`
      :returns: ``fitz.Rect(0, 0, width, height)`` with ``width, height = fitz.PaperSize(s)``.

      >>> import fitz
      >>> fitz.PaperRect("letter-l")
      fitz.Rect(0.0, 0.0, 792.0, 612.0)
      >>> 

-----

   .. attribute:: paperSizes
      A dictionary of pre-defines paper formats. Used as basis for :meth:`PaperSize`.

-----

   .. method:: getPDFnow()

      Convenience function to return the current local timestamp in PDF compatible format, e.g. ``D:20170501121525-04'00'`` for local datetime May 1, 2017, 12:15:25 in a timezone 4 hours westward of the UTC meridian.

      :rtype: str
      :returns: current local PDF timestamp.

-----

   .. method:: getPDFstr(obj, brackets = True)

      Make a PDF-compatible string: if ``obj`` contains code points ``ord(c) > 255``, then it will be converted to UTF-16BE as a hexadecimal character string like ``<feff...>``. Otherwise, if ``brackets = True``, it will enclose the argument in ``()`` replacing any characters with code points ``ord(c) > 127`` by their octal number ``\nnn`` prefixed with a backslash. If ``brackets = False``, then the string is returned unchanged.

      :arg obj: the object to convert
      :type obj: str or bytes or unicode

      :rtype: str
      :returns: PDF-compatible string enclosed in either ``()`` or ``<>``.

   .. method:: ConversionHeader(output = "text", filename = "UNKNOWN")

      Return the header string required to make a valid document out of page text outputs.

      :arg str output: type of document. Use the same as the output parameter of ``getText()``.

      :arg str filename: optional arbitrary name to use in output types "json" and "xml".

      :rtype: str


   .. method:: ConversionTrailer(output)

      Return the trailer string required to make a valid document out of page text outputs. See :meth:`Page.getText` for an example.

      :arg str output: type of document. Use the same as the output parameter of ``getText()``.

      :rtype: str

-----

   .. method:: Document._deleteObject(xref)

      PDF only: Delete an object given by its cross reference number.

      :arg int xref: the cross reference number. Must be within the document's valid xref range.

      .. caution:: Only use with extreme care: this may make the PDF unreadable.

-----

   .. method:: Document._delXmlMetadata()

      Delete an object containing XML-based metadata from the PDF. (Py-) MuPDF does not support XML-based metadata. Use this if you want to make sure that the conventional metadata dictionary will be used exclusively. Many thirdparty PDF programs insert their own metadata in XML format and thus may override what you store in the conventional dictionary. This method deletes any such reference, and the corresponding PDF object will be deleted during next garbage collection of the file.

-----

   .. method:: Document._getXmlMetadataXref()

      Return he XML-based metadata object id from the PDF if present - also refer to :meth:`Document._delXmlMetadata`. You can use it to retrieve the content via :meth:`Document._getXrefStream` and then work with it using some XML software.

-----

   .. method:: Document._getPageObjNumber(pno)

      or

   .. method:: Document._getPageXref(pno)

       Return the XREF and generation number for a given page.

      :arg int pno: Page number (zero-based).

      :rtype: list
      :returns: XREF and generation number of page ``pno`` as a list ``[xref, gen]``.

-----

   .. method:: Page._getXref()

      Page version for ``_getPageObjNumber()`` only delivering the XREF (not the generation number).

-----

   .. method:: Page.run(dev, transform)

      Run a page through a device.

      :arg dev: Device, obtained from one of the :ref:`Device` constructors.
      :type dev: :ref:`Device`

      :arg transform: Transformation to apply to the page. Set it to :ref:`Identity` if no transformation is desired.
      :type transform: :ref:`Matrix`

-----

   .. method:: Page.getTextBlocks(images = False)

      Extract all blocks of the page's :ref:`TextPage` as a Python list. Provides basic positioning information but at a much higher speed than :meth:`TextPage.extractDICT`. The block sequence is as specified in the document. All lines of a block are concatenated into one string, separated by ``\n``.

      :arg bool images: also extract image blocks. Default is false. This serves as a means to get complete page layout information. Only image metadata, **not the binary image data** itself is extracted, see below (use the resp. :meth:`Page.getText` versions for accessing full information detail).

      :rtype: *list*
      :returns: a list whose items have the following entries.

                * ``x0, y0, x1, y1``: 4 floats defining the bbox of the block.
                * ``text``: concatenated text lines in the block *(str)*. If this is an image block, a text like this is contained: ``<image: DeviceRGB, width 511, height 379, bpc 8>`` (original image properties).
                * ``block_n``: 0-based block number *(int)*.
                * ``type``: block type *(int)*, 0 = text, 1 = image.

-----

   .. method:: Page.getTextWords()

      Extract all words of the page's :ref:`TextPage` as a Python list. A "word" in this context is any character string surrounded by spaces. Provides positioning information for each word, similar to information contained in :meth:`TextPage.extractDICT` or :meth:`TextPage.extractXML`, but more directly and at a much higher speed. The word sequence is as specified in the document. The accompanying bbox coordinates can be used to re-arrange the final text output to your liking. Block and line numbers help keeping track of the original position.

      :rtype: list
      :returns: a list whose items are lists with the following entries:

                * ``x0, y0, x1, y1``: 4 floats defining the bbox of the word.
                * ``word``: the word, spaces stripped off *(str)*. Note that any non-space character is accepted as part of a word - not only letters. So, ``    Hello   world!   `` will yield the two words ``Hello`` and ``world!``.
                * ``block_n, line_n, word_n``: 0-based counters for block, line and word *(int)*.

-----

   .. method:: Page.insertFont(fontname = "Helvetica", fontfile = None, idx = 0, set_simple = False)

      Store a new font for the page and return its XREF. If the page already references this font, it is a no-operation and just the XREF is returned.

      :arg str fontname: The reference name of the font. If the name does not occur in :meth:`Page.getFontList`, then this must be either the name of one of the :ref:`Base-14-Fonts`, or ``fontfile`` must also be given. Following this method, font name prefixed with a slash "/" can be used to refer to the font in text insertions. If it appears in the list, the method ignores all other parameters and exits with the xref number.

      :arg str fontfile: font file name. This file will be embedded in the PDF.

      :arg int idx: index of the font in the given file. Has no meaning and is ingored if ``fontfile`` is not specified. Default is zero. An invalid index will cause an exception.
      
            .. note::  Certain font files can contain more than one font. This parameter can be used to select the right one. PyMuPDF has no way to tell whether the font file indeed contains a font for any non-zero index.

            .. caution:: Only the first choice of ``idx`` will be honored - subsequent specifications are ignored.

      :arg bool set_simple: When inserting from a font file, a "Type0" font will be installed by default. This option causes the font to be installed as a simple font instead. Only 1-byte characters will then be presented correctly, others will appear as "?" (question mark).

            .. caution:: Only the first choice of ``set_simple`` will be honored. Subsequent specifications are ignored.

      :rtype: int
      :returns: the XREF of the font. PyMuPDF records inserted fonts in two places:
      
            1. An inserted font will appear in :meth:`Page.getFontList()`.
            2. :attr:`Document.FontInfos` records information about all fonts that have been inserted by this method on a document-wide basis.

-----

   .. method:: Page.getDisplayList()

      Run a page through a list device and return its display list.

      :rtype: :ref:`DisplayList`
      :returns: the display list of the page.

-----

   .. method:: Page._getContents()

      Return a list of xref numbers of ``/Contents`` objects belongig to the page. The length of this list will always be at least one (otherwise the PDF is damaged).

      :rtype: list
      :returns: a list of xref integers.

      Each page has one or more associated contents objects (streams) which contain PDF some operator syntax describing what appears where on the page (like text or images, etc. See the :ref:`AdobeManual`, chapter "Operator Summary", page 985). This function only enumerates the number(s) of such objects. To get the actual stream source, use function :meth:`Document._getXrefStream` with one of the numbers in this list. Use :meth:`Document._updateStream` to replace the content [#f1]_ [#f2]_.

-----

   .. method:: Page._setContents(xref)

      PDF only: Set a given object (identified by its xref) as the page's ``/Contents`` object. Useful for joining mutiple ``/Contents`` objects into one as in the following snippet:

      >>> c = b""
      >>> xreflist = page._getContents()
      >>> for xref in xreflist: c += doc._getXrefStream(xref)
      >>> doc._updateStream(xreflist[0], c)
      >>> page._setContents(xreflist[0])
      >>> # doc.save(..., garbage = 4) will remove the unused objects

      :arg int xref: the cross reference number of a ``/Contents`` object. An exception is raised if outside the valid xref range or not a stream object.

-----

   .. method:: Page._cleanContents()

      Clean all ``/Contents`` objects associated with this page (including contents of all annotations on the page). "Cleaning" includes syntactical corrections, standardizations and "pretty printing" of the contents stream. If a page has several contents objects, they will be combined into one. Any discrepancies between ``/Contents`` and ``/Resources`` objects will also be resolved / corrected. Note that the resulting contents stream will be stored **uncompressed** (if you do not specify ``deflate`` on save). See :meth:`Page._getContents` for more details.

      :rtype: int
      :returns: 0 on success.

-----

   .. method:: Annot._getXref()

      Return the xref number of an annotation.

      :rtype: int
      :returns: XREF number of the annotation.

-----

   .. method:: Annot._cleanContents()

      Clean the ``/Contents`` streams associated with the annotation. This is the same type of action :meth:`Page._cleanContents` performs - just restricted to this annotation.

      :rtype: int
      :returns: 0 if successful (exception raised otherwise).

-----

   .. method:: Document.getCharWidths(xref = 0, limit = 256)

      Return a list of character glyphs and their widths for a font that is present in the document. A font must be specified by its PDF cross reference number ``xref``. This function is called automatically from :meth:`Page.insertText` and :meth:`Page.insertTextbox`. So you should rarely need to do this yourself.

      :arg int xref: cross reference number of a font embedded in the PDF. To find a font xref, use e.g. ``doc.getPageFontList(pno)`` of page number ``pno`` and take the first entry of one of the returned list entries.

      :arg int limit: limits the number of returned entries. The default of 256 is enforced for all fonts that only support 1-byte characters, so-called "simple fonts" (checked by this method). All :ref:`Base-14-Fonts` are simple fonts.

      :rtype: list
      :returns: a list of ``limit`` tuples. Each character ``c`` has an entry  ``(g, w)`` in this list with an index of ``ord(c)``. Entry ``g`` (integer) of the tuple is the glyph id of the character, and float ``w`` is its normalized width. The actual width for some fontsize can be calculated as ``w * fontsize``. For simple fonts, the ``g`` entry can always be safely ignored. In all other cases ``g`` is the basis for graphically representing ``c``.

      This function calculates the pixel width of a string called ``text``::

       def pixlen(text, widthlist, fontsize):
       try:
           return sum([widthlist[ord(c)] for c in text]) * fontsize
       except IndexError:
           m = max([ord(c) for c in text])
           raise ValueError:("max. code point found: %i, increase limit" % m)

-----

   .. method:: Document._getObjectString(xref)

   .. method:: Document._getXrefString(xref)

      Return the string ("source code") representing an arbitrary object. For stream objects, only the non-stream part is returned. To get the stream content, use :meth:`_getXrefStream`.

      :arg int xref: XREF number.

      :rtype: string
      :returns: the string defining the object identified by ``xref``.

-----

   .. method:: Document._getGCTXerrmsg()

      Retrieve exception message text issued by PyMuPDF's low-level code. This in most cases, but not always, are MuPDF messages. This string will never be cleared - only overwritten as needed. Only rely on it if a ``RuntimeError`` had been raised.

      :rtype: str
      :returns: last C-level error message on occasion of a ``RuntimeError`` exception.

-----

   .. method:: Document._getNewXref()

      Increase the XREF by one entry and return that number. This can then be used to insert a new object.

      :rtype: int
      :returns: the number of the new XREF entry.

-----

   .. method:: Document._updateObject(xref, obj_str, page = None)

      Associate the object identified by string ``obj_str`` with the XREF number ``xref``, which must already exist. If ``xref`` pointed to an existing object, this will be replaced with the new object. If a page object is specified, links and other annotations of this page will be reloaded after the object has been updated.

      :arg int xref: XREF number.

      :arg str obj_str: a string containing a valid PDF object definition.

      :arg page: a page object. If provided, indicates, that annotations of this page should be refreshed (reloaded) to reflect changes incurred with links and / or annotations.
      :type page: :ref:`Page`

      :rtype: int
      :returns: zero if successful, otherwise an exception will be raised.

-----

   .. method:: Document._getXrefLength()

      Return length of XREF table.

      :rtype: int
      :returns: the number of entries in the XREF table.

-----

   .. method:: Document._getXrefStream(xref)

      Return the decompressed stream of the object referenced by ``xref``. If the object is no stream, ``None`` is returned.

      :arg int xref: XREF number.
      
      :rtype: bytes
      :returns: the (decompressed) stream of the object.

-----

   .. method:: Document._updateStream(xref, stream, new = False)

      Replace the stream of an object identified by ``xref``. If the object has no stream, an exception is raised unless ``new = True`` is used. The function automatically performs a compress operation ("deflate").

      :arg int xref: XREF number.
      
      :arg bytes/bytearray stream: the new content of the stream.
      
      :arg bool new: whether to force accepting the stream, and thus turning ``xref`` into a stream object.

      This method is intended to manipulate streams containing PDF operator syntax (see pp. 985 of the :ref:`AdobeManual`) as it is the case for e.g. page content streams.
      
      If you update a contents stream, you should use save parameter ``clean = True``. This ensures consistency between PDF operator source and the object structure.
      
      Example: Let us assume that you no longer want a certain image appear on a page. This can be achieved by deleting [#f2]_ the respective reference in its contents source(s) - and indeed: the image will be gone after reloading the page. But the page's ``/Resources`` object would still [#f3]_ show the image as being referenced by the page. This save option will clean up any such mismatches.

-----

   .. method:: Document._getOLRootNumber()

       Return XREF number of the /Outlines root object (this is **not** the first outline entry!). If this object does not exist, a new one will be created.

      :rtype: int
      :returns: XREF number of the **/Outlines** root object.

   .. method:: Document.extractImage(xref = 0)

      PDF Only: Extract data and meta information of an image stored in the document. The output can directly be used to be stored as an image file, as input for PIL, :ref:`Pixmap` creation, etc. This method avoids using pixmaps wherever possible to present the image in its original format (e.g. as JPEG).

      :arg int xref: cross reference number of an image object. If the object is not an image or other errors occur, an empty dictionary is returned and no exception is generated. Must however be in range of valid PDF cross reference numbers.

      :rtype: *dict*
      :returns: a dictionary with the following keys
      
        * ``ext`` (*str*) image type (e.g. ``'jpeg'``), usable as image file extension
        * ``smask`` (*int*) xref number of a stencil (/SMask) image or zero
        * ``width`` (*int*) image width
        * ``height`` (*int*) image height
        * ``colorspace`` (*int*) the image's ``pixmap.n`` number (indicative only: depends on whether internal pixmaps had to be used)
        * ``xres`` (*int*) resolution in x direction
        * ``yres`` (*int*) resolution in y direction
        * ``image`` (*bytes*) image data, usable as image file content

      >>> d = doc.extractImage(25)
      >>> d
      {}
      >>> d = doc.extractImage(1373)
      >>> d
      {'ext': 'png', 'smask': 2934, 'width': 5, 'height': 629, 'colorspace': 3, 'xres': 96,
      'yres': 96, 'image': b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x05\ ...'}
      >>> imgout = open("image." + d["ext"], "wb")
      >>> imgout.write(d["image"])
      102
      >>> imgout.close()

      .. note:: There is a functional overlap with ``pix = fitz.Pixmap(doc, xref)``, followed by a ``pix.getPNGData()``. Main differences are that extractImage **(1)** does not only deliver PNG image formats, **(2)** is much faster with JPEG images, **(3)** usually results in much less disk storage for extracted images, **(4)** generates an empty *dict* for non-image xrefs (generates no exception). Look at the following example images within the same PDF.

         * PNG image at xref 1268 -- Comparable execution time and identical output::

            In [23]: %timeit pix = fitz.Pixmap(doc, 1268);pix.getPNGData()
            10.8 ms ± 52.4 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
            In [24]: len(pix.getPNGData())
            Out[24]: 21462
            
            In [25]: %timeit img = doc.extractImage(1268)
            10.8 ms ± 86 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
            In [26]: len(img["image"])
            Out[26]: 21462
         
         * JPEG image at xref 1186 -- :meth:`Document.extractImage` is thousands of times faster and produces a **much smaller** output::

            In [27]: %timeit pix = fitz.Pixmap(doc, 1186);pix.getPNGData()
            341 ms ± 2.86 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
            In [28]: len(pix.getPNGData())
            Out[28]: 2599433
            
            In [29]: %timeit img = doc.extractImage(1186)
            15.7 µs ± 116 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
            In [30]: len(img["image"])
            Out[30]: 371177

   .. method:: Document.extractFont(xref, info_only = False)

      PDF Only: Return an embedded font file's data and appropriate file extension. This can be used to store the font as an external file. The method does not throw exceptions (other than via checking for PDF and valid xref).

      :arg int xref: PDF object number of the font to extract.
      :arg bool info_only: only return font information, not the buffer. To be used for information-only purposes, saves allocation of large buffer areas.

      :rtype: tuple
      :returns: a tuple ``(basename, ext, subtype, buffer)``, where ``ext`` is a 3-byte suggested file extension (*str*), ``basename`` is the font's name (*str*), ``subtype`` is the font's type (e.g. "Type1") and ``buffer`` is a bytes object containing the font file's content (or ``b""``). For possible extension values and their meaning see :ref:`FontExtensions`. Return details on error:

            * ``("", "", "", b"")`` - invalid xref or xref is not a (valid) font object.
            * ``(basename, "n/a", "Type1", b"")`` - ``basename`` is one of the :ref:`Base-14-Fonts`, which cannot be extracted.

      Example:

      >>> # store font as an external file
      >>> name, ext, buffer = doc.extractFont(4711)
      >>> # assuming buffer is not None:
      >>> ofile = open(name + "." + ext, "wb")
      >>> ofile.write(buffer)
      >>> ofile.close()

      .. caution:: The basename is returned unchanged from the PDF. So it may contain characters (such as blanks) which may disqualify it as a valid filename for your operating system. Take appropriate action.

      .. note: The returned ``basename`` in general is **not** the original file name, but probably has some similarity.

   .. attribute:: Document.FontInfos

       Contains following information for any font inserted via :meth:`Page.insertFont`:

       * xref *(int)* - XREF number of the ``/Type/Font`` object.
       * info *(dict)* - detail font information with the following keys:

            * name *(str)* - name of the basefont
            * idx *(int)* - index number for multi-font files
            * type *(str)* - font type (like "TrueType", "Type0", etc.)
            * ext *(str)* - extension to be used, when font is extracted to a file (see :ref:`FontExtensions`).
            * glyphs (*list*) - list of glyph numbers and widths (filled by textinsertion methods).

      :rtype: list

.. rubric:: Footnotes

.. [#f1] If a page has multiple contents streams, they are treated as being one logical stream when the document is processed by reader software. A single operator cannot be split between stream boundaries, but a single **instruction** may well be. E.g. invoking the display of an image looks like this: ``q a b c d e f cm /imageid Do Q``. Any single of these items (PDF notation: "lexical tokens") is always contained in one stream, but ``q a b c d e f cm`` may be in one and ``/imageid Do Q`` in the next one.
.. [#f2] Note that ``/Contents`` objects (similar to /Resources) may be **shared** among pages. A change to a contents stream may therefore affect other pages, too. To avoid this: (1) use :meth:`Page._cleanContents`, (2) read the ``/Contents`` object (there will now be only one left), (3) make your changes.
.. [#f3] Resources objects are inheritable. This means that many pages can share one. Keeping a page's ``/Resources`` object in sync with changes of its ``/Contents`` therefore may require creating an own ``/Resources`` object for the page. This can best be achieved by using ``clean`` when saving, or by invoking :meth:`Page._cleanContents`.
