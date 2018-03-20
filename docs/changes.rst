Change Logs
===============

Changes in Version 1.12.4
--------------------------
This is an extension of 1.12.3.

* Fix of `issue #147 <https://github.com/rk700/PyMuPDF/issues/147>`_: methods :meth:`Document.getPageFontlist` and :meth:`Document.getPageImagelist` now also show fonts and images contained in ``/Resources`` nested via "Form XObjects".
* Temporary fix of `issue #148 <https://github.com/rk700/PyMuPDF/issues/148>`_: Saving to new PDF files will now automatically use ``garbage = 2`` if a lower value is given. Final fix is to be expected with MuPDF's next version. At that point we will remove this circumvention.
* Preventive fix of illegally using stencil / image mask pixmaps in some methods.
* Method :meth:`Document.getPageFontlist` now includes the encoding name for each font in the list.
* Method :meth:`Document.getPageImagelist` now includes the decode method name for each image in the list.

Changes in Version 1.12.3
--------------------------
This is an extension of 1.12.2.

* Many functions now return ``None`` instead of ``0``, if the result has no other meaning than just indicating successful execution (:meth:`Document.close`, :meth:`Document.save`, :meth:`Document.select`, :meth:`Pixmap.writePNG` and many others).

Changes in Version 1.12.2
--------------------------
This is an extension of 1.12.1.

* Method :meth:`Page.showPDFpage` now accepts the new ``clip`` argument. This specifies an area of the source page to which the display should be restricted.

* New :attr:`Page.CropBox` and :attr:`Page.MediaBox` have been included for convenience.


Changes in Version 1.12.1
--------------------------
This is an extension of version 1.12.0.

* New method :meth:`Page.showPDFpage` displays another's PDF page. This is a **vector** image and therefore remains precise across zooming. Both involved documents must be PDF.

* New method :meth:`Page.getSVGimage` creates an SVG image from the page. In contrast to the raster image of a pixmap, this is a vector image format. The return is a unicode text string, which can be saved in a ``.svg`` file.

* Method :meth:`Page.getTextBlocks` now accepts an additional bool parameter "images". If set to true (default is false), image blocks (metadata only) are included in the produced list and thus allow detecting areas with rendered images.

* Minor bug fixes.

* "text" result of :meth:`Page.getText` concatenates all lines within a block using a single space character. MuPDF's original uses "\\n" instead, producing a rather ragged output.

* New properties of :ref:`Page` objects :attr:`Page.MediaBoxSize` and :attr:`Page.CropBoxPosition` provide more information about a page's dimensions. For non-PDF files (and for most PDF files, too) these will be equal to :attr:`Page.rect.bottom_right`, resp. :attr:`Page.rect.top_left`. For example, class :ref:`Shape` makes use of them to correctly position its items.

Changes in Version 1.12.0
--------------------------
This version is based on and requires MuPDF v1.12.0. The new MuPDF version contains quite a number of changes - most of them around text extraction. Some of the changes impact the programmer's API.

* :meth:`Outline.saveText` and :meth:`Outline.saveXML` have been deleted without replacement. You probably haven't used them much anyway. But if you are looking for a replacement: the output of :meth:`Document.getToC` can easily be used to produce something equivalent.

* Class ``TextSheet`` does no longer exist.

* Text "spans" (one of the hierarchy levels of :ref:`TextPage`) no longer contain positioning information (i.e. no "bbox" key). Instead, spans now provide the font information for its text. This impacts our JSON output variant.

* HTML output has improved very much: it now creates valid documents which can be displayed by browsers to produce a similar view as the original document.

* There is a new output format XHTML, which provides text and images in a browser-readable format. The difference to HTML output is, that no effort is made to reproduce the original layout.

* All output formats of :meth:`Page.getText` now support creating complete, valid documents, by wrapping them with appropriate header and trailer information. If you are interested in using the HTML output, please make sure to read :ref:`HTMLQuality`.

* To support finding text positions, we have added special methods that don't need detours like :meth:`TextPage.extractJSON` or :meth:`TextPage.extractXML`: use :meth:`Page.getTextBlocks` or resp. :meth:`Page.getTextWords` to create lists of text blocks or resp. words, which are accompanied by their rectangles. This should be much faster than the standard text extraction methods and also avoids using additional packages for interpreting their output.


Changes in Version 1.11.2
--------------------------
This is an extension of v1.11.1.

* New :meth:`Page.insertFont` creates a PDF ``/Font`` object and returns its object number.

* New :meth:`Document.extractFont` extracts the content of an embedded font given its object number.

* Methods ``*FontList(...)`` items no longer contain the PDF generation number. This value never had any significance. Instead, the font file extension is included (e.g. "pfa" for a "PostScript Font for ASCII"), which is more valuable information.

* Fonts other than "simple fonts" (Type1) are now also supported.

* New options to change :ref:`Pixmap` size:

    * Method :meth:`Pixmap.shrink` reduces the pixmap proportionally in place.

    * A new :ref:`Pixmap` copy constructor allows scaling via setting target width and height.


Changes in Version 1.11.1
--------------------------------
This is an extension of v1.11.0.

* New class ``Shape``. It facilitates and extends the creation of image shapes on PDF pages. It contains multiple methods for creating elementary shapes like lines, rectangles or circles, which can be combined into more complex ones and be given common properties like line width or colors. Combined shapes are handled as a unit and e.g. be "morphed" together. The class can accumulate multiple complex shapes and put them all in the page's foreground or background - thus also reducing the number of updates to the page's ``/Contents`` object.

* All ``Page`` draw methods now use the new ``Shape`` class.

* Text insertion methods ``insertText()`` and ``insertTextBox()`` now support morphing in addition to text rotation. They have become part of the ``Shape`` class and thus allow text to be freely combined with graphics.

* A new ``Pixmap`` constructor allows creating pixmap copies with an added alpha channel. A new method also allows directly manipulating alpha values.

* Binary algebraic operations with geometry objects (matrices, rectangles and points) now generally also support lists or tuples as the second operand. You can add a tuple ``(x, y)`` of numbers to a :ref:`Point`. In this context, such sequences are called "point-like" (resp. matrix-like, rectangle-like).

* Geometry objects now fully support in-place operators. For example, ``p /= m`` replaces point p with ``p * 1/m`` for a number, or ``p * ~m`` for a matrix-like object ``m``. Similarly, if ``r`` is a rectangle, then ``r |= (3, 4)`` is the new rectangle that also includes ``fitz.Point(3, 4)``, and ``r &= (1, 2, 3, 4)`` is its intersection with ``fitz.Rect(1, 2, 3, 4)``.

Changes in Version 1.11.0
--------------------------------
This version is based on and requires MuPDF v1.11.

Though MuPDF has declared it as being mostly a bug fix version, one major new feature is indeed contained: support of embedded files - also called portfolios or collections. We have extended PyMuPDF functionality to embrace this up to an extent just a little beyond the ``mutool`` utility as follows.

* The ``Document`` class now support embedded files with several new methods and one new property:

    - ``embeddedFileInfo()`` returns metadata information about an entry in the list of embedded files. This is more than ``mutool`` currently provides: it shows all the information that was used to embed the file (not just the entry's name).
    - ``embeddedFileGet()`` retrieves the (decompressed) content of an entry into a ``bytes`` buffer.
    - ``embeddedFileAdd(...)`` inserts new content into the PDF portfolio. We (in contrast to ``mutool``) **restrict** this to entries with a **new name** (no duplicate names allowed).
    - ``embeddedFileDel(...)`` deletes an entry from the portfolio (function not offered in MuPDF).
    - ``embeddedFileSetInfo()`` - changes filename or description of an embedded file.
    - ``embeddedFileCount`` - contains the number of embedded files.

* Several enhancements deal with streamlining geometry objects. These are not connected to the new MuPDF version and most of them are also reflected in PyMuPDF v1.10.0. Among them are new properties to identify the corners of rectangles by name (e.g. ``Rect.bottom_right``) and new methods to deal with set-theoretic questions like ``Rect.contains(x)`` or ``IRect.intersects(x)``. Special effort focussed on supporting more "Pythonic" language constructs: ``if x in rect ...`` is equivalent to ``rect.contains(x)``.

* The :ref:`Rect` chapter now has more background on empty amd infinite rectangles and how we handle them. The handling itself was also updated for more consistency in this area.

* We have started basic support for **generation** of PDF content:

    - ``Document.insertPage()`` adds a new page into a PDF, optionally containing some text.
    - ``Page.insertImage()`` places a new image on a PDF page.
    - ``Page.insertText()`` puts new text on an existing page

* For **FileAttachment** annotations, content and name of the attached file can extracted and changed.

Changes in Version 1.10.0
-------------------------------

MuPDF v1.10 Impact
~~~~~~~~~~~~~~~~~~~~~~~~
MuPDF version 1.10 has a significant impact on our bindings. Some of the changes also affect the API - in other words, **you** as a PyMuPDF user.

* Link destination information has been reduced. Several properties of the ``linkDest`` class no longer contain valuable information. In fact, this class as a whole has been deleted from MuPDF's library and we in PyMuPDF only maintain it to provide compatibilty to existing code.

* In an effort to minimize memory requirements, several improvements have been built into MuPDF v1.10:

    - A new ``config.h`` file can be used to de-select unwanted features in the C base code. Using this feature we have been able to reduce the size of our binary ``_fitz.o`` / ``_fitz.pyd`` by about 50% (from 9 MB to 4.5 MB). When UPX-ing this, the size goes even further down to a very handy 2.3 MB.

    - The alpha (transparency) channel for pixmaps is now optional. Letting alpha default to ``False`` significantly reduces pixmap sizes (by 20% - CMYK, 25% - RGB, 50% - GRAY). Many ``Pixmap`` constructors therefore now accept an ``alpha`` boolean to control inclusion of this channel. Other pixmap constructors (e.g. those for file and image input) create pixmaps with no alpha alltogether. On the downside, save methods for pixmaps no longer accept a ``savealpha`` option: this channel will always be saved when present. To minimize code breaks, we have left this parameter in the call patterns - it will just be ignored.

* ``DisplayList`` and ``TextPage`` class constructors now **require the mediabox** of the page they are referring to (i.e. the ``page.bound()`` rectangle). There is no way to construct this information from other sources, therefore a source code change cannot be avoided in these cases. We assume however, that not many users are actually employing these rather low level classes explixitely. So the impact of that change should be minor.

Other Changes compared to Version 1.9.3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* The new :ref:`Document` method ``write()`` writes an opened PDF to memory (as opposed to a file, like ``save()`` does).
* An annotation can now be scaled and moved around on its page. This is done by modifying its rectangle.
* Annotations can now be deleted. :ref:`Page` contains the new method ``deleteAnnot()``.
* Various annotation attributes can now be modified, e.g. content, dates, title (= author), border, colors.
* Method ``Document.insertPDF()`` now also copies annotations of source pages.
* The ``Pages`` class has been deleted. As documents can now be accessed with page numbers as indices (like ``doc[n] = doc.loadPage(n)``), and document object can be used as iterators, the benefit of this class was too low to maintain it. See the following comments.
* ``loadPage(n)`` / ``doc[n]`` now accept arbitrary integers to specify a page number, as long as ``n < pageCount``. So, e.g. ``doc[-500]`` is always valid and will load page ``(-500) % pageCount``.
* A document can now also be used as an iterator like this: ``for page in doc: ...<do something with "page"> ...``. This will yield all pages of ``doc`` as ``page``.
* The :ref:`Pixmap` method ``getSize()`` has been replaced with property ``size``. As before ``Pixmap.size == len(Pixmap)`` is true.
* In response to transparency (alpha) being optional, several new parameters and properties have been added to :ref:`Pixmap` and :ref:`Colorspace` classes to support determining their characteristics.
* The :ref:`Page` class now contains new properties ``firstAnnot`` and ``firstLink`` to provide starting points to the respective class chains, where ``firstLink`` is just a mnemonic synonym to method ``loadLinks()`` which continues to exist. Similarly, the new property ``rect`` is a synonym for method ``bound()``, which also continues to exist.
* :ref:`Pixmap` methods ``samplesRGB()`` and ``samplesAlpha()`` have been deleted because pixmaps can now be created without transparency.
* :ref:`Rect` now has a property ``irect`` which is a synonym of method ``round()``. Likewise, :ref:`IRect` now has property ``rect`` to deliver a :ref:`Rect` which has the same coordinates as floats values.
* Document has the new method ``searchPageFor()`` to search for a text string. It works exactly like the corresponding ``Page.searchFor()`` with page number as additional parameter.


Changes in Version 1.9.3
----------------------------------
This version is also based on MuPDF v1.9a. Changes compared to version 1.9.2:

* As a major enhancement, annotations are now supported in a similar way as links. Annotations can be displayed (as pixmaps) and their properties can be accessed.
* In addition to the document ``select()`` method, some simpler methods can now be used to manipulate a PDF:

    - ``copyPage()`` copies a page within a document.
    - ``movePage()`` is similar, but deletes the original.
    - ``deletePage()`` deletes a page
    - ``deletePageRange()`` deletes a page range

* ``rotation`` or ``setRotation()`` access or change a PDF page's rotation, respectively.
* Available but undocumented before, :ref:`IRect`, :ref:`Rect`, :ref:`Point` and :ref:`Matrix` support the ``len()`` method and their coordinate properties can be accessed via indices, e.g. ``IRect.x1 == IRect[2]``.
* For convenience, documents now support simple indexing: ``doc.loadPage(n) == doc[n]``. The index may however be in range ``-pageCount < n < pageCount``, such that ``doc[-1]`` is the last page of the document.

Changes in Version 1.9.2
------------------------------
This version is also based on MuPDF v1.9a. Changes compared to version 1.9.1:

* ``fitz.open()`` (no parameters) creates a new empty **PDF** document, i.e. if saved afterwards, it must be given a ``.pdf`` extension.
* :ref:`Document` now accepts all of the following formats (``Document`` and ``open`` are synonyms):

  - ``open()``,
  - ``open(filename)`` (equivalent to ``open(filename, None)``),
  - ``open(filetype, area)`` (equivalent to ``open(filetype, stream = area)``).

  Type of memory area ``stream`` may be ``str`` (Python 2), ``bytes`` (Python 3) or ``bytearray`` (Python 2 and 3). Thus, e.g. ``area = open("file.pdf", "rb").read()`` may be used directly (without first converting it to bytearray).
* New method ``Document.insertPDF()`` (PDFs only) inserts a range of pages from another PDF.
* ``Document`` objects doc now support the ``len()`` function: ``len(doc) == doc.pageCount``.
* New method ``Document.getPageImageList()`` creates a list of images used on a page.
* New method ``Document.getPageFontList()`` creates a list of fonts referenced by a page.
* New pixmap constructor ``fitz.Pixmap(doc, xref)`` creates a pixmap based on an opened PDF document and an XREF number of the image.
* New pixmap constructor ``fitz.Pixmap(cspace, spix)`` creates a pixmap as a copy of another one ``spix`` with the colorspace converted to ``cspace``. This works for all colorspace combinations.
* Pixmap constructor ``fitz.Pixmap(colorspace, width, height, samples)`` now allows ``samples`` to also be ``str`` (Python 2) or ``bytes`` (Python 3), not only ``bytearray``.


Changes in Version 1.9.1
----------------------------
This version of PyMuPDF is based on MuPDF library source code version 1.9a published on April 21, 2016.

Please have a look at MuPDF's website to see which changes and enhancements are contained herein.

Changes in version 1.9.1 compared to version 1.8.0 are the following:

* New methods ``getRectArea()`` for both ``fitz.Rect`` and ``fitz.IRect``
* Pixmaps can now be created directly from files using the new constructor ``fitz.Pixmap(filename)``.
* The Pixmap constructor ``fitz.Pixmap(image)`` has been extended accordingly.
* ``fitz.Rect`` can now be created with all possible combinations of points and coordinates.
* PyMuPDF classes and methods now all contain  __doc__ strings,  most of them created by SWIG automatically. While the PyMuPDF documentation certainly is more detailed, this feature should help a lot when programming in Python-aware IDEs.
* A new document method of ``getPermits()`` returns the permissions associated with the current access to the document (print, edit, annotate, copy), as a Python dictionary.
* The identity matrix ``fitz.Identity`` is now **immutable**.
* The new document method ``select(list)`` removes all pages from a document that are not contained in the list. Pages can also be duplicated and re-arranged.
* Various improvements and new members in our demo and examples collections. Perhaps most prominently: ``PDF_display`` now supports scrolling with the mouse wheel, and there is a new example program ``wxTableExtract`` which allows to graphically identify and extract table data in documents.
* ``fitz.open()`` is now an alias of ``fitz.Document()``.
* New pixmap method ``getPNGData()`` which will return a bytearray formatted as a PNG image of the pixmap.
* New pixmap method ``samplesRGB()`` providing a ``samples`` version with alpha bytes stripped off (RGB colorspaces only).
* New pixmap method ``samplesAlpha()`` providing the alpha bytes only of the ``samples`` area.
* New iterator ``fitz.Pages(doc)`` over a document's set of pages.
* New matrix methods ``invert()`` (calculate inverted matrix), ``concat()`` (calculate matrix product), ``preTranslate()`` (perform a shift operation).
* New ``IRect`` methods ``intersect()`` (intersection with another rectangle), ``translate()`` (perform a shift operation).
* New ``Rect`` methods ``intersect()`` (intersection with another rectangle), ``transform()`` (transformation with a matrix), ``includePoint()`` (enlarge rectangle to also contain a point), ``includeRect()`` (enlarge rectangle to also contain another one).
* Documented ``Point.transform()`` (transform a point with a matrix).
* ``Matrix``, ``IRect``, ``Rect`` and ``Point`` classes now support compact, algebraic formulations for manipulating such objects.
* Incremental saves for changes are possible now using the call pattern ``doc.save(doc.name, incremental=True)``.
* A PDF's metadata can now be deleted, set or changed by document method ``setMetadata()``. Supports incremental saves.
* A PDF's bookmarks (or table of contents) can now be deleted, set or changed with the entries of a list using document method ``setToC(list)``. Supports incremental saves.