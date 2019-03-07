.. _Document:

================
Document
================

This class represents a document. It can be constructed from a file or from memory.

Since version 1.9.0 there exists the alias ``open`` for this class.

For addional details on **embedded files** refer to Appendix 3.

===================================== ==========================================================
**Method / Attribute**                **Short Description**
===================================== ==========================================================
:meth:`Document.authenticate`         decrypt the document
:meth:`Document.close`                close the document
:meth:`Document.copyPage`             PDF only: copy a page to another location
:meth:`Document.convertToPDF`         write a PDF version to memory
:meth:`Document.deletePage`           PDF only: delete a page by its number
:meth:`Document.deletePageRange`      PDF only: delete a range of pages
:meth:`Document.embeddedFileAdd`      PDF only: add a new embedded file from buffer
:meth:`Document.embeddedFileDel`      PDF only: delete an embedded file entry
:meth:`Document.embeddedFileGet`      PDF only: extract an embedded file buffer
:meth:`Document.embeddedFileInfo`     PDF only: metadata of an embedded file
:meth:`Document.embeddedFileUpd`      PDF only: change an embedded file
:meth:`Document.embeddedFileSetInfo`  PDF only: change metadata of an embedded file
:meth:`Document.getPageFontList`      PDF only: make a list of fonts on a page
:meth:`Document.getPageImageList`     PDF only: make a list of images on a page
:meth:`Document.getPagePixmap`        create a pixmap of a page by page number
:meth:`Document.getPageText`          extract the text of a page by page number
:meth:`Document.getToC`               create a table of contents
:meth:`Document.insertPage`           PDF only: insert a new page
:meth:`Document.insertPDF`            PDF only: insert pages from another PDF
:meth:`Document.layout`               re-paginate the document (if supported)
:meth:`Document.loadPage`             read a page
:meth:`Document.movePage`             PDF only: move a page to another location
:meth:`Document.newPage`              PDF only: insert a new empty page
:meth:`Document.save`                 PDF only: save the document
:meth:`Document.saveIncr`             PDF only: save the document incrementally
:meth:`Document.searchPageFor`        search for a string on a page
:meth:`Document.select`               PDF only: select a subset of pages
:meth:`Document.setMetadata`          PDF only: set the metadata
:meth:`Document.setToC`               PDF only: set the table of contents (TOC)
:meth:`Document.write`                PDF only: writes the document to memory
:attr:`Document.embeddedFileCount`    number of embedded files
:attr:`Document.FormFonts`            PDF only: list of existing field fonts
:attr:`Document.isClosed`             has document been closed?
:attr:`Document.isPDF`                is this a PDF?
:attr:`Document.isFormPDF`            is this a Form PDF?
:attr:`Document.isReflowable`         is this a reflowable document?
:attr:`Document.metadata`             metadata
:attr:`Document.name`                 filename of document
:attr:`Document.needsPass`            require password to access data?
:attr:`Document.isEncrypted`          document (still) encrypted?
:attr:`Document.openErrCode`          > 0 if repair occurred during open
:attr:`Document.openErrMsg`           last error message if openErrCode > 0
:attr:`Document.outline`              first `Outline` item
:attr:`Document.pageCount`            number of pages
:attr:`Document.permissions`          permissions to access the document
===================================== ==========================================================

**Class API**

.. class:: Document

    .. index::
       pair: filename; open args
       pair: stream; open args
       pair: filetype; open args
       pair: rect; open args
       pair: width; open args
       pair: height; open args
       pair: fontsize; open args
       pair: open; Document
       pair: filename; Document args
       pair: stream; Document args
       pair: filetype; Document args
       pair: rect; Document args
       pair: fontsize; Document args

    .. method:: __init__(self, filename = None, stream = None, filetype = None, rect = None, width = 0, height = 0, fontsize = 11)

      Creates a ``Document`` object.

      * With default parameters, a **new empty PDF** document will be created.
      * If ``stream`` is given, then the document is created from memory and either ``filename`` or ``filetype`` must indicate its type.
      * If ``stream`` is ``None``, then a document is created from a file given by ``filename``. Its type is inferred from the extension, which can be overruled by specifying ``filetype``.

      :arg str/pathlib filename: A UTF-8 string or ``pathlib`` object containing a file path (or a file type, see below).

      :arg bytes/bytearray stream: A memory area containing a supported document. Its type **must** be specified by either ``filename`` or ``filetype``.

      :arg str filetype: A string specifying the type of document. This may be something looking like a filename (e.g. ``"x.pdf"``), in which case MuPDF uses the extension to determine the type, or a mime type like ``application/pdf``. Just using strings like ``"pdf"`` will also work.

      :arg rect-like rect: a rectangle specifying the desired page size. This parameter is only meaningful for document types with a variable page layout ("reflowable" documents), like e-books or HTML, and ignored otherwise. If specified, it must be a non-empty, finite rectangle with top-left coordinates (0, 0). Together with parameter ``fontsize``, each page will be accordingly laid out and hence also determine the number of pages.

      :arg float width: may used together with ``height`` as an alternative to ``rect`` to specify layout information.

      :arg float height: may used together with ``width`` as an alternative to ``rect`` to specify layout information.

      :arg float fontsize: the default fontsize for reflowable document types. This parameter is ignored if none of the parameters ``rect`` or ``width`` and ``height`` are specified. Will be used to calculate the page layout.

      Overview of possible forms (using the ``open`` synonym of ``Document``):

      >>> # from a file
      >>> doc = fitz.open("some.pdf")
      >>> doc = fitz.open("some.file", None, "pdf")      # copes with wrong extension
      >>> doc = fitz.open("some.file", filetype = "pdf") # copes with wrong extension

      >>> # from memory
      >>> doc = fitz.open("pdf", mem_area)
      >>> doc = fitz.open(None, mem_area, "pdf")
      >>> doc = fitz.open(stream = mem_area, filetype = "pdf")

      >>> # new empty PDF
      >>> doc = fitz.open()

    .. method:: authenticate(password)

      Decrypts the document with the string ``password``. If successful, all of the document's data can be accessed (e.g. for rendering).

      :arg str password: The password to be used.

      :rtype: int
      :returns: positive value if decryption was successful, zero otherwise. If successful, indicator ``isEncrypted`` is set to ``False``.

    .. method:: loadPage(pno = 0)

      Load a :ref:`Page` for further processing like rendering, text searching, etc.

      :arg int pno: page number, zero-based (0 is default and the first page of the document) and ``< doc.pageCount``. If ``pno < 0``, then page ``pno % pageCount`` will be loaded (IAW ``pageCount`` will be added to ``pno`` until the result is no longer negative). For example: to load the last page, you can specify ``doc.loadPage(-1)``. After this you have ``page.number == doc.pageCount - 1``.

      :rtype: :ref:`Page`

    .. note:: Conveniently, pages can also be loaded via indexes over the document: ``doc.loadPage(n) == doc[n]``. Consequently, a document can also be used as an iterator over its pages, e.g. ``for page in doc: ...`` and ``for page in reversed(doc): ...`` will yield the :ref:`Page`\ s of ``doc`` as ``page``.

    .. index::
       pair: from_page; Document.convertToPDF args
       pair: to_page; Document.convertToPDF args
       pair: rotate; Document.convertToPDF args

    .. method:: convertToPDF(from_page = -1, to_page = -1, rotate = 0)

      Create a PDF version of the current document and write it to memory. **All document types** (except PDF) are supported. The parameters have the same meaning as in :meth:`insertPDF`. In essence, you can restrict the conversion to a page subset, specify page rotation, and revert page sequence.

      :arg int from_page: first page to copy (0-based). Default is first page.
      
      :arg int to_page: last page to copy (0-based). Default is last page.
      
      :arg int rotate: rotation angle. Default is 0 (no rotation). Should be ``n * 90`` with an integer ``n`` (not checked).
      
      :rtype: bytes
      :returns: a Python ``bytes`` object containing a PDF file image. It is created by internally using ``write(garbage=4, deflate = True)``. See :meth:`write`. You can output it directly to disk or open it as a PDF via ``fitz.open("pdf", pdfbytes)``. Here are some examples:

      >>> # convert an XPS file to PDF
      >>> xps = fitz.open("some.xps")
      >>> pdfbytes = xps.convertToPDF()
      >>>
      >>> # either do this --->
      >>> pdf = fitz.open("pdf", pdfbytes)
      >>> pdf.save("some.pdf")
      >>>
      >>> # or this --->
      >>> pdfout = open("some.pdf", "wb")
      >>> pdfout.write(pdfbytes)
      >>> pdfout.close()

      >>> # copy image files to PDF pages
      >>> # each page will have image dimensions
      >>> doc = fitz.open()                     # new PDF
      >>> imglist = [ ... image file names ...] # e.g. a directory listing
      >>> for img in imglist:
              imgdoc = fitz.open(img)           # open image as a document
              pdfbytes = imgdoc.convertToPDF()  # make a 1-page PDF of it
              imgpdf = fitz.open("pdf", pdfbytes)
              doc.insertPDF(imgpdf)             # insert the image PDF
      >>> doc.save("allmyimages.pdf")

      .. note:: The method uses the same logic as the ``mutool convert`` CLI. This works very well in most cases -- however, beware of the following limitations.

        * Image files: perfect, no issues detected. Apparently however, image transparency is ignored. If you need that (like for a watermark), use :meth:`Page.insertImage` instead. Otherwise, this method is recommended for its much better prformance.
        * XPS: appearance very good. Links work fine, outlines (bookmarks) are lost, but can easily be recovered [#f2]_.
        * EPUB, CBZ, FB2: similar to XPS.
        * SVG: medium. Roughly comparable to `svglib <https://github.com/deeplook/svglib>`_.

    .. method:: getToC(simple = True)

      Creates a table of contents out of the document's outline chain.

      :arg bool simple: Indicates whether a simple or a detailed ToC is required. If ``simple == False``, each entry of the list also contains a dictionary with :ref:`linkDest` details for each outline entry.

      :rtype: list

      :returns: a list of lists. Each entry has the form ``[lvl, title, page, dest]``. Its entries have the following meanings:

        * ``lvl`` -- hierarchy level (positive *int*). The first entry is always 1. Entries in a row are either **equal**, **increase** by 1, or **decrease** by any number.
        * ``title`` -- title (*str*)
        * ``page`` -- 1-based page number (*int*). Page numbers ``< 1`` either indicate a target outside this document or no target at all (see next entry).
        * ``dest`` -- (*dict*) included only if ``simple = False``. Contains details of the link destination.

    .. method:: getPagePixmap(pno, *args, **kwargs)

      Creates a pixmap from page ``pno`` (zero-based). Invokes :meth:`Page.getPixmap`.

      :rtype: :ref:`Pixmap`

    .. method:: getPageImageList(pno)

      PDF only: Return a list of all image descriptions referenced by a page.

      :arg int pno: page number, 0-based, any value ``< len(doc)``.

      :rtype: list

      :returns: a list of images shown on this page. Each entry looks like ``[xref, smask, width, height, bpc, colorspace, alt. colorspace, name, filter]``. Where
      
        * ``xref`` (*int*) is the image object number,
        * ``smask`` (*int* optional) is the object number of its soft-mask image (if present),
        * ``width`` and ``height`` (*ints*) are the image dimensions,
        * ``bpc`` (*int*) denotes the number of bits per component (a typical value is 8),
        * ``colorspace`` (*str*)a string naming the colorspace (like ``DeviceRGB``),
        * ``alt. colorspace`` (*str* optional) is any alternate colorspace depending on the value of ``colorspace``,
        * ``name`` (*str*) is the symbolic name by which the **page references the image** in its content stream, and
        * ``filter`` (*str* optional) is the decode filter of the image (:ref:`AdobeManual`, pp. 65).
      
      See below how this information can be used to extract PDF images as separate files. Another demonstration:

      >>> doc = fitz.open("pymupdf.pdf")
      >>> doc.getPageImageList(0)
      [[316, 0, 261, 115, 8, 'DeviceRGB', '', 'Im1', 'DCTDecode']]
      >>> pix = fitz.Pixmap(doc, 316)      # 316 is the xref of the image
      >>> pix
      fitz.Pixmap(DeviceRGB, fitz.IRect(0, 0, 261, 115), 0)

      .. note:: This list has no duplicate entries: the combination of :data:`xref` and ``name`` is unique. But by themselves, each of the two may occur multiple times. The same image may well be referenced under different names within a page. Duplicate ``name`` entries on the other hand indicate the presence of "Form XObjects" on the page, e.g. generated by :meth:`Page.showPDFpage`.

    .. method:: getPageFontList(pno)

      PDF only: Return a list of all fonts referenced by the page.

      :arg int pno: page number, 0-based, any value ``< len(doc)``.

      :rtype: list

      :returns: a list of fonts referenced by this page. Each entry looks like ``[xref, ext, type, basefont, name, encoding]``. Where
      
        * ``xref`` (*int*) is the font object number (may be zero if the PDF uses one of the builtin fonts directly),
        * ``ext`` (*str*) font file extension (e.g. ``ttf``, see :ref:`FontExtensions`),
        * ``type`` (*str*) is the font type (like ``Type1`` or ``TrueType`` etc.),
        * ``basefont`` (*str*) is the base font name,
        * ``name`` (*str*) is the reference name (or label), by which **the page references the font** in its contents stream(s), and
        * ``encoding`` (*str* optional) the font's character encoding if different from its built-in encoding (:ref:`AdobeManual`, p. 414):

      >>> doc = fitz.open("some.pdf")
      >>> for f in doc.getPageFontList(0): print(f)
      [24, 'ttf', 'TrueType', 'DOKBTG+Calibri', 'R10', '']
      [17, 'ttf', 'TrueType', 'NZNDCL+CourierNewPSMT', 'R14', '']
      [32, 'ttf', 'TrueType', 'FNUUTH+Calibri-Bold', 'R8', '']
      [28, 'ttf', 'TrueType', 'NOHSJV+Calibri-Light', 'R12', '']
      [8, 'ttf', 'Type0', 'ECPLRU+Calibri', 'R23', 'Identity-H']

      .. note:: This list has no duplicate entries: the combination of :data:`xref` and ``name`` is unique. But by themselves, each of the two may occur multiple times. Duplicate ``name`` entries indicate the presence of "Form XObjects" on the page, e.g. generated by :meth:`Page.showPDFpage`.

    .. method:: getPageText(pno, output = "text")

      Extracts the text of a page given its page number ``pno`` (zero-based). Invokes :meth:`Page.getText`.

      :arg int pno: page number, 0-based, any value ``< len(doc)``.

      :arg str output: A string specifying the requested output format: text, html, json or xml. Default is ``text``.

      :rtype: str

    .. index::
       pair: fontsize; Document.layout args
       pair: rect; Document.layout args
       pair: width; Document.layout args
       pair: height; Document.layout args

    .. method:: layout(rect=None, width=0, height=0, fontsize = 11)

      Re-paginate ("reflow") the document based on the given page dimension and fontsize. This only affects some document types like e-books and HTML. Ignored if not supported. Supported documents have ``True`` in property :attr:`isReflowable`.

      :arg rect-like rect: desired page size. Must be finite, not empty and start at point (0, 0).
      :arg float width: use it together with ``height`` as alternative to ``rect``.
      :arg float height: use it together with ``width`` as alternative to ``rect``.
      :arg float fontsize: the desired default fontsize.

    .. method:: select(s)

      PDF only: Keeps only those pages of the document whose numbers occur in the list. Empty sequences or elements outside the range ``0 <= page < doc.pageCount`` will cause a ``ValueError``. For more details see remarks at the bottom or this chapter.

      :arg sequence s: A sequence (see :ref:`SequenceTypes`) of page numbers (zero-based) to be included. Pages not in the sequence will be deleted (from memory) and become unavailable until the document is reopened. **Page numbers can occur multiple times and in any order:** the resulting document will reflect the sequence exactly as specified.

    .. method:: setMetadata(m)

      PDF only: Sets or updates the metadata of the document as specified in ``m``, a Python dictionary. As with :meth:`select`, these changes become permanent only when you save the document. Incremental save is supported.

      :arg dict m: A dictionary with the same keys as ``metadata`` (see below). All keys are optional. A PDF's format and encryption method cannot be set or changed and will be ignored. If any value should not contain data, do not specify its key or set the value to ``None``. If you use ``m = {}`` all metadata information will be cleared to the string ``"none"``. If you want to selectively change only some values, modify a copy of ``doc.metadata`` and use it as the argument. Arbitrary unicode values are possible if specified as UTF-8-encoded.

    .. method:: setToC(toc)

      PDF only: Replaces the **complete current outline** tree (table of contents) with the new one provided as the argument. After successful execution, the new outline tree can be accessed as usual via method ``getToC()`` or via property ``outline``. Like with other output-oriented methods, changes become permanent only via ``save()`` (incremental save supported). Internally, this method consists of the following two steps. For a demonstration see example below.

      - Step 1 deletes all existing bookmarks.

      - Step 2 creates a new TOC from the entries contained in ``toc``.

      :arg sequence toc:

          A Python nested sequence with **all bookmark entries** that should form the new table of contents. Each entry is a list with the following format. Output variants of method ``getToC()`` are also acceptable as input.

          * ``[lvl, title, page, dest]``, where

            - ``lvl`` is the hierarchy level (int > 0) of the item, starting with ``1`` and being at most 1 higher than that of the predecessor,

            - ``title`` (str) is the title to be displayed. It is assumed to be UTF-8-encoded (relevant for multibyte code points only).

            - ``page`` (int) is the target page number **(attention: 1-based to support getToC()-output)**, must be in valid page range if positive. Set this to ``-1`` if there is no target, or the target is external.

            - ``dest`` (optional) is a dictionary or a number. If a number, it will be interpreted as the desired height (in points) this entry should point to on ``page`` in the current document. Use a dictionary (like the one given as output by ``getToC(simple = False)``) if you want to store destinations that are either "named", or reside outside this documennt (other files, internet resources, etc.).

      :rtype: int
      :returns: ``outline`` and ``getToC()`` will be updated upon successful execution. The return code will either equal the number of inserted items (``len(toc)``) or the number of deleted items if ``toc`` is an empty sequence.

      .. note:: We currently always set the :ref:`Outline` attribute ``is_open`` to ``False``. This shows all entries below level 1 as collapsed.

    .. method:: save(outfile, garbage=0, clean=False, deflate=False, incremental=False, ascii=False, expand=0, linear=False, pretty=False, decrypt=True)

      PDF only: Saves the document in its **current state** under the name ``outfile``.

      :arg str outfile: The file name to save to. Must be different from the original value if "incremental" is false or zero. When saving incrementally, "garbage" and "linear" **must be** false or zero and this parameter **must equal** the original filename (for convenience use ``doc.name``).

      :arg int garbage: Do garbage collection. Positive values exclude ``incremental``.

       * 0 = none
       * 1 = remove unused objects
       * 2 = in addition to 1, compact the :data:`xref` table
       * 3 = in addition to 2, merge duplicate objects
       * 4 = in addition to 3, check object streams for duplication (may be slow)

      :arg bool clean: Clean content streams [#f1]_.

      :arg bool deflate: Deflate (compress) uncompressed streams.

      :arg bool incremental: Only save changed objects. Excludes "garbage" and "linear". Cannot be used for decrypted files and for repaired files (``openErrCode > 0``). In these cases saving to a new file is required.

      :arg bool ascii: Where possible convert binary data to ASCII.

      :arg int expand: Decompress objects. Generates versions that can be better read by some other programs.

       * 0 = none
       * 1 = images
       * 2 = fonts
       * 255 = all

      :arg bool linear: Save a linearised version of the document. This option creates a file format for improved performance when read via internet connections. Excludes "incremental".

      :arg bool pretty: Prettify the document source for better readability.

      :arg bool decrypt: Save a decrypted copy (the default). If false, the resulting PDF will be encrypted with the same password as the original. Will be ignored for non-encrypted files.

    .. method:: saveIncr()

      PDF only: saves the document incrementally. This is a convenience abbreviation for ``doc.save(doc.name, incremental = True)``.

    .. caution:: A PDF may not be encrypted, but still be password protected against changes -- see the ``permissions`` property. Performing incremental saves while ``permissions["edit"] == False`` can lead to unpredictable results. Save to a new file in such a case. We also consider raising an exception under this condition.

    .. method:: searchPageFor(pno, text, hit_max = 16, quads = False)

       Search for ``text`` on page number ``pno``. Works exactly like the corresponding :meth:`Page.searchFor`. Any integer ``pno < len(doc)`` is acceptable.

    .. method:: write(garbage=0, clean=False, deflate=False, ascii=False, expand=0, linear=False, pretty=False, decrypt=True)

      PDF only: Writes the **current content of the document** to a bytes object instead of to a file like ``save()``. Obviously, you should be wary about memory requirements. The meanings of the parameters exactly equal those in :meth:`save`. Cpater :ref:`FAQ` contains an example for using this method as a pre-processor to `pdfrw <https://pypi.python.org/pypi/pdfrw/0.3>`_.

      :rtype: bytes
      :returns: a bytes object containing the complete document data.

    .. index::
       pair: from_page; Document.insertPDF args
       pair: to_page; Document.insertPDF args
       pair: start_at; Document.insertPDF args
       pair: rotate; Document.insertPDF args
       pair: links; Document.insertPDF args

    .. method:: insertPDF(docsrc, from_page = -1, to_page = -1, start_at = -1, rotate = -1, links = True)

      PDF only: Copy the page range **[from_page, to_page]** (including both) of PDF document ``docsrc`` into the current one. Inserts will start with page number ``start_at``. Negative values can be used to indicate default values. All pages thus copied will be rotated as specified. Links can be excluded in the target, see below. All page numbers are zero-based.

      :arg docsrc: An opened PDF ``Document`` which must not be the current document object. However, it may refer to the same underlying file.
      :type docsrc: ``Document``

      :arg int from_page: First page number in ``docsrc``. Default is zero.

      :arg int to_page: Last page number in ``docsrc`` to copy. Default is the last page.

      :arg int start_at: First copied page will become page number ``start_at`` in the destination. If omitted, the page range will be appended to current document. If zero, the page range will be inserted before current first page.

      :arg int rotate: All copied pages will be rotated by the provided value (degrees, integer multiple of 90).

      :arg bool links: Choose whether (internal and external) links should be included with the copy. Default is ``True``. An **internal** link is always excluded if its destination is outside the copied page range.

    .. note:: If ``from_page > to_page``, pages will be **copied in reverse order**. If ``0 <= from_page == to_page``, then one page will be copied.

    .. note:: ``docsrc`` bookmarks **will not be copied**. It is easy however, to recover a table of contents for the resulting document. Look at the examples below and at program `PDFjoiner.py <https://github.com/pymupdf/PyMuPDF/blob/master/examples/PDFjoiner.py>`_ in the *examples* directory: it can join PDF documents and at the same time piece together respective parts of the tables of contents.

    .. index::
       pair: fontsize; Document.insertPage args
       pair: width; Document.insertPage args
       pair: height; Document.insertPage args
       pair: fontname; Document.insertPage args
       pair: fontfile; Document.insertPage args
       pair: color; Document.insertPage args

    .. method:: insertPage(to = -1, text = None, fontsize = 11, width = 595, height = 842, fontname = "Helvetica", fontfile = None, color = (0, 0, 0))

      PDF only: Insert an new page. Default page dimensions are those of A4 portrait paper format. Optionally, text can also be inserted -- provided as a string or as a sequence.

      :arg int to: page number (0-based) in front of which to insert. Valid specifications must be in range ``-1 <= pno <= len(doc)``. The default ``-1`` and ``pno = len(doc)`` indicate end of document, i.e. after the last page.

      :arg text: optional text to put on the page. If given, it will start at 72 points (one inch) below top and 50 points from left. Line breaks (``\n``) will be honored, if it is a string. No care will be taken as to whether lines are too wide. However, text output stops when no more lines will fit on the page (discarding any remaining text). If a sequence is specified, its entries must be a of type string. Each entry will be put on one line. Line breaks *within an entry* will be treated as any other white space. If you want to calculate the number of lines fitting on a page beforehand, use this formula: ``int((height - 108) / (fontsize * 1.2)``. So, this methods reserves one inch at the top and 1/2 inches at the bottom of the page as free space.
      :type text: str or sequence

      :arg float fontsize: font size in pixels. Default is 11. If more than one line is provided, a line spacing of ``fontsize * 1.2`` (fontsize plus 20%) is used.

      :arg float width: width in pixels. Default is 595 (A4 width). Choose 612 for *Letter width*.

      :arg float height: page height in pixels. Default is 842 (A4 height). Choose 792 for *Letter height*.

      :arg str fontname: name of one of the :ref:`Base-14-Fonts` (default is "Helvetica") if fontfile is not specified.

      :arg str fontfile: file path of a font existing on the system. If this parameter is specified, specifying ``fontname`` is **mandatory**. If the font is new to the PDF, it will be embedded. Of the font file, index 0 is used. Be sure to choose a font that supports horizontal, left-to-right spacing.

      :arg sequence color: RGB text color specified as a triple of floats in range 0 to 1. E.g. specify black (default) as ``(0, 0, 0)``, red as ``(1, 0, 0)``, some gray value as ``(0.5, 0.5, 0.5)``, etc.

      :rtype: int
      :returns: number of text lines put on the page. Use this to check which part of your text did not fit.

      **Notes:**

      This method can be used to

      1. create a PDF containing only one empty page of a given dimension. The size of such a file is well below 500 bytes and hence close to the theoretical PDF minimum.
      2. create a protocol page of which files have been embedded, or separator pages between joined pieces of PDF Documents.
      3. convert textfiles to PDF like in the demo script `text2pdf.py <https://github.com/pymupdf/PyMuPDF/blob/master/demo/text2pdf.py>`_.
      4. For now, the inserted text should restrict itself to one byte character codes.
      5. An easy way to create pages with a usual paper format, use a statement like ``width, height = fitz.PaperSize("A4-L")``.
      6. To simplify color specification, we provide a :ref:`ColorDatabase`. This allows you to specify ``color = getColor("turquoise")``, without bothering about any more details.

    .. index::
       pair: width; Document.newPage args
       pair: height; Document.newPage args

    .. method:: newPage(to = -1, width = 595, height = 842)
    
      PDF only: Convenience method: insert an empty page like ``insertPage()`` does. Valid parameters have the same meaning. However, no text can be inserted, instead the inserted page object is returned.

      If you do not need to insert text with your new page right away, then this method is the more convenient one: it saves you one statement if you need it for subsequent work -- see the below example.

      :rtype: :ref:`Page`
      :returns: the page object just inserted.

      >>> # let the following be a list of image files, from which we
      >>> # create a PDF with one image per page:
      >>> imglist = [...]   # list of image filenames
      >>> doc = fitz.open() # new empty PDF
      >>> for img in imglist:
              pix = fitz.Pixmap(img)
              page = doc.newPage(-1, width = pix.width, height = pix.height)
              page.insertImage(page.rect, pixmap = pix)
      >>> doc.save("image-file.pdf", deflate = True)

    .. method:: deletePage(pno = -1)

      PDF only: Delete a page given by its 0-based number in range ``0 <= pno < len(doc)``.

      :arg int pno: the page to be deleted. For ``-1`` the last page will be deleted.

    .. method:: deletePageRange(from_page = -1, to_page = -1)

      PDF only: Delete a range of pages specified as 0-based numbers. Any ``-1`` parameter will first be replaced by ``len(doc) - 1``. After that, condition ``0 <= from_page <= to_page < len(doc)`` must be true. If the parameters are equal, one page will be deleted.

      :arg int from_page: the first page to be deleted.

      :arg int to_page: the last page to be deleted.

    .. method:: copyPage(pno, to = -1)

      PDF only: Copy a page within the document.

      :arg int pno: the page to be copied. Must be in range ``0 <= pno < len(doc)``.

      :arg int to: the page number in front of which to copy. To insert after the last page (default), specify ``-1``.

    .. method:: movePage(pno, to = -1)

      PDF only: Move (copy and then delete original) a page within the document.

      :arg int pno: the page to be moved. Must be in range ``0 <= pno < len(doc)``.

      :arg int to: the page number in front of which to insert the moved page. To insert after the last page (default), specify ``-1``.

    .. index::
       pair: filename; Document.embeddedFileAdd args
       pair: ufilename; Document.embeddedFileAdd args
       pair: desc; Document.embeddedFileAdd args

    .. method:: embeddedFileAdd(buffer, name, filename = None, ufilename = None, desc = None)

      PDF only: Embed a new file. All string parameters except the name may be unicode (in previous versions, only ASCII worked correctly). File contents will be compressed (where beneficial).

      :arg bytes/bytearray buffer: file contents.
      :arg str name: entry identifier, must not already exist.
      :arg str filename: optional filename. Documentation only, will be set to ``name`` if ``None``.
      :arg str ufilename: optional unicode filename. Documentation only, will be set to ``filename`` if ``None``.
      :arg str desc: optional description. Documentation only, will be set to ``name`` if ``None``.
      
      .. note:: The position of the new entry in the embedded files list can in general not be predicted. Do not assume a specific place (like the end or the beginning), even if the chosen name seems to suggest it. If you add several files, their sequence in that list will probably not be maintained either. In addition, the various PDF viewers each seem to use their own ordering logic when showing the list of embedded files for the same PDF.

    .. method:: embeddedFileGet(n)

      PDF only: Retrieve the content of embedded file by its entry number or name. If the document is not a PDF, or entry cannot be found, an exception is raised.

      :arg int/str n: index or name of entry. For an integer ``0 <= n < embeddedFileCount`` must be true.

      :rtype: bytes

    .. method:: embeddedFileDel(name)

      PDF only: Remove an entry from `/EmbeddedFiles`. As always, physical deletion of the embedded file content (and file space regain) will occur when the document is saved to a new file with garbage option.

      :arg str name: name of entry. We do not support entry **numbers** for this function yet. If you need to e.g. delete **all** embedded files, scan through embedded files by number, and use the returned dictionary's ``name`` entry to delete each one.

      :rtype: int
      :returns: the number of deleted file entries.

      .. caution:: This function will delete **every entry with this name**. Be aware that PDFs not created with PyMuPDF may contain duplicate names, in which case more than one entry may be deleted.

    .. method:: embeddedFileInfo(n)

      PDF only: Retrieve information of an embedded file given by its number or by its name.

      :arg int/str n: index or name of entry. For an integer ``0 <= n < embeddedFileCount`` must be true.

      :rtype: dict
      :returns: a dictionary with the following keys:

          * ``name`` -- (*str*) name under which this entry is stored
          * ``filename`` -- (*str*) filename
          * ``ufilename`` -- (*unicode*) filename
          * ``desc`` -- (*str*) description
          * ``size`` -- (*int*) original file size
          * ``length`` -- (*int*) compressed file length

    .. index::
       pair: filename; Document.embeddedFileUpd args
       pair: ufilename; Document.embeddedFileUpd args
       pair: desc; Document.embeddedFileUpd args

    .. method:: embeddedFileUpd(n, buffer = None, filename = None, ufilename = None, desc = None)

      PDF only: Change an embedded file given its entry number or name. All parameters are optional. Letting them default leads to a no-operation.

      :arg int/str n: index or name of entry. For an integer ``0 <= n < embeddedFileCount`` must be true.
      :arg bytes/bytearray buffer: the new file content.
      :arg str filename: the new filename.
      :arg str ufilename: the new unicode filename.
      :arg str desc: the new description.

    .. method:: embeddedFileSetInfo(n, filename = None, ufilename = None, desc = None)

      PDF only: Change embedded file meta information. All parameters are optional. Letting them default will lead to a no-operation.

      :arg int/str n: index or name of entry. For an integer ``0 <= n < embeddedFileCount`` must be true.
      :arg str filename: sets the filename.
      :arg str ufilename: sets the unicode filename.
      :arg str desc: sets the description.

      .. note:: Deprecated subset of :meth:`embeddedFileUpd`. Will be deleted in next version.

    .. method:: close()

      Release objects and space allocations associated with the document. If created from a file, also closes ``filename`` (releasing control to the OS).

    .. attribute:: outline

      Contains the first :ref:`Outline` entry of the document (or ``None``). Can be used as a starting point to walk through all outline items. Accessing this property for encrypted, not authenticated documents will raise an ``AttributeError``.

      :type: :ref:`Outline`

    .. attribute:: isClosed

      ``False`` if document is still open. If closed, most other attributes and methods will have been deleted / disabled. In addition, :ref:`Page` objects referring to this document (i.e. created with :meth:`Document.loadPage`) and their dependent objects will no longer be usable. For reference purposes, :attr:`Document.name` still exists and will contain the filename of the original document (if applicable).

      :type: bool

    .. attribute:: isPDF

      ``True`` if this is a PDF document, else ``False``.

      :type: bool

    .. attribute:: isFormPDF

      ``True`` if this is a Form PDF document with field count greater zero, else ``False``.

      :type: bool

    .. attribute:: isReflowable

      ``True`` if document has a variable page layout (like e-books or HTML). In this case you can set the desired page dimensions during document creation (open) or via method :meth:`layout`.

      :type: bool

    .. attribute:: needsPass

      Contains an indicator showing whether the document is encrypted (``True``) or not (``False``). This indicator remains unchanged -- **even after the document has been authenticated**. Precludes incremental saves if ``True``.

      :type: bool

    .. attribute:: isEncrypted

      This indicator initially equals ``needsPass``. After an authentication, it is set to ``False`` to reflect the situation.

      :type: bool

    .. attribute:: permissions

      Shows the permissions to access the document. Contains a dictionary likes this:

       >>> doc.permissions
       {'print': True, 'edit': True, 'note': True, 'copy': True}

      The keys have the obvious meanings of permissions to print, change, annotate and copy the document, respectively.

      :type: dict

    .. attribute:: metadata

      Contains the document's meta data as a Python dictionary or ``None`` (if ``isEncrypted = True`` and ``needPass=True``). Keys are ``format``, ``encryption``, ``title``, ``author``, ``subject``, ``keywords``, ``creator``, ``producer``, ``creationDate``, ``modDate``. All item values are strings or ``None``.

      Except ``format`` and ``encryption``, the key names correspond in an obvious way to the PDF keys ``/Creator``, ``/Producer``, ``/CreationDate``, ``/ModDate``, ``/Title``, ``/Author``, ``/Subject``, and ``/Keywords`` respectively.

      - ``format`` contains the PDF version (e.g. 'PDF-1.6').

      - ``encryption`` either contains ``None`` (no encryption), or a string naming an encryption method (e.g. ``'Standard V4 R4 128-bit RC4'``). Note that an encryption method may be specified **even if** ``needsPass = False``. In such cases not all permissions will probably have been granted. Check dictionary ``permissions`` for details.

      - If the date fields contain valid data (which need not be the case at all!), they are strings in the PDF-specific timestamp format "D:<TS><TZ>", where

          - <TS> is the 12 character ISO timestamp ``YYYYMMDDhhmmss`` (``YYYY`` - year, ``MM`` - month, ``DD`` - day, ``hh`` - hour, ``mm`` - minute, ``ss`` - second), and

          - <TZ> is a time zone value (time intervall relative to GMT) containing a sign ('+' or '-'), the hour (``hh``), and the minute (``'mm'``, note the apostrophies!).

      - A Paraguayan value might hence look like ``D:20150415131602-04'00'``, which corresponds to the timestamp April 15, 2015, at 1:16:02 pm local time Asuncion.

      :type: dict

    .. Attribute:: name

      Contains the ``filename`` or ``filetype`` value with which ``Document`` was created.

      :type: str

    .. Attribute:: pageCount

      Contains the number of pages of the document. May return 0 for documents with no pages. Function ``len(doc)`` will also deliver this result.

      :type: int

    .. Attribute:: openErrCode

      If ``openErrCode > 0``, errors have occurred while opening / parsing the document, which usually means damages like document structure issues. In this case **incremental** save cannot be used. The **document is available** for processing however, potentially with restrictions (depending on damage details).

      :type: int

    .. Attribute:: openErrMsg

      Contains either an empty string or the last open error message if ``openErrCode > 0``. To see all messages, look at :attr:`Tools.fitz_stderr`, e.g. ``print(fitz.TOOLS.fitz_stderr)``.

      :type: str

    .. Attribute:: embeddedFileCount

      Contains the number of files in the `/EmbeddedFiles` list, -1 if the document is not a PDF.

      :type: int

    .. Attribute:: FormFonts

      A list of font resource names. Contains ``None`` if not a PDF and ``[]`` if not a Form PDF.

      :type: int

.. NOTE:: For methods that change the structure of a PDF (:meth:`insertPDF`, :meth:`select`, :meth:`copyPage`, :meth:`deletePage` and others), be aware that objects or properties in your program may have been invalidated or orphaned. Examples are :ref:`Page` objects and their children (links and annotations), variables holding old page counts, tables of content and the like. Remember to keep such variables up to date or delete orphaned objects.

Remarks on :meth:`select`
--------------------------

Page numbers in the sequence need not be unique nor be in any particular order. This makes the method a versatile utility to e.g. select only the even or the odd pages, re-arrange a document from back to front, duplicate it, and so forth. In combination with text search or extraction you can also omit / include pages with no text or containing a certain text, etc.

If you have de-selected many pages, consider specifying the ``garbage`` option to eventually reduce the resulting document's size (when saving to a new file).

Also note, that this method **preserves all links, annotations and bookmarks** that are still valid. In other words: deleting pages only deletes references which point to de-selected pages. Page numbers of bookmarks (outline items) are automatically updated when a TOC is retrieved again after execution of this method. If a bookmark's destination page happened to be deleted, then its page number will be set to ``-1``.

The results of this method can of course also be achieved using combinations of methods :meth:`copyPage`, :meth:`deletePage` etc. While there are many cases, when these methods are more practical, :meth:`select` is easier and safer to use when many pages are involved.

:meth:`select` Examples
--------------------------

In general, any sequence of integers that are in the document's page range can be used. Here are some illustrations.

Delete pages with no text::

 import fitz
 doc = fitz.open("any.pdf")
 r = list(range(len(doc)))                  # list of page numbers

 for page in doc:
     if not page.getText():                 # page contains no text
         r.remove(page.number)              # remove page number from list

 if len(r) < len(doc):                      # did we actually delete anything?
     doc.select(r)                          # apply the list
 doc.save("out.pdf", garbage = 4)           # save result to new PDF, OR

 # update the original document ... *** VERY FAST! ***
 doc.saveIncr()


Create a sub document with only the odd pages:

>>> import fitz
>>> doc = fitz.open("any.pdf")
>>> r = list(range(0, len(doc), 2))
>>> doc.select(r)                              # apply the list
>>> doc.save("oddpages.pdf", garbage = 4)      # save sub-PDF of the odd pages


Concatenate a document with itself:

>>> import fitz
>>> doc = fitz.open("any.pdf")
>>> r = list(range(len(doc)))
>>> r += r                                     # turn PDF into a copy of itself
>>> doc.select(r)
>>> doc.save("any+any.pdf")                    # contains doubled <any.pdf>

Create document copy in reverse page order (well, don't try with a million pages):

>>> import fitz
>>> doc = fitz.open("any.pdf")
>>> r = list(range(len(doc)))
>>> r.reverse()
>>> doc.select(r)
>>> doc.save("back-to-front.pdf")

:meth:`setMetadata` Example
-------------------------------
Clear metadata information. If you do this out of privacy / data protection concerns, make sure you save the document as a new file with ``garbage > 0``. Only then the old ``/Info`` object will also be physically removed from the file. In this case, you may also want to clear any XML metadata inserted by several PDF editors:

>>> import fitz
>>> doc=fitz.open("pymupdf.pdf")
>>> doc.metadata             # look at what we currently have
{'producer': 'rst2pdf, reportlab', 'format': 'PDF 1.4', 'encryption': None, 'author':
'Jorj X. McKie', 'modDate': "D:20160611145816-04'00'", 'keywords': 'PDF, XPS, EPUB, CBZ',
'title': 'The PyMuPDF Documentation', 'creationDate': "D:20160611145816-04'00'",
'creator': 'sphinx', 'subject': 'PyMuPDF 1.9.1'}
>>> doc.setMetadata({})      # clear all fields
>>> doc.metadata             # look again to show what happened
{'producer': 'none', 'format': 'PDF 1.4', 'encryption': None, 'author': 'none',
'modDate': 'none', 'keywords': 'none', 'title': 'none', 'creationDate': 'none',
'creator': 'none', 'subject': 'none'}
>>> doc._delXmlMetadata()    # clear any XML metadata
>>> doc.save("anonymous.pdf", garbage = 4)       # save anonymized doc

:meth:`setToC` Demonstration
----------------------------------
This shows how to modify or add a table of contents. Also have a look at `csv2toc.py <https://github.com/pymupdf/PyMuPDF/blob/master/examples/csv2toc.py>`_ and `toc2csv.py <https://github.com/pymupdf/PyMuPDF/blob/master/examples/toc2csv.py>`_ in the examples directory.

>>> import fitz
>>> doc = fitz.open("test.pdf")
>>> toc = doc.getToC()
>>> for t in toc: print(t)                           # show what we have
[1, 'The PyMuPDF Documentation', 1]
[2, 'Introduction', 1]
[3, 'Note on the Name fitz', 1]
[3, 'License', 1]
>>> toc[1][1] += " modified by setToC"               # modify something
>>> doc.setToC(toc)                                  # replace outline tree
3                                                    # number of bookmarks inserted
>>> for t in doc.getToC(): print(t)                  # demonstrate it worked
[1, 'The PyMuPDF Documentation', 1]
[2, 'Introduction modified by setToC', 1]            # <<< this has changed
[3, 'Note on the Name fitz', 1]
[3, 'License', 1]

:meth:`insertPDF` Examples
----------------------------
**(1) Concatenate two documents including their TOCs:**

>>> doc1 = fitz.open("file1.pdf")          # must be a PDF
>>> doc2 = fitz.open("file2.pdf")          # must be a PDF
>>> pages1 = len(doc1)                     # save doc1's page count
>>> toc1 = doc1.getToC(simple = False)     # save TOC 1
>>> toc2 = doc2.getToC(simple = False)     # save TOC 2
>>> doc1.insertPDF(doc2)                   # doc2 at end of doc1
>>> for t in toc2:                         # increase toc2 page numbers
        t[2] += pages1                     # by old len(doc1)
>>> doc1.setToC(toc1 + toc2)               # now result has total TOC

Obviously, similar ways can be found in more general situations. Just make sure that hierarchy levels in a row do not increase by more than one. Inserting dummy bookmarks before and after ``toc2`` segments would heal such cases. A ready-to-use GUI (wxPython) solution can be found in script `PDFjoiner.py <https://github.com/pymupdf/PyMuPDF/blob/master/examples/PDFjoiner.py>`_ of the examples directory.

**(2) More examples:**

>>> # insert 5 pages of doc2, where its page 21 becomes page 15 in doc1
>>> doc1.insertPDF(doc2, from_page = 21, to_page = 25, start_at = 15)

>>> # same example, but pages are rotated and copied in reverse order
>>> doc1.insertPDF(doc2, from_page = 25, to_page = 21, start_at = 15, rotate = 90)

>>> # put copied pages in front of doc1
>>> doc1.insertPDF(doc2, from_page = 21, to_page = 25, start_at = 0)

Other Examples
----------------
**Extract all page-referenced images of a PDF into separate PNG files**::

 for i in range(len(doc)):
     imglist = doc.getPageImageList(i)
     for img in imglist:
         xref = img[0]                  # xref number
         pix = fitz.Pixmap(doc, xref)   # make pixmap from image
         if pix.n - pix.alpha < 4:      # can be saved as PNG
             pix.writePNG("p%s-%s.png" % (i, xref))
         else:                          # CMYK: must convert first
             pix0 = fitz.Pixmap(fitz.csRGB, pix)
             pix0.writePNG("p%s-%s.png" % (i, xref))
             pix0 = None                # free Pixmap resources
         pix = None                     # free Pixmap resources

**Rotate all pages of a PDF:**

>>> for page in doc: page.setRotation(90)

.. rubric:: Footnotes

.. [#f1] Content streams describe what (e.g. text or images) appears where and how on a page. PDF uses a specialized mini language similar to PostScript to do this (pp. 985 in :ref:`AdobeManual`), which gets interpreted when a page is loaded.

.. [#f2] However, you **can** use :meth:`Document.getToC` and :meth:`Page.getLinks` (which are available for all document types) and copy this information over to the output PDF. See demo `pdf-converter.py <https://github.com/pymupdf/PyMuPDF/blob/master/demo/pdf-converter.py>`_.