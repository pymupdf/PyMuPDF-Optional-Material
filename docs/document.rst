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
:meth:`Document.deletePage`           PDF only: delete a page by its number
:meth:`Document.deletePageRange`      PDF only: delete a range of pages
:meth:`Document.embeddedFileAdd`      PDF only: add a new embedded file from buffer
:meth:`Document.embeddedFileDel`      PDF only: delete an embedded file entry
:meth:`Document.embeddedFileGet`      PDF only: extract an embedded file buffer
:meth:`Document.embeddedFileInfo`     PDF only: metadata of an embedded file
:meth:`Document.embeddedFileSetInfo`  PDF only: change metadata of an embedded file
:meth:`Document.getPageFontList`      make a list of fonts on a page
:meth:`Document.getPageImageList`     make a list of images on a page
:meth:`Document.getPagePixmap`        create a pixmap of a page by page number
:meth:`Document.getPageText`          extract the text of a page by page number
:meth:`Document.getToC`               create a table of contents
:meth:`Document.insertPage`           PDF only: insert a new page
:meth:`Document.insertPDF`            PDF only: insert pages from another PDF
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
:attr:`Document.isClosed`             has document been closed?
:attr:`Document.isPDF`                is document type PDF?
:attr:`Document.metadata`             metadata
:attr:`Document.name`                 filename of document
:attr:`Document.needsPass`            require password to access data?
:attr:`Document.openErrCode`          > 0 if repair occurred during open
:attr:`Document.openErrMsg`           last error message if openErrCode > 0
:attr:`Document.outline`              first `Outline` item
:attr:`Document.pageCount`            number of pages
:attr:`Document.permissions`          permissions to access the document
===================================== ==========================================================

**Class API**

.. class:: Document

    .. method:: __init__(self, [filename])

      Constructs a ``Document`` object from ``filename``.

      :arg str filename: A string containing the path / name of the document file to be used. The file will be opened and remain open until either explicitely closed (see below) or until end of program. If omitted or ``None``, a new empty **PDF** document will be created.

      :rtype: ``Document``
      :returns: A ``Document`` object.

    .. method:: __init__(self, filetype, stream)

      Constructs a ``Document`` object from memory area ``stream``.

      :arg str filetype: A string specifying the type of document contained in ``stream``. This may be either something that looks like a filename (e.g. ``"x.pdf"``), in which case MuPDF uses the extension to determine the type, or a mime type like ``application/pdf``. Recommended is using the filename scheme, or even the name of the original file for documentation purposes. But just using strings like ``"pdf"`` will also work.

      :arg bytes stream: A memory area representing the content of a supported document type. A type of ``bytearray`` is supported, too.

      :rtype: ``Document``
      :returns: A ``Document`` object.

    .. method:: authenticate(password)

      Decrypts the document with the string ``password``. If successful, all of the document's data can be accessed (e.g. for rendering).

      :arg str password: The password to be used.

      :rtype: int
      :returns: ``True (1)`` if decryption with ``password`` was successful, ``False (0)`` otherwise. If successfull, indicator ``isEncrypted`` is set to ``False``.

    .. method:: loadPage(pno = 0)

      Loads a ``Page`` for further processing like rendering, text searching, etc. See the :ref:`Page` object.

      :arg int pno: page number, zero-based (0 is default and the first page of the document) and ``< doc.pageCount``. If ``number < 0``, then page ``number % pageCount`` will be loaded (IAW ``pageCount`` will be added to ``number`` repeatedly, until the result is no longer negative). For example: to load the last page, you can specify ``doc.loadPage(-1)``. After this you have ``page.number == doc.pageCount - 1``.

      :rtype: :ref:`Page`

    .. note:: Conveniently, pages can also be loaded via indexes over the document: ``doc.loadPage(n) == doc[n]``. Consequently, a document can also be used as an iterator over its pages, e.g. ``for page in doc: ...`` and ``for page in reversed(doc): ...`` will yield the :ref:`Page` objects of ``doc`` as ``page``.

    .. method:: getToC(simple = True)

      Creates a table of contents out of the document's outline chain.

      :arg bool simple: Indicates whether a detailed ToC is required. If ``simple == False``, each entry of the list also contains a dictionary with :ref:`linkDest` details for each outline entry.

      :rtype: list

      :returns: a list of lists. Each entry has the form ``[lvl, title, page, dest]``. Its entries have the following meanings:

      * lvl - hierarchy level (integer). The first entry has hierarchy level 1, and entries in a row increase by at most one level.
      * title - title (string)
      * page - 1-based page number (integer). Page numbers ``< 1`` either indicate a target outside this document or no target at all (see next entry).
      * dest - included only if ``simple = False`` is specified. A dictionary containing details of the link destination.

    .. method:: getPagePixmap(pno, matrix = fitz.Identity, colorspace = "rgb", clip = None, alpha = True)

      Creates a pixmap from page ``pno`` (zero-based). Invokes :meth:`Page.getPixmap`.

      :arg int pno: Page number, zero-based. Any value ``< len(doc)`` is acceptable.

      :arg matrix: A transformation matrix - default is :ref:`Identity`.

      :type matrix: :ref:`Matrix`

      :arg colorspace: A string specifying the requested colorspace - default is ``rgb``.

      :type colorspace: str or :ref:`Colorspace`

      :arg clip: An :ref:`IRect` to restrict rendering of the page to the rectangle's area. If not specified, the complete page will be rendered.

      :type clip: :ref:`IRect`

      :arg bool alpha: Indicates whether a transparent image should be created. This has an important behavior impact. See :meth:`Page.getPixmap`.

      :rtype: :ref:`Pixmap`

    .. method:: getPageImageList(pno)

      PDF only: Returns a nested list of all image descriptions referenced by a page.

      :arg int pno: page number, zero-based. Any value ``< len(doc)`` is acceptable.

      :rtype: list

      :returns: a list of images shown on this page. Each entry looks like ``[xref, smask, width, height, bpc, colorspace, alt. colorspace, name]``. Where ``xref`` is the image object number, ``smask`` is the object number of its soft-mask image (if present), ``width`` and ``height`` are the image dimensions, ``bpc`` denotes the number of bits per component (a typical value is 8), ``colorspace`` a string naming the colorspace (like ``DeviceRGB``),  ``alt. colorspace`` is any alternate colorspace depending on the value of ``colorspace``, and ``name`` - which is the symbolic name *(str)* by which the page references this particular image in its content stream. See below how this information can be used to extract pages images as separate files. Another demonstration:

       >>> doc = fitz.open("pymupdf.pdf")
       >>> imglist = doc.getPageImageList(0)
       >>> for img in imglist: print img
       [[241, 0, 1043, 457, 8, 'DeviceRGB', '', 'Im1']]
       >>> pix = fitz.Pixmap(doc, 241)
       >>> pix
       fitz.Pixmap(DeviceRGB, fitz.IRect(0, 0, 1043, 457), 0)

    .. method:: getPageFontList(pno)

      PDF only: Return a nested list of all fonts referenced by the page.

      :arg int pno: page number, zero-based. Any value ``< len(doc)`` is acceptable.

      :rtype: list

      :returns: a list of fonts referenced by this page. Each entry looks like ``[xref, gen, type, basefont, name]``. Where ``xref`` is the font object number, ``gen`` its generation number (should usually be zero), ``type`` is the font type (like ``Type1`` or ``TrueType`` etc.), ``basefont`` is the base font name and ``name`` is the reference name by which the page points to it in its contents stream:

       >>> doc = fitz.open("pymupdf.pdf")
       >>> fontlist = doc.getPageFontList(85)
       >>> for font in fontlist: print(font)
       [1024, 0, 'Type1', 'CJXQIC+NimbusMonL-Bold', 'R366']
       [141, 0, 'Type1', 'HJQJNS+NimbusMonL-Regu', 'R247']
       [162, 0, 'Type1', 'CTCORW+NimbusRomNo9L-Regu', 'R245']
       [1039, 0, 'Type1', 'PWJUZS+NimbusRomNo9L-ReguItal', 'R373']
       [202, 0, 'Type1', 'VMQYGP+NimbusRomNo9L-Medi', 'R243']
       [100, 0, 'Type1', 'LSBBMD+NimbusSanL-Bold', 'R201']
      
      .. note:: Font are stored on the document level (like images). The reference name is specific for the page, i.e. other pages using the same font may use a different name for it. Also note, that a font may appear in this list though is not actually used by any text. But conversely, every piece of text on the page will refer to exactly one of these entries.

      .. note:: For more background see :ref:`AdobeManual` chapters 5.4 to 5.8, pp 410.

    .. method:: getPageText(pno, output = "text")

      Extracts the text of a page given its page number ``pno`` (zero-based).

      :arg int pno: Page number, zero-based. Any value ``< len(doc)`` is acceptable.

      :arg str output: A string specifying the requested output format: text, html, json or xml. Default is ``text``.

      :rtype: str

    .. method:: select(list)

      PDF only: Keeps only those pages of the document whose numbers occur in the list. Empty lists or elements outside the range ``0 <= page < doc.pageCount`` will cause a ``ValueError``. For more details see remarks at the bottom or this chapter.

      :arg sequence list: A list (or tuple) of page numbers (zero-based) to be included. Pages not in the list will be deleted (from memory) and become unavailable until the document is reopened. **Page numbers can occur multiple times and in any order:** the resulting sub-document will reflect the list exactly as specified.

      :rtype: int
      :returns: Zero upon successful execution. All document information will be updated to reflect the new state of the document, like outlines, number and sequence of pages, etc. Changes become permanent only after saving the document. Incremental save is supported.

    .. method:: setMetadata(m)

      PDF only: Sets or updates the metadata of the document as specified in ``m``, a Python dictionary. As with method ``select()``, these changes become permanent only when you save the document. Incremental save is supported.

      :arg dict m: A dictionary with the same keys as ``metadata`` (see below). All keys are optional. A PDF's format and encryption method cannot be set or changed, these keys therefore have no effect and will be ignored. If any value should not contain data, do not specify its key or set the value to ``None``. If you use ``m = {}`` all metadata information will be cleared to ``none``. If you want to selectively change only some values, modify ``doc.metadata`` directly and use it as the argument for this method.

      :rtype: int
      :returns: Zero upon successful execution and ``doc.metadata`` will be updated.

    .. method:: setToC(toc)

      PDF only: Replaces the **complete current outline** tree (table of contents) with a new one. After successful execution, the new outline tree can be accessed as usual via method ``getToC()`` or via property ``outline``. Like with other output-oriented methods, changes become permanent only via ``save()`` (incremental save supported). Internally, this method consists of the following two steps. For a demonstration see example below.

      Please note, that currently the ``is_open`` flag is set to ``False``. Therefore all entries will initially be shown collapsed in PDF readers.

      - Step 1 deletes all existing bookmarks.

      - Step 2 creates a new TOC from the entries contained in ``toc``.

      :arg sequence toc:

          A Python sequence with **all bookmark entries** that should form the new table of contents. Each entry of this list is again a list with the following format. Output variants of method ``getToC()`` are acceptable as input, too.

          * ``[lvl, title, page, dest]``, where

            - ``lvl`` is the hierarchy level (int > 0) of the item, starting with ``1`` and being at most 1 higher than that of the predecessor,

            - ``title`` (str) is the title to be displayed.

            - ``page`` (int) is the target page number **(attention: 1-based to support getToC()-output)**, must be in valid page range if positive. Set this to ``-1`` if there is no target, or the target is external.

            - ``dest`` (optional) is a dictionary or a number. If a number, it will be interpreted as the desired height (in points) this entry should point to on ``page`` in the current document. Use a dictionary (like the one given as output by ``getToC(simple = False)``) if you want to store destinations that are either "named", or reside outside this documennt (other files, internet resources, etc.).

      :rtype: int
      :returns: ``outline`` and ``getToC()`` will be updated upon successful execution. The return code will either equal the number of inserted items (``len(toc)``) or the number of deleted items if ``toc = []``.

      .. note:: We currently always set the :ref:`Outline` attribute ``is_open`` to ``False``. This shows all entries below level 1 as collapsed.

    .. method:: save(outfile, garbage=0, clean=0, deflate=0, incremental=0, ascii=0, expand=0, linear=0)

      PDF only: Saves the document in its **current state** under the name ``outfile``. A document may have changed for a number of reasons: e.g. after a successful ``authenticate``, a decrypted copy will be saved, and, in addition (even without optional parameters), some basic cleaning may also have occurred, e.g. broken xref tables may have been repaired and earlier incremental changes may have been resolved. If you executed any modifying methods like ``select()``, ``setMetadata()``, ``setToC()``, etc., their results will also be reflected in the saved version.

      :arg str outfile: The file name to save to. Must be different from the original value value if ``incremental=False``. When saving incrementally, ``garbage`` and ``linear`` **must be** ``False / 0`` and ``outfile`` **must equal** the original filename (for convenience use ``doc.name``).

      :arg int garbage: Do garbage collection: 0 = none, 1 = remove unused objects, 2 = in addition to 1, compact xref table, 3 = in addition to 2, merge duplicate objects, 4 = in addition to 3, check streams for duplication. Excludes ``incremental``.

      :arg int clean: Clean content streams [#f1]_: 0 / False, 1 / True.

      :arg int deflate: Deflate uncompressed streams: 0 / False, 1 / True.

      :arg int incremental: Only save changed objects: 0 / False, 1 / True. Excludes ``garbage`` and ``linear``. Cannot be used for decrypted files and for files opened in repair mode (``openErrCode > 0``). In these cases saving to a new file is required.

      :arg int ascii: Where possible make the output ASCII: 0 / False, 1 / True.

      :arg int expand: Decompress contents: 0 = none, 1 = images, 2 = fonts, 255 = all. This convenience option generates a decompressed file version that can be better read by some other programs.

      :arg int linear: Save a linearised version of the document: 0 = False, 1 = True. This option creates a file format for improved performance when read via internet connections. Excludes ``incremental``.

      :rtype: int
      :returns: Zero upon successful execution.

    .. method:: saveIncr()

      PDF only: saves the document incrementally. This is a convenience abbreviation for ``doc.save(doc.name, incremental = True)``.

    .. caution:: A PDF may not be encrypted, but still be password protected against changes - see the ``permissions`` property. Performing incremental saves if ``permissions["edit"] == False`` can lead to unpredictable results. Save to a new file in such a case. We also consider raising an exception under this condition.

    .. method:: searchPageFor(pno, text, hit_max = 16)

       Search for ``text`` on page number ``pno``. Works exactly like the corresponding :meth:`Page.searchFor`. Any integer ``pno < len(doc)`` is acceptable.
    
    .. method:: write(garbage=0, clean=0, deflate=0, ascii=0, expand=0, linear=0)

      PDF only: Writes the **current content of the document** to a bytes object instead of to a file like ``save()``. Obviously, you should be wary about memory requirements. The meanings of the parameters exactly equal those in :meth:`Document.save`. The tutorial contains an example for using this method as a pre-processor to `pdfrw <https://pypi.python.org/pypi/pdfrw/0.3>`_.

      :rtype: bytes
      :returns: a bytes object containing the complete document data.

    .. method:: insertPDF(docsrc, from_page = -1, to_page = -1, start_at = -1, rotate = -1, links = True)

      PDF only: Copy the page range **[from_page, to_page]** (including both) of PDF document ``docsrc`` into the current one. Inserts will start with page number ``start_at``. Negative values can be used to indicate default values. All pages thus copied will be rotated as specified. Links can be excluded in the target, see below. All page numbers are zero-based.

      :arg docsrc: An opened PDF ``Document`` which must not be the current document object. However, it may refer to the same underlying file.
      :type docsrc: ``Document``

      :arg int from_page: First page number in ``docsrc``. Default is zero.

      :arg int to_page: Last page number in ``docsrc`` to copy. Default is the last page.

      :arg int start_at: First copied page will become page number ``start_at`` in the destination. If omitted, the page range will be appended to current document. If zero, the page range will be inserted before current first page.

      :arg int rotate: All copied pages will be rotated by the provided value (degrees). If you do not specify a value (or ``-1``), the original will not be changed. Otherwise it must be an integer multiple of 90 (not checked). Rotation is counter-clockwise if ``rotate`` is positive, else clockwise.

      :arg bool links: Choose whether (internal and external) links should be included with the copy. Default is ``True``. An **internal** link is always excluded if its destination is not one of the copied pages.

      :rtype: int
      :returns: Zero upon successful execution.

    .. note:: If ``from_page > to_page``, pages will be copied in reverse order. If ``0 <= from_page == to_page``, then one page will be copied.

    .. note:: ``docsrc`` bookmarks **will not be copied**. It is easy however, to recover a table of contents for the resulting document. Look at the examples below and at program ``PDFjoiner.py`` in the *examples* directory: it can join PDF documents and at the same time piece together respective parts of the tables of contents.

    .. method:: insertPage(to = -1, text = None, fontsize = 11, width = 595, height = 842, fontname = "Helvetica", fontfile = None, color = (0, 0, 0))
    
      PDF only: Insert an empty page. Default page dimensions are those of A4 portrait paper format. Optionally, text can also be inserted - provided as a string or asequence.

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
      3. convert textfiles to PDF like in the demo script ``text2pdf.py``.
      4. For now, the inserted text should restrict itself to one byte character codes.
      5. An easy way to create pages with a usual paper format, use a statement like ``width, height = fitz.PaperSize("A4-L")``.
      6. To simplify color specification, we provide a :ref:`ColorDatabase`. This allows you to specify ``color = getColor("turquoise")``, without bothering about any more details.

    .. method:: newPage(to = -1, width = 595, height = 842)
    
      PDF only: Convenience method: insert an empty page like ``insertPage()`` does. Valid parameters have the same meaning. However, no text can be inserted, instead the inserted page object is returned.

      :rtype: :ref:`Page`
      :returns: the page object just inserted.

    .. method:: deletePage(pno)

      PDF only: Delete a page given by its 0-based number in range ``0 <= pno < len(doc)``.

      :arg int pno: the page to be deleted.

    .. method:: deletePageRange(from_page = -1, to_page = -1)

      PDF only: Delete a range of pages specified as 0-based numbers. Any negative parameter will first be replaced by ``len(doc) - 1``. After that, condition ``0 <= from_page <= to_page < len(doc)`` must be true. If the parameters are equal, one page will be deleted.

      :arg int from_page: the first page to be deleted.

      :arg int to_page: the last page to be deleted.

    .. method:: copyPage(pno, to = -1)

      PDF only: Copy a page within the document.

      :arg int pno: the page to be copied. Number must be in range ``0 <= pno < len(doc)``.

      :arg int to: the page number in front of which to insert the copy. To insert at end of document (default), specify a negative value.

    .. method:: movePage(pno, to = -1)

      PDF only: Move (copy and then delete original) page to another location.

      :arg int pno: the page to be moved. Number must be in range ``0 <= pno < len(doc)``.

      :arg int to: the page number in front of which to insert the moved page. To insert at end of document (default), specify a negative value. Must not be in ``(pno, pno + 1)``.

    .. method:: embeddedFileInfo(n)

      PDF only: Retrieve information of an embedded file identified by either its number or by its name.

      :arg n: index or name of entry. Obviously ``0 <= n < embeddedFileCount`` must be true if ``n`` is an integer.
      :type n: int or str
      :rtype: dict
      :returns: a dictionary with the following keys:

          * ``name`` - (*str*) name under which this entry is stored
          * ``file`` - (*str*) filename associated with the entry
          * ``desc`` - (*str*) description of the entry
          * ``size`` - (*int*) original content size
          * ``length`` - (*int*) compressed content length

    .. method:: embeddedFileSetInfo(n, filename = filename, desc = desc)

      PDF only: Change some information of an embedded file given its entry number or name. At least one of ``filename`` and ``desc`` must be specified. Response will be zero if successful, else an exception is raised.

      :arg n: index or name of entry. Obviously ``0 <= n < embeddedFileCount`` must be true if ``n`` is an integer.
      :type n: int or str
      :arg str filename: sets the filename of the entry.
      :arg str desc: sets the description of the entry.

    .. method:: embeddedFileGet(n)

      PDF only: Retrieve the content of embedded file by its entry number or name. If the document is not a PDF, or entry cannot be found, an exception is raised.

      :arg n: index or name of entry. Obviously ``0 <= n < embeddedFileCount`` must be true if ``n`` is an integer.
      :type n: int or str
      :rtype: ``bytes`` (Python 3), ``str`` (Python 2)

    .. method:: embeddedFileDel(name)

      PDF only: Remove an entry from the portfolio. As always, physical deletion of the embedded file content (and file space regain) will occur when the document is saved to a new file with ``garbage`` option. With an incremental save, the associated object will only be marked deleted.

      .. note:: We do not support entry **numbers** for this function yet. If you need to e.g. delete **all** embedded files, scan through all embedded files by number, and use the returned dictionary's ``name`` entry to delete each one. This function will delete the first entry with this name it finds. Be wary that for arbitrary PDF files, this may not have been the only one, because PDF itself has no mechanism to prevent duplicate entries ...

      :arg str name: name of entry.

    .. method:: embeddedFileAdd(stream, name, filename = filename, desc = desc)

      PDF only: Add new content to the document's portfolio.

      :arg stream: contents
      :type stream: bytes or bytearray or str (Python 2 only)
      :param str name: new entry identifier, must not already exist in embedded files.
      :param str filename: optional filename or ``None``, documentation only, will be set to ``name`` if ``None`` or omitted.
      :param str desc: optional description or ``None``, arbitrary documentation text, will be set to ``name`` if ``None`` or omitted.
      :rtype: int
      :returns: the index given to the new entry. In the current (April 11, 2017) MuPDF version, this is not reliably true (for this reason we have decided to restrict ``embeddedFileDel()`` to entries identified by name). Use character string look up to find your entry again. For any error condition, an exception is raised.

    .. method:: close()

      Release objects and space allocations associated with the document. If created from a file, also closes ``filename`` (releasing control to the OS).

    .. attribute:: outline

      Contains the first :ref:`Outline` entry of the document (or ``None``). Can be used as a starting point to walk through all outline items. Accessing this property for encrypted, not authenticated documents will raise an ``AttributeError``.

      :type: :ref:`Outline`

    .. attribute:: isClosed

      ``False / 0`` if document is still open, ``True / 1`` otherwise. If closed, most other attributes and methods will have been deleted / disabled. In addition, :ref:`Page` objects referring to this document (i.e. created with :meth:`Document.loadPage`) and their dependent objects will no longer be usable. For reference purposes, :attr:`Document.name` still exists and will contain the filename of the original document (if applicable).

      :type: bool

    .. attribute:: isPDF

      ``True`` if this is a PDF document, else ``False``.

      :type: bool

    .. attribute:: needsPass

      Contains an indicator showing whether the document is encrypted (``True (1)``) or not (``False (0)``). This indicator remains unchanged - even after the document has been authenticated. Precludes incremental saves if set.

      :type: bool

    .. attribute:: isEncrypted

      This indicator initially equals ``needsPass``. After successful authentication, it is set to ``False`` to reflect the situation.

      :type: bool

    .. attribute:: permissions

      Shows the permissions to access the document. Contains a dictionary likes this:
      ::
       >>> doc.permissions
       {'print': True, 'edit': True, 'note': True, 'copy': True}

      The keys have the obvious meaning of permissions to print, change, annotate and copy the document, respectively.

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

      If ``openErrCode > 0``, errors have occurred while opening / parsing the document, which usually means document structure issues. In this case incremental save cannot be used.

      :type: int

    .. Attribute:: openErrMsg

      Contains either an empty string or the last open error message if ``openErrCode > 0``. Together with any other error messages of MuPDF's C library, it will also appear on ``SYSERR``.

      :type: str

    .. Attribute:: embeddedFileCount

      Contains the number of files in the embedded / portfolio files list (also known as collection or attached files). If the document is not a PDF, ``-1`` will be returned.

      :type: int

.. NOTE:: For methods that change the structure of a PDF (``insertPDF()``, ``select()``, ``copyPage()``, ``deletePage()`` and others), be aware that objects or properties in your program may have been invalidated or orphaned. Examples are :ref:`Page` objects and their children (links and annotations), variables holding old page counts, tables of content and the like. Remember to keep such variables up to date or delete orphaned objects.


Remarks on ``select()``
------------------------

Page numbers in the list need not be unique nor be in any particular sequence. This makes the method a versatile utility to e.g. select only the even or the odd pages, re-arrange a document from back to front, duplicate it, and so forth. In combination with text search or extraction you can also omit / include pages with no text or containing a certain text, etc.

You can execute several selections in a row. The document structure will be updated after each method execution.

Any of those changes will become permanent only with a ``doc.save()``. If you have de-selected many pages, consider specifying the ``garbage`` option to eventually reduce the resulting document's size (when saving to a new file).

Also note, that this method **preserves all links, annotations and bookmarks** that are still valid. In other words: deleting pages only deletes references which point to de-selected pages. Page number of bookmarks (outline items) are automatically updated when a TOC is retrieved again with ``getToC()``. If a bookmark's destination page happened to be deleted, then its page number in ``getToC()`` will be set to ``-1``.

The results of this method can of course also be achieved using combinations of methods ``copyPage()``, ``deletePage()`` and ``movePage()``. While there are many cases, when these methods are more practical, ``select()`` is easier and safer to use when many pages are involved.

``select()`` Examples
----------------------------------------

In general, any list of integers within the document's page range can be used. Here are some illustrations.

Delete pages with no text:
::
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
>>> r = list(range(len(doc) - 1, -1, -1))
>>> doc.select(r)
>>> doc.save("back-to-front.pdf")

``setMetadata()`` Example
----------------------------------------
Clear metadata information. If you do this out of privacy / data protection concerns, make sure you save the document as a new file with ``garbage > 0``. Only then the old ``/Info`` object will also be physically removed from the file. In this case, you may also want to clear any XML metadata inserted by several PDF editors:

>>> import fitz
>>> doc=fitz.open("pymupdf.pdf")
>>> doc.metadata             # look at what we currently have
{'producer': 'rst2pdf, reportlab', 'format': 'PDF 1.4', 'encryption': None, 'author':
'Jorj X. McKie', 'modDate': "D:20160611145816-04'00'", 'keywords': 'PDF, XPS, EPUB, CBZ',
'title': 'The PyMuPDF Documentation', 'creationDate': "D:20160611145816-04'00'",
'creator': 'sphinx', 'subject': 'PyMuPDF 1.9.1'}
>>> doc.setMetadata({})      # clear all fields
0
>>> doc.metadata             # look again to show what happened
{'producer': 'none', 'format': 'PDF 1.4', 'encryption': None, 'author': 'none',
'modDate': 'none', 'keywords': 'none', 'title': 'none', 'creationDate': 'none',
'creator': 'none', 'subject': 'none'}
>>> doc._delXmlMetadata()    # clear any XML metadata
0
>>> doc.save("anonymous.pdf", garbage = 4)       # save anonymized doc
0


``setToC()`` Example
----------------------------------
This shows how to modify or add a table of contents. Also have a look at ``csv2toc.py`` and ``toc2csv.py`` in the examples directory:

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

``insertPDF()`` Examples
-------------------------
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

Obviously, similar ways can be found in more general situations. Just make sure that hierarchy levels in a row do not increase by more than one. Inserting dummy bookmarks before and after ``toc2`` segments would heal such cases.

**(2) More examples:**

>>> # insert 5 pages of doc2, where its page 21 becomes page 15 in doc1
>>> doc1.insertPDF(doc2, from_page = 21, to_page = 25, start_at = 15)

>>> # same example, but pages are rotated and copied in reverse order
>>> doc1.insertPDF(doc2, from_page = 25, to_page = 21, start_at = 15, rotate = 90)

>>> # put copied pages in front of doc1
>>> doc1.insertPDF(doc2, from_page = 21, to_page = 25, start_at = 0)


Other Examples
----------------
**Extract all page-referenced images of a PDF into separate PNG files:**
::
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

.. [#f1] Content streams describe what (e.g. text or images) appears where and how on a page. PDF uses a specialized language to do this (pp. 985 in :ref:`AdobeManual`), which gets interpreted when a page is loaded.