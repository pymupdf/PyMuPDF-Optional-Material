Change Logs
===============

Changes in Version 1.14.0
---------------------------
MuPDF v1.14.0 required massive changes in PyMuPDF. There are also quite a lot of interesting new features now supported. Based on MuPDF v1.14.0, PyMuPDF contains the following changes:

* **Added** "ink" annotation.
* **Added** "rubber stamp" annotation.
* **Added** "squiggly" text marker annotation.
* **Added** new class :ref:`Quad` (quadrilateral or tetragon) -- which represents a general four-sided shape in the plane. The special subtype of rectangular, non-empty tetragons is used in text marker annotations and as returned objects in text search methods.
* **Added** a new option "decrypt" to :meth:`Document.save` and :meth:`Document.write`. Now you can **keep encryption** when saving a password protected PDF.
* **Changed:** Changes to annotations now **always require** :meth:`Annot.update` to become effective.
* **Changed** free text annotations to support the full Latin character set and range of appearance options.
* **Changed** text searching, :meth:`Page.searchFor`, to optionally return :ref:`Quad` instead :ref:`Rect` objects surrounding each search hit.
* **Changed** plain text output: we now add a ``\n`` to each line if it does not itself end with this character.
* **Fixed** issue 211 ("Something wrong in the doc").
* **Fixed** issue 213 ("Rewritten outline is displayed only by mupdf-based applications").
* **Fixed** issue 214 ("PDF decryption GONE!").
* **Fixed** issue 215 ("Formatting of links added with pyMuPDF").
* **Fixed** issue 217 ("extraction through json is failing for my pdf").


Changes in Version 1.13.19
---------------------------
This version contains some technical / performance improvements and bug fixes.

* **Changed** memory management: for Python 3 builds, Python memory management is exclusively used across all C-level code (i.e. no more native ``malloc()`` in MuPDF code or PyMuPDF interface code). This leads to improved memory usage profiles and also some runtime improvements: we have seen > 2% shorter runtimes for text extractions and pixmap creations (on Windows machines only to date).
* **Fixed** an error occurring in Python 2.7, which crashed the interpreter when using :meth:`TextPage.extractRAWDICT` (= ``Page.getText("rawdict")``).
* **Fixed** an error occurring in Python 2.7, when creating link destinations.
* **Extended** the :ref:`FAQ` chapter with more examples.

Changes in Version 1.13.18
---------------------------
* **Added** method :meth:`TextPage.extractRAWDICT`, and a corresponding new string parameter "rawdict" to method :meth:`Page.getText`. It extracts text and images from a page in Python *dict* form like :meth:`TextPage.extractDICT`, but with the detail level of :meth:`TextPage.extractXML`, which is position information down to each single character.

Changes in Version 1.13.17
---------------------------
* **Fixed** an error that intermittently caused an exception in :meth:`Page.showPDFpage`, when pages from many different source PDFs were shown.
* **Changed** method :meth:`Document.extractImage` to now return more meta information about the extracted imgage. Also, its performance has been greatly improved. Several demo scripts have been changed to make use of this method.
* **Changed** method :meth:`Document._getXrefStream` to now return ``None`` if the object is no stream and no longer raise an exception if otherwise.
* **Added** method :meth:`Document._deleteObject` which deletes a PDF object identified by its xref. Only to be used by the experienced PDF expert.
* **Added** a method :meth:`PaperRect` which returns a :ref:`Rect` for a supplied paper format string. Example: ``fitz.PaperRect("letter") = fitz.Rect(0.0, 0.0, 612.0, 792.0)``.
* **Added** a :ref:`FAQ` chapter to this document.

Changes in Version 1.13.16
---------------------------
* **Added** support for correctly setting transparency (opacity) for certain annotation types.
* **Added** a tool property (:attr:`Tools.fitz_config`) showing the configuration of this PyMuPDF version.
* **Fixed** issue #193 ('insertText(overlay=False) gives "cannot resize a buffer with shared storage" error') by avoiding read-only buffers.

Changes in Version 1.13.15
---------------------------
* **Fixed** issue #189 ("cannot find builtin CJK font"), so we are supporting builtin CJK fonts now (CJK = China, Japan, Korea). This should lead to correctly generated pixmaps for documents using these languages. This change has consequences for our binary file size: it will now range between 8 and 10 MB, depending on the OS.
* **Fixed** issue #191 ("Jupyter notebook kernel dies after ca. 40 pages"), which occurred when modifying the contents of an annotation.

Changes in Version 1.13.14
---------------------------
This patch version contains several improvements, mainly for annotations.

* **Changed** :attr:`Annot.lineEnds` is now a list of two integers representing the line end symbols. Previously was a *dict* of strings.
* **Added** support of line end symbols for applicable annotations. PyMuPDF now can generate these annotations including the line end symbols.
* **Added** :meth:`Annot.setLineEnds` adds line end symbols to applicable annotation types ('Line', 'PolyLine', 'Polygon').
* **Changed** technical implementation of :meth:`Page.insertImage` and :meth:`Page.showPDFpage`: they now create there own contents objects, thereby avoiding changes of potentially large streams with consequential compression / decompression efforts and high change volumes with incremental updates.

Changes in Version 1.13.13
---------------------------
This patch version contains several improvements for embedded files and file attachment annotations.

* **Added** :meth:`Document.embeddedFileUpd` which allows changing **file content and metadata** of an embedded file. It supersedes the old method :meth:`Document.embeddedFileSetInfo` (which will be deleted in a future version). Content is automatically compressed and metadata may be unicode.
* **Changed** :meth:`Document.embeddedFileAdd` to now automatically compress file content. Accompanying metadata can now be unicode (had to be ASCII in the past).
* **Changed** :meth:`Document.embeddedFileDel` to now automatically delete **all entries** having the supplied identifying name. The return code is now an integer count of the removed entries (was ``None`` previously).
* **Changed** embedded file methods to now also accept or show the PDF unicode filename as additional parameter ``ufilename``.
* **Added** :meth:`Page.addFileAnnot` which adds a new file attachment annotation.
* **Changed** :meth:`Annot.fileUpd` (file attachment annot) to now also accept the PDF unicode ``ufilename`` parameter. The description parameter ``desc`` correctly works with unicode. Furthermore, **all** parameters are optional, so metadata may be changed without also replacing the file content.
* **Changed** :meth:`Annot.fileInfo` (file attachment annot) to now also show the PDF unicode filename as parameter ``ufilename``.
* **Fixed** issue #180 ("page.getText(output='dict') return invalid bbox") to now also work for vertical text.
* **Fixed** issue #185 ("Can't render the annotations created by PyMuPDF"). The issue's cause was the minimalistic MuPDF approach when creating annotations. Several annotation types have no ``/AP`` ("appearance") object when created by MuPDF functions. MuPDF, SumatraPDF and hence also PyMuPDF cannot render annotations without such an object. This fix now ensures, that an appearance object is always created together with the annotation itself. We still do not support line end styles.

Changes in Version 1.13.12
---------------------------
* **Fixed** issue #180 ("page.getText(output='dict') return invalid bbox"). Note that this is a circumvention of an MuPDF error, which generates zero-height character rectangles in some cases. When this happens, this fix ensures a bbox height of at least fontsize.
* **Changed** for ListBox and ComboBox widgets, the attribute list of selectable values has been renamed to :attr:`Widget.choice_values`.
* **Changed** when adding widgets, any missing of the :ref:`Base-14-Fonts` is automatically added to the PDF. Widget text fonts can now also be chosen from existing widget fonts. Any specified field values are now honored and lead to a field with a preset value.
* **Added** :meth:`Annot.updateWidget` which allows changing existing form fields -- including the field value.

Changes in Version 1.13.11
---------------------------
While the preceeding patch subversions only contained various fixes, this version again introduces major new features:

* **Added** basic support for PDF widget annotations. You can now add PDF form fields of types Text, CheckBox, ListBox and ComboBox. Where necessary, the PDF is tranformed to a Form PDF with the first added widget.
* **Fixed** issues #176 ("wrong file embedding"), #177 ("segment fault when invoking page.getText()")and #179 ("Segmentation fault using page.getLinks() on encrypted PDF").


Changes in Version 1.13.7
--------------------------
* **Added** support of variable page sizes for reflowable documents (e-books, HTML, etc.): new parameters ``rect`` and ``fontsize`` in :ref:`Document` creation (open), and as a separate method :meth:`Document.layout`.
* **Added** :ref:`Annot` creation of many annotations types: sticky notes, free text, circle, rectangle, line, polygon, polyline and text markers.
* **Added** support of annotation transparency (:attr:`Annot.opacity`, :meth:`Annot.setOpacity`).
* **Changed** :attr:`Annot.vertices`: point coordinates are now grouped as pairs of floats (no longer as separate floats).
* **Changed** annotation colors dictionary: the two keys are now named ``"stroke"`` (formerly ``"common"``) and ``"fill"``.
* **Added** :attr:`Document.isDirty` which is ``True`` if a PDF has been changed in this session. Reset to ``False`` on each :meth:`Document.save` or :meth:`Document.write`.

Changes in Version 1.13.6
--------------------------
* Fix #173: for memory-resident documents, ensure the stream object will not be garbage-collected by Python before document is closed.

Changes in Version 1.13.5
--------------------------
* New low-level method :meth:`Page._setContents` defines an object given by its xref to serve as the ``/Contents`` object.
* Changed and extended PDF form field support: the attribute ``widget_text`` has been renamed to :attr:`Annot.widget_value`. Values of all form field types (except signatures) are now supported. A new attribute :attr:`Annot.widget_choices` contains the selectable values of listboxes and comboboxes. All these attributes now contain ``None`` if no value is present.

Changes in Version 1.13.4
--------------------------
* :meth:`Document.convertToPDF` now supports page ranges, reverted page sequences and page rotation. If the document already is a PDF, an exception is raised.
* Fixed a bug (introduced with v1.13.0) that prevented :meth:`Page.insertImage` for transparent images.

Changes in Version 1.13.3
--------------------------
Introduces a way to convert **any MuPDF supported document** to a PDF. If you ever wanted PDF versions of your XPS, EPUB, CBZ or FB2 files -- here is a way to do this.

* :meth:`Document.convertToPDF` returns a Python ``bytes`` object in PDF format. Can be opened like normal in PyMuPDF, or be written to disk with the ``".pdf"`` extension.

Changes in Version 1.13.2
--------------------------
The major enhancement is PDF form field support. Form fields are annotations of type ``(19, 'Widget')``. There is a new document method to check whether a PDF is a form. The :ref:`Annot` class has new properties describing field details.

* :attr:`Document.isFormPDF` is true if object type ``/AcroForm`` and at least one form field exists.
* :attr:`Annot.widget_type`, :attr:`Annot.widget_text` and :attr:`Annot.widget_name` contain the details of a form field (i.e. a "Widget" annotation).

Changes in Version 1.13.1
--------------------------
* :meth:`TextPage.extractDICT` is a new method to extract the contents of a document page (text and images). All document types are supported as with the other :ref:`TextPage` ``extract*()`` methods. The returned object is a dictionary of nested lists and other dictionaries, and **exactly equal** to the JSON-deserialization of the old :meth:`TextPage.extractJSON`. The difference is that the result is created directly -- no JSON module is used. Because the user needs no JSON module to interpet the information, it should be easier to use, and also have a better performance, because it contains images in their original **binary format** -- they need not be base64-decoded.
* :meth:`Page.getText` correspondingly supports the new parameter value ``"dict"`` to invoke the above method.
* :meth:`TextPage.extractJSON` (resp. ``Page.getText("json")``) is still supported for convenience, but its use is expected to decline.

Changes in Version 1.13.0
--------------------------
This version is based on MuPDF v1.13.0. This release is "primarily a bug fix release".

In PyMuPDF, we are also doing some bug fixes while introducing minor enhancements. There only very minimal changes to the user's API.

* :ref:`Document` construction is more flexible: the new ``filetype`` parameter allows setting the document type. If specified, any extension in the filename will be ignored. More completely addresses `issue #156 <https://github.com/rk700/PyMuPDF/issues/156>`_. As part of this, the documentation has been reworked.

* Changes to :ref:`Pixmap` constructors:
    - Colorspace conversion no longer allows dropping the alpha channel: source and target **alpha will now always be the same**. We have seen exceptions and even interpreter crashes when using ``alpha = 0``.
    - As a replacement, the simple pixmap copy lets you choose the target alpha.

* :meth:`Document.save` again offers the full garbage collection range 0 thru 4. Because of a bug in XREF maintenance, we had to temporarily enforce ``garbage > 1``. Finally resolves `issue #148 <https://github.com/rk700/PyMuPDF/issues/148>`_.

* :meth:`Document.save` now offers to "prettify" PDF source via an additional argument.
* :meth:`Page.insertImage` has the additional ``stream`` \-parameter, specifying a memory area holding an image.

* Issue with garbled PNGs on Linux systems has been resolved (`"Problem writing PNG" #133) <https://github.com/rk700/PyMuPDF/issues/133>`_.


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
This version is based on and requires MuPDF v1.12.0. The new MuPDF version contains quite a number of changes -- most of them around text extraction. Some of the changes impact the programmer's API.

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

* New class ``Shape``. It facilitates and extends the creation of image shapes on PDF pages. It contains multiple methods for creating elementary shapes like lines, rectangles or circles, which can be combined into more complex ones and be given common properties like line width or colors. Combined shapes are handled as a unit and e.g. be "morphed" together. The class can accumulate multiple complex shapes and put them all in the page's foreground or background -- thus also reducing the number of updates to the page's ``/Contents`` object.

* All ``Page`` draw methods now use the new ``Shape`` class.

* Text insertion methods ``insertText()`` and ``insertTextBox()`` now support morphing in addition to text rotation. They have become part of the ``Shape`` class and thus allow text to be freely combined with graphics.

* A new ``Pixmap`` constructor allows creating pixmap copies with an added alpha channel. A new method also allows directly manipulating alpha values.

* Binary algebraic operations with geometry objects (matrices, rectangles and points) now generally also support lists or tuples as the second operand. You can add a tuple ``(x, y)`` of numbers to a :ref:`Point`. In this context, such sequences are called "point-like" (resp. matrix-like, rectangle-like).

* Geometry objects now fully support in-place operators. For example, ``p /= m`` replaces point p with ``p * 1/m`` for a number, or ``p * ~m`` for a matrix-like object ``m``. Similarly, if ``r`` is a rectangle, then ``r |= (3, 4)`` is the new rectangle that also includes ``fitz.Point(3, 4)``, and ``r &= (1, 2, 3, 4)`` is its intersection with ``fitz.Rect(1, 2, 3, 4)``.

Changes in Version 1.11.0
--------------------------------
This version is based on and requires MuPDF v1.11.

Though MuPDF has declared it as being mostly a bug fix version, one major new feature is indeed contained: support of embedded files -- also called portfolios or collections. We have extended PyMuPDF functionality to embrace this up to an extent just a little beyond the ``mutool`` utility as follows.

* The ``Document`` class now support embedded files with several new methods and one new property:

    - ``embeddedFileInfo()`` returns metadata information about an entry in the list of embedded files. This is more than ``mutool`` currently provides: it shows all the information that was used to embed the file (not just the entry's name).
    - ``embeddedFileGet()`` retrieves the (decompressed) content of an entry into a ``bytes`` buffer.
    - ``embeddedFileAdd(...)`` inserts new content into the PDF portfolio. We (in contrast to ``mutool``) **restrict** this to entries with a **new name** (no duplicate names allowed).
    - ``embeddedFileDel(...)`` deletes an entry from the portfolio (function not offered in MuPDF).
    - ``embeddedFileSetInfo()`` -- changes filename or description of an embedded file.
    - ``embeddedFileCount`` -- contains the number of embedded files.

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
MuPDF version 1.10 has a significant impact on our bindings. Some of the changes also affect the API -- in other words, **you** as a PyMuPDF user.

* Link destination information has been reduced. Several properties of the ``linkDest`` class no longer contain valuable information. In fact, this class as a whole has been deleted from MuPDF's library and we in PyMuPDF only maintain it to provide compatibilty to existing code.

* In an effort to minimize memory requirements, several improvements have been built into MuPDF v1.10:

    - A new ``config.h`` file can be used to de-select unwanted features in the C base code. Using this feature we have been able to reduce the size of our binary ``_fitz.o`` / ``_fitz.pyd`` by about 50% (from 9 MB to 4.5 MB). When UPX-ing this, the size goes even further down to a very handy 2.3 MB.

    - The alpha (transparency) channel for pixmaps is now optional. Letting alpha default to ``False`` significantly reduces pixmap sizes (by 20% -- CMYK, 25% -- RGB, 50% -- GRAY). Many ``Pixmap`` constructors therefore now accept an ``alpha`` boolean to control inclusion of this channel. Other pixmap constructors (e.g. those for file and image input) create pixmaps with no alpha alltogether. On the downside, save methods for pixmaps no longer accept a ``savealpha`` option: this channel will always be saved when present. To minimize code breaks, we have left this parameter in the call patterns -- it will just be ignored.

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

  Type of memory area ``stream`` may be ``bytes`` or ``bytearray``. Thus, e.g. ``area = open("file.pdf", "rb").read()`` may be used directly (without first converting it to bytearray).
* New method ``Document.insertPDF()`` (PDFs only) inserts a range of pages from another PDF.
* ``Document`` objects doc now support the ``len()`` function: ``len(doc) == doc.pageCount``.
* New method ``Document.getPageImageList()`` creates a list of images used on a page.
* New method ``Document.getPageFontList()`` creates a list of fonts referenced by a page.
* New pixmap constructor ``fitz.Pixmap(doc, xref)`` creates a pixmap based on an opened PDF document and an XREF number of the image.
* New pixmap constructor ``fitz.Pixmap(cspace, spix)`` creates a pixmap as a copy of another one ``spix`` with the colorspace converted to ``cspace``. This works for all colorspace combinations.
* Pixmap constructor ``fitz.Pixmap(colorspace, width, height, samples)`` now allows ``samples`` to also be ``bytes``, not only ``bytearray``.


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
