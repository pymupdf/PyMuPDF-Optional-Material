============
Functions
============
The following are miscellaneous functions to be used by the experienced PDF programmer.

==================================== ==============================================================
**Function**                         **Short Description**
==================================== ==============================================================
:meth:`Annot._cleanContents`         PDF only: clean the annot's ``/Contents`` objects
:meth:`Annot._getXref`               PDF only: return XREF number of annotation
:meth:`Document._delXmlMetadata`     PDF only: remove XML metadata
:meth:`Document._getXmlMetadataXref` PDF only: return XML metadata XREF number
:meth:`Document._getCharWidths`      PDF only: return a list of glyph widths of a font
:meth:`Document._getNewXref`         PDF only: create and return a new XREF entry
:meth:`Document._getObjectString`    PDF only: return object source code
:meth:`Document._getOLRootNumber`    PDF only: return / create XREF of ``/Outline``
:meth:`Document._getPageObjNumber`   PDF only: return XREF and generation number of a page
:meth:`Document._getPageRectText`    PDF only: return raw string within rectangle
:meth:`Document._getPageXref`        PDF only: same as ``_getPageObjNumber()``
:meth:`Document._getXrefLength`      PDF only: return length of XREF table
:meth:`Document._getXrefStream`      PDF only: return content of a stream
:meth:`Document._getXrefString`      PDF only: return object source code
:meth:`Document._updateObject`       PDF only: insert or update a PDF object
:meth:`Document._updateStream`       PDF only: replace the stream of an object
:meth:`getPDFnow`                    return the current timestamp in PDF format
:meth:`getPDFstr`                    return PDF-compatible string
:meth:`Page.insertFont`              PDF only: store a new font in the document
:meth:`Page._cleanContents`          PDF only: clean the page's ``/Contents`` objects
:meth:`Page._getContents`            PDF only: return a list of content numbers
:meth:`Page._getRectText`            PDF only: return raw string within rectangle
:meth:`Page._getXref`                PDF only: return XREF number of page
:meth:`Page.getDisplayList`          create the page's display list
:meth:`Page.run`                     run a page through a device
:meth:`PaperSize`                    return width, height for known paper formats
==================================== ==============================================================

   .. method:: PaperSize(s)

      Convenience function to return width and height of a known paper format code. These values are given in pixels for the standard resolution 72 pixels = 1 inch.
      
      Currently defined formats include A0 through A10, B0 through B10, C0 through C10, Card-4x6, Card-5x7, Commercial, Executive, Invoice, Ledger, Legal, Legal-13, Letter, Monarch and Tabloid-Extra.

      A format name must be supplied as a string (case insensitive), optionally suffixed with "-L" (landscape) or "-P" (portrait). No suffix defaults to portrait.

      :arg str s: a format name like ``"A4"`` or ``"letter-l"``.

      :rtype: tuple
      :returns: ``(width, height)`` of the paper format. For an unknown format ``(-1, -1)`` is returned. ``PaperSize("A4")`` returns ``(595, 842)`` and ``PaperSize("letter-l")`` delivers ``(792, 612)``.

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

-----

   .. method:: Document._delXmlMetadata()

      PDF documents only: Delete an object containing XML-based metadata from the PDF. (Py-) MuPDF does not support XML-based metadata. Use this if you want to make sure that the conventional metadata dictionary will be used exclusively. Many thirdparty PDF programs insert their own metadata in XML format and thus may override what you store in the conventional dictionary. This method deletes any such reference, and the corresponding PDF object will be deleted during next garbage collection of the file.

-----

   .. method:: Document._getXmlMetadataXref()

      PDF documents only: Return he XML-based metadata object id from the PDF if present - also refer to :meth:`Document._delXmlMetadata`. You can use it to retrieve the content via :meth:`Document._getXrefStream` and then work with it using some XML software.
-----

   .. method:: Document._getPageObjNumber(pno)

      or

   .. method:: Document._getPageXref(pno)

       PDF documents only: Return the XREF and generation number for a given page.

      :arg int pno: Page number (zero-based).

      :rtype: list
      :returns: XREF and generation number of page ``pno`` as a list ``[xref, gen]``.

-----

   .. method:: Page._getXref()

      PDF documents only: Page version for ``_getPageObjNumber()`` only delivering the XREF (not the generation number).

-----

   .. method:: Page.run(dev, transform)

      Run a page through a device.

      :arg dev: Device, obtained from one of the :ref:`Device` constructors.
      :type dev: :ref:`Device`

      :arg transform: Transformation to apply to the page. Set it to :ref:`Identity` if no transformation is desired.
      :type transform: :ref:`Matrix`

-----

   .. method:: Page.insertFont(fontname = "Helvetica", fontfile = None)

      Store a new font for the page. This is a no-operation, if the font already exists.

      :arg str fontname: The reference name of the font. If the name does not occur in ``Page.getFontList()``, then this must be the name of one of the :ref:`Base-14-Fonts`, or ``fontfile`` must also be given. After using this method, this name prefixed with a slash "/" can be used to refer to the font.

      :arg str fontfile: font file name. The font will be included in the PDF.

      :rtype: int
      :returns: the XREF of the font.

-----

   .. method:: Page.getDisplayList()

      Run a page through a list device and return its display list.

      :rtype: :ref:`DisplayList`
      :returns: the display list of the page.

-----

   .. method:: Page._getContents()

      PDF documents only: Return a list of XREF numbers of ``/Contents`` objects belongig to the page. The length of this list will always be at least one.

      :rtype: list
      :returns: a list of XREF integers.

      Each page has one or more associated contents objects (streams) which contain PDF operator syntax describing what appears where on the page (like text or images, etc. See the :ref:`AdobeManual`, chapter "Operator Summary", page 985). This function only enumerates the XREF number(s) of such objects. To get the actual stream source, use function :meth:`Document._getXrefStream` with one of the numbers in this list. Use :meth:`Document._updateStream` to replace the content [#f1]_ [#f2]_.

-----

   .. method:: Page._cleanContents()

      PDF documents only: Clean all ``/Contents`` objects associated with this page (including contents of all annotations). "Cleaning" includes syntactical corrections, standardizations and "pretty printing" of the contents stream. If a page has several contents objects, they will be combined into one. Any discrepancies between ``/Contents`` and ``/Resources`` objects are also resolved / corrected. Note that the resulting contents stream will be stored uncompressed (if you do not specify ``deflate`` on save). See :meth:`Page._getContents` for more details.

      :rtype: int
      :returns: 0 on success.

-----

   .. method:: Annot._getXref()

      PDF documents only: Return the xref number of an annotation.

      :rtype: int
      :returns: XREF number of the annotation.

-----

   .. method:: Annot._cleanContents()

      PDF documents only: Clean the ``/Contents`` streams associated with the annotation. This is the same type of action :meth:`Page._cleanContents` performs - just restricted to this annotation.

      :rtype: int
      :returns: 0 if successful (exception raised otherwise).

-----

   .. method:: Document._getCharWidths(fontname = None, fontfile = None, xref = 0, limit = 256)

      PDF documents only: Return a list of character (glyph) widths for a font. A font must be specified by exactly one of the parameters ``fontname``, ``fontfile`` or ``xref``.

      :arg str fontname: name of a :ref:`Base-14-Fonts`. Excludes parameters ``fontfile`` and ``xref``.

      :arg str fontfile: path / name of a font file available on your system. Excludes parameters ``fontname`` and ``xref``.

      :arg int xref: cross reference number of a font embedded in the PDF. Excludes parameters ``fontname`` and ``fontfile``. To find a font xref, use e.g. ``doc.getPageFontList(pno)`` of page number ``pno`` and take the first entry of one of the returned list entries.

      :arg int limit: limits the number of returned entries. The default of 256 is sufficient for all fonts that only support characters up to unicode point 255. Specify a number as required.

      :rtype: list
      :returns: a list of ``limit`` floats, each representing the horizontal width in pixels, that a character needs which has a unicode point equal to an index entry. To get the actual width of some character "c", use ``widthlist[ord(c)] * fontsize``. Currently, only horizontal spacing is supported. A zero entry in this list indicates, that the font does not support this unicode point with a glyph. It is up to you to take appropriate action in such cases. Many fonts will have zero entries for indices ``< 32`` (which represents the space character ``0x20``), others only provide glyphs for the ASCII character set.

      A fairly simple function can be used to calculate the pixel width of a string named ``text``, like so:
      ::
          def pixlen(text, widthlist, fontsize):
            try:
                return sum([widthlist[ord(c)] for c in text]) * fontsize
            except IndexError:
                m = max([ord(c) for c in text])
                raise ValueError:("max. code point found: %i, increase limit" % m)
          

-----

   .. method:: Document._getPageRectText(pno, rect)

      PDF documents only: Return raw text contained in a rectangle.

      :arg int pno: page number.

      :arg rect: rectangle
      :type rect: :ref:`Rect`

      :rtype: string
      :returns: text contained in the rectangle

-----

   .. method:: Page._getRectText(rect)

      PDF documents only: Return raw plain text contained in a rectangle.

      :arg rect: rectangle
      :type rect: :ref:`Rect`

      :rtype: string
      :returns: text contained in the rectangle

-----

   .. method:: Document._getObjectString(xref)

      or

   .. method:: Document._getXrefString(xref)

      PDF documents only: Return the string ("source code") representing an arbitrary object. For stream objects, only the non-stream part is returned. To get the stream content, use :meth:`_getXrefStream`.

      :arg int xref: XREF number.

      :rtype: string
      :returns: the string defining the object identified by ``xref``.

-----

   .. method:: Document._getNewXref()

      PDF documents only: Increase the XREF by one entry and return that number. This can then be used to insert a new object.

      :rtype: int
      :returns: the number of the new XREF entry.

-----

   .. method:: Document._updateObject(xref, obj_str, page = None)

      PDF documents only: Associate the object identified by string ``obj_str`` with the XREF number ``xref``, which must already exist. If ``xref`` pointed to an existing object, this will be replaced with the new object. If a page object is specified, links and other annotations of this page will be reloaded after the object has been updated.

      :arg int xref: XREF number.

      :arg str obj_str: a string containing a valid PDF object definition.

      :arg page: a page object. If provided, indicates, that annotations of this page should be refreshed (reloaded) to reflect changes incurred with links and / or annotations.
      :type page: :ref:`Page`

      :rtype: int
      :returns: zero if successful, otherwise an exception will be raised.

-----

   .. method:: Document._getXrefLength()

      PDF documents only: Return length of XREF table.

      :rtype: int
      :returns: the number of entries in the XREF table.

-----

   .. method:: Document._getXrefStream(xref)

      PDF documents only: Return decompressed content stream of the object referenced by ``xref``. If the object has / is no stream, an exception is raised.

      :arg int xref: XREF number.
      
      :rtype: str or bytes
      :returns: the (decompressed) stream of the object. This is a string in Python 2 and a ``bytes`` object in Python 3.

-----

   .. method:: Document._updateStream(xref, stream)

      PDF documents only: Replace the stream of an object identified by ``xref``. If the object has no stream, an exception is raised. The function automatically performs a compress operation ("deflate").

      :arg int xref: XREF number.
      
      :arg stream: the new content of the stream.
      :type stream: bytes or bytearray
      
      :rtype: int

      This method is intended to manipulate streams containing PDF operator syntax (see pp. 985 of the :ref:`AdobeManual`) as it is the case for e.g. page content streams.
      
      If you update a contents stream, you should use save parameter ``clean = True``. This ensures consistency between PDF operator source and the object structure.
      
      Example: Let us assume that you no longer want a certain image appear on a page. This can be achieved by deleting [#f2]_ the respective reference in its contents source(s) - and indeed: the image will be gone after reloading the page. But the page's ``/Resources`` object would still [#f3]_ show the image as being referenced by the page. This save option will clean up any such mismatches.

-----

   .. method:: Document._getOLRootNumber()

      PDF documents only:  Return XREF number of the /Outlines root object (this is **not** the first outline entry!). If this object does not exist, a new one will be created.

      :rtype: int
      :returns: XREF number of the **/Outlines** root object.

.. rubric:: Footnotes

.. [#f1] If a page has multiple contents streams, they are treated as being one logical stream when the document is processed by reader software. A single operator cannot be split between stream boundaries, but a single **instruction** may well be! E.g. for invoking the display of an image, a complete instruction may look like ``q a b c d e f cm /imageid Do Q``. In this example, any single of these items (PDF notation: "lexical tokens") is completely contained in one stream, but ``q a b c d e f cm`` may be in one and ``/imageid Do Q`` may be in the next one.
.. [#f2] Note that ``/Contents`` objects (similar to /Resources) may be **shared** among pages. If you change a contents stream, this will affect all pages referencing the same object. To avoid this,use :meth:`Page._cleanContents` **before** making your changes.
.. [#f3] Resources objects are inheritable. This means that many pages can share one. Keeping a page's ``/Resources`` object in sync with changes of its ``/Contents`` therefore may require creating an own ``/Resources`` object for the page. This can achieved by either specifying the ``clean`` option when saving, or by invoking :meth:`Page._cleanContents`.
