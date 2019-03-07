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
:meth:`Annot._cleanContents`         PDF only: clean the annot's :data:`contents` objects
:meth:`ConversionHeader`             return header string for ``getText`` methods
:meth:`ConversionTrailer`            return trailer string for ``getText`` methods
:meth:`Document._delXmlMetadata`     PDF only: remove XML metadata
:meth:`Document._deleteObject`       PDF only: delete an object
:meth:`Document._getGCTXerrmsg`      retrieve C-level exception message
:meth:`Document._getNewXref`         PDF only: create and return a new :data:`xref` entry
:meth:`Document._getOLRootNumber`    PDF only: return / create :data:`xref` of ``/Outline``
:meth:`Document._getPageObjNumber`   PDF only: return :data:`xref` and generation number of a page
:meth:`Document._getPageXref`        PDF only: same as ``_getPageObjNumber()``
:meth:`Document._getTrailerString`   PDF only: return the PDF file trailer
:meth:`Document._getXmlMetadataXref` PDF only: return XML metadata :data:`xref` number
:meth:`Document._getXrefLength`      PDF only: return length of :data:`xref` table
:meth:`Document._getXrefStream`      PDF only: return content of a stream object
:meth:`Document._getXrefString`      PDF only: return object definition "source"
:meth:`Document._updateObject`       PDF only: insert or update a PDF object
:meth:`Document._updateStream`       PDF only: replace the stream of an object
:meth:`Document.extractFont`         PDF only: extract embedded font
:meth:`Document.extractImage`        PDF only: extract embedded image
:meth:`Document.getCharWidths`       PDF only: return a list of glyph widths of a font
:meth:`getPDFnow`                    return the current timestamp in PDF format
:meth:`getPDFstr`                    return PDF-compatible string
:meth:`getTextlength`                return string length for a given font & fontsize
:meth:`Page._cleanContents`          PDF only: clean the page's :data:`contents` objects
:meth:`Page._getContents`            PDF only: return a list of content numbers
:meth:`Page._setContents`            PDF only: set page's :data:`contents` object to specified :data:`xref`
:meth:`Page.getDisplayList`          create the page's display list
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

   .. method:: getTextlength(text, fontname="helv", fontsize=11, encoding=TEXT_ENCODING_LATIN)

      Calculate the length of text on output with a given **builtin** font, fontsize and encoding.

      :arg str text: the text string.
      :arg str fontname: the fontname. Must be one of either the :ref:`Base-14-Fonts` or the CJK fonts, identified by their four-character "reserved" fontnames.
      :arg float fontsize: size of the font.
      :arg int encoding: the encoding to use. Besides 0 = Latin, 1 = Greek and 2 = Cyrillic (Russian) are available. Relevant for Base-14 fonts "Helvetica", "Courier" and "Times" and their variants only. Make sure to use the same value as in the corresponding text insertion.
      :rtype: float
      :returns: the length in points the string will have (e.g. when used in :meth:`Page.insertText`).

      .. note:: This function will only do the calculation -- neither does it insert the font nor write the text.

      .. caution:: If you use this function to determine the required rectangle width for the (:ref:`Page` or :ref:`Shape`) ``insertTextbox`` methods, be aware that they calculate on a **by-character level**. Because of rounding effects, this will mostly lead to a slightly larger number: ``sum([fitz.getTextlength(c) for c in text]) > fitz.getTextlength(text)``. So either (1) do the same, or (2) use something like ``fitz.getTextlength(text + "'")`` for your calculation.

-----

   .. method:: getPDFstr(text)

      Make a PDF-compatible string: if the text contains code points ``ord(c) > 255``, then it will be converted to UTF-16BE with BOM as a hexadecimal character string enclosed in "<>" brackets like ``<feff...>``. Otherwise, it will return the string enclosed in (round) brackets, replacing any characters outside the ASCII range with some special code. Also, every "(", ")" or backslash is escaped with an additional backslash.

      :arg str text: the object to convert

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

      :arg int xref: the cross reference number. Must be within the document's valid :data:`xref` range.

      .. caution:: Only use with extreme care: this may make the PDF unreadable.

-----

   .. method:: Document._delXmlMetadata()

      Delete an object containing XML-based metadata from the PDF. (Py-) MuPDF does not support XML-based metadata. Use this if you want to make sure that the conventional metadata dictionary will be used exclusively. Many thirdparty PDF programs insert their own metadata in XML format and thus may override what you store in the conventional dictionary. This method deletes any such reference, and the corresponding PDF object will be deleted during next garbage collection of the file.

-----

   .. method:: Document._getTrailerString()

      Return the trailer of the PDF (UTF-8), which is usually located at the PDF file's end. If not a PDF or the PDF has no trailer (because of irrecoverable errors), ``None`` is returned.

      :returns: a string with the PDF trailer information. This is the analogous method to :meth:`Document._getXrefString` except that the trailer has no identifying :data:`xref` number. As can be seen here, the trailer object points to other important objects:

      >>> doc=fitz.open("adobe.pdf")
      >>> print(doc._getTrailerString())
      '<</Size 334093/Prev 25807185/XRefStm 186352/Root 333277 0 R/Info 109959 0 R
      /ID[(\\227\\366/gx\\016ds\\244\\207\\326\\261\\\\\\305\\376u)
      (H\\323\\177\\346\\371pkF\\243\\262\\375\\346\\325\\002)]>>'

      .. note:: MuPDF is capable of recovering from a number of damages a PDF may have. This includes re-generating a trailer, where the end of a file has been lost (e.g. because of incomplete downloads). If however ``None`` is returned for a PDF, then the recovery mechanisms were unsuccessful and you should check for any error messages (:attr:`Document.openErrCode`, :attr:`Document.openErrMsg`, :attr:`Tools.fitz_stderr`).


-----

   .. method:: Document._getXmlMetadataXref()

      Return the XML-based metadata object id from the PDF if present -- also refer to :meth:`Document._delXmlMetadata`. You can use it to retrieve the content via :meth:`Document._getXrefStream` and then work with it using some XML software.

-----

   .. method:: Document._getPageObjNumber(pno)

      or

   .. method:: Document._getPageXref(pno)

       Return the :data:`xref` and generation number for a given page.

      :arg int pno: Page number (zero-based).

      :rtype: list
      :returns: :data:`xref` and generation number of page ``pno`` as a list ``[xref, gen]``.

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
                * ``word``: the word, spaces stripped off *(str)*. Note that any non-space character is accepted as part of a word -- not only letters. So, ``    Hello   world!   `` will yield the two words ``Hello`` and ``world!``.
                * ``block_n, line_n, word_n``: 0-based counters for block, line and word *(int)*.

-----

   .. method:: Page.getDisplayList()

      Run a page through a list device and return its display list.

      :rtype: :ref:`DisplayList`
      :returns: the display list of the page.

-----

   .. method:: Page._getContents()

      Return a list of :data:`xref` numbers of :data:`contents` objects belonging to the page. 

      :rtype: list
      :returns: a list of :data:`xref` integers.

      Each page may have zero to many associated contents objects (streams) which contain PDF some operator syntax describing what appears where on the page (like text or images, etc. See the :ref:`AdobeManual`, chapter "Operator Summary", page 985). This function only enumerates the number(s) of such objects. To get the actual stream source, use function :meth:`Document._getXrefStream` with one of the numbers in this list. Use :meth:`Document._updateStream` to replace the content.

-----

   .. method:: Page._setContents(xref)

      PDF only: Set a given object (identified by its :data:`xref`) as the page's one and only :data:`contents` object. Useful for joining mutiple :data:`contents` objects as in the following snippet:

      >>> c = b""
      >>> xreflist = page._getContents()
      >>> for xref in xreflist: c += doc._getXrefStream(xref)
      >>> doc._updateStream(xreflist[0], c)
      >>> page._setContents(xreflist[0])
      >>> # doc.save(..., garbage = 1) will remove the unused objects

      :arg int xref: the cross reference number of a :data:`contents` object. An exception is raised if outside the valid :data:`xref` range or not a stream object.

-----

   .. method:: Page._cleanContents()

      Clean all :data:`contents` objects associated with this page (including contents of all annotations on the page). "Cleaning" includes syntactical corrections, standardizations and "pretty printing" of the contents stream. If a page has several contents objects, they will be combined into one. Any discrepancies between :data:`contents` and :data:`resources` objects will also be corrected. Note that the resulting :data:`contents` stream will be stored **uncompressed** (if you do not specify ``deflate`` on save). See :meth:`Page._getContents` for more details.

      :rtype: int
      :returns: 0 on success.

-----

   .. method:: Annot._cleanContents()

      Clean the :data:`contents` streams associated with the annotation. This is the same type of action :meth:`Page._cleanContents` performs -- just restricted to this annotation.

      :rtype: int
      :returns: 0 if successful (exception raised otherwise).

-----

   .. method:: Document.getCharWidths(xref = 0, limit = 256)

      Return a list of character glyphs and their widths for a font that is present in the document. A font must be specified by its PDF cross reference number :data:`xref`. This function is called automatically from :meth:`Page.insertText` and :meth:`Page.insertTextbox`. So you should rarely need to do this yourself.

      :arg int xref: cross reference number of a font embedded in the PDF. To find a font :data:`xref`, use e.g. ``doc.getPageFontList(pno)`` of page number ``pno`` and take the first entry of one of the returned list entries.

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

   .. method:: Document._getXrefString(xref)

      Return the string ("source code") representing an arbitrary object. For stream objects, only the non-stream part is returned. To get the stream content, use :meth:`_getXrefStream`.

      :arg int xref: :data:`xref` number.

      :rtype: string
      :returns: the string defining the object identified by :data:`xref`.

-----

   .. method:: Document._getGCTXerrmsg()

      Retrieve exception message text issued by PyMuPDF's low-level code. This in most cases, but not always, are MuPDF messages. This string will never be cleared -- only overwritten as needed. Only rely on it if a ``RuntimeError`` had been raised.

      :rtype: str
      :returns: last C-level error message on occasion of a ``RuntimeError`` exception.

-----

   .. method:: Document._getNewXref()

      Increase the :data:`xref` by one entry and return that number. This can then be used to insert a new object.

      :rtype: int
      :returns: the number of the new :data:`xref` entry.

-----

   .. method:: Document._updateObject(xref, obj_str, page = None)

      Associate the object identified by string ``obj_str`` with ``xref``, which must already exist. If ``xref`` pointed to an existing object, this will be replaced with the new object. If a page object is specified, links and other annotations of this page will be reloaded after the object has been updated.

      :arg int xref: :data:`xref` number.

      :arg str obj_str: a string containing a valid PDF object definition.

      :arg page: a page object. If provided, indicates, that annotations of this page should be refreshed (reloaded) to reflect changes incurred with links and / or annotations.
      :type page: :ref:`Page`

      :rtype: int
      :returns: zero if successful, otherwise an exception will be raised.

-----

   .. method:: Document._getXrefLength()

      Return length of :data:`xref` table.

      :rtype: int
      :returns: the number of entries in the :data:`xref` table.

-----

   .. method:: Document._getXrefStream(xref)

      Return the decompressed stream of the object referenced by ``xref``. For non-stream objects ``None`` is returned.

      :arg int xref: :data:`xref` number.
      
      :rtype: bytes
      :returns: the (decompressed) stream of the object.

-----

   .. method:: Document._updateStream(xref, stream, new = False)

      Replace the stream of an object identified by ``xref``. If the object has no stream, an exception is raised unless ``new = True`` is used. The function automatically performs a compress operation ("deflate").

      :arg int xref: :data:`xref` number.
      
      :arg bytes|bytearray stream: the new content of the stream.
      
      :arg bool new: whether to force accepting the stream, and thus **turning it into a stream object**.

      This method is intended to manipulate streams containing PDF operator syntax (see pp. 985 of the :ref:`AdobeManual`) as it is the case for e.g. page content streams.
      
      If you update a contents stream, you should use save parameter ``clean = True``. This ensures consistency between PDF operator source and the object structure.
      
      Example: Let us assume that you no longer want a certain image appear on a page. This can be achieved by deleting the respective reference in its contents source(s) -- and indeed: the image will be gone after reloading the page. But the page's :data:`resources` object would still show the image as being referenced by the page. This save option will clean up any such mismatches.

-----

   .. method:: Document._getOLRootNumber()

       Return :data:`xref` number of the /Outlines root object (this is **not** the first outline entry!). If this object does not exist, a new one will be created.

      :rtype: int
      :returns: :data:`xref` number of the **/Outlines** root object.

   .. method:: Document.extractImage(xref = 0)

      PDF Only: Extract data and meta information of an image stored in the document. The output can directly be used to be stored as an image file, as input for PIL, :ref:`Pixmap` creation, etc. This method avoids using pixmaps wherever possible to present the image in its original format (e.g. as JPEG).

      :arg int xref: :data:`xref` of an image object. If the object is not an image or other errors occur, an empty dictionary is returned and no exception is generated. Must however be in range of valid PDF cross reference numbers.

      :rtype: dict
      :returns: a dictionary with the following keys
      
        * ``ext`` (*str*) image type (e.g. ``'jpeg'``), usable as image file extension
        * ``smask`` (*int*) :data:`xref` number of a stencil (/SMask) image or zero
        * ``width`` (*int*) image width
        * ``height`` (*int*) image height
        * ``colorspace`` (*int*) the image's ``pixmap.n`` number (indicative only: depends on whether internal pixmaps had to be used). Zero for JPX images.
        * ``cs-name`` (*str*) the image's ``colorspace.name``.
        * ``xres`` (*int*) resolution in x direction. Zero for JPX images.
        * ``yres`` (*int*) resolution in y direction. Zero for JPX images.
        * ``image`` (*bytes*) image data, usable as image file content

      >>> d = doc.extractImage(25)
      >>> d
      {}
      >>> d = doc.extractImage(1373)
      >>> d
      {'ext': 'png', 'smask': 2934, 'width': 5, 'height': 629, 'colorspace': 3, 'xres': 96,
      'yres': 96, 'cs-name': 'DeviceRGB',
      'image': b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x05\ ...'}
      >>> imgout = open("image." + d["ext"], "wb")
      >>> imgout.write(d["image"])
      102
      >>> imgout.close()

      .. note:: There is a functional overlap with ``pix = fitz.Pixmap(doc, xref)``, followed by a ``pix.getPNGData()``. Main differences are that extractImage **(1)** does not only deliver PNG image formats, **(2)** is **very** much faster with non-PNG images, **(3)** usually results in much less disk storage for extracted images, **(4)** generates an empty *dict* for non-image xrefs (generates no exception). Look at the following example images within the same PDF.

         * xref 1268 is a PNG -- Comparable execution time and identical output::

            In [23]: %timeit pix = fitz.Pixmap(doc, 1268);pix.getPNGData()
            10.8 ms ± 52.4 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
            In [24]: len(pix.getPNGData())
            Out[24]: 21462
            
            In [25]: %timeit img = doc.extractImage(1268)
            10.8 ms ± 86 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
            In [26]: len(img["image"])
            Out[26]: 21462
         
         * xref 1186 is a JPEG -- :meth:`Document.extractImage` is **thousands of times faster** and produces a **much smaller** output (2.48 MB vs. 0.35 MB)::

            In [27]: %timeit pix = fitz.Pixmap(doc, 1186);pix.getPNGData()
            341 ms ± 2.86 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
            In [28]: len(pix.getPNGData())
            Out[28]: 2599433
            
            In [29]: %timeit img = doc.extractImage(1186)
            15.7 µs ± 116 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
            In [30]: len(img["image"])
            Out[30]: 371177

   .. method:: Document.extractFont(xref, info_only = False)

      PDF Only: Return an embedded font file's data and appropriate file extension. This can be used to store the font as an external file. The method does not throw exceptions (other than via checking for PDF and valid :data:`xref`).

      :arg int xref: PDF object number of the font to extract.
      :arg bool info_only: only return font information, not the buffer. To be used for information-only purposes, avoids allocation of large buffer areas.

      :rtype: tuple
      :returns: a tuple ``(basename, ext, subtype, buffer)``, where ``ext`` is a 3-byte suggested file extension (*str*), ``basename`` is the font's name (*str*), ``subtype`` is the font's type (e.g. "Type1") and ``buffer`` is a bytes object containing the font file's content (or ``b""``). For possible extension values and their meaning see :ref:`FontExtensions`. Return details on error:

            * ``("", "", "", b"")`` -- invalid xref or xref is not a (valid) font object.
            * ``(basename, "n/a", "Type1", b"")`` -- ``basename`` is one of the :ref:`Base-14-Fonts`, which cannot be extracted.

      Example:

      >>> # store font as an external file
      >>> name, ext, buffer = doc.extractFont(4711)
      >>> # assuming buffer is not None:
      >>> ofile = open(name + "." + ext, "wb")
      >>> ofile.write(buffer)
      >>> ofile.close()

      .. caution:: The basename is returned unchanged from the PDF. So it may contain characters (such as blanks) which may disqualify it as a filename for your operating system. Take appropriate action.

      .. note: The returned ``basename`` in general is **not** the original file name, but it probably has some similarity.

   .. attribute:: Document.FontInfos

       Contains following information for any font inserted via :meth:`Page.insertFont` in **this** session of PyMuPDF:

       * xref *(int)* -- XREF number of the ``/Type/Font`` object.
       * info *(dict)* -- detail font information with the following keys:

            * name *(str)* -- name of the basefont
            * idx *(int)* -- index number for multi-font files
            * type *(str)* -- font type (like "TrueType", "Type0", etc.)
            * ext *(str)* -- extension to be used, when font is extracted to a file (see :ref:`FontExtensions`).
            * glyphs (*list*) -- list of glyph numbers and widths (filled by textinsertion methods).

      :rtype: list

