
================================================
Appendix 4: Assorted Technical Information
================================================

.. _Base-14-Fonts:

PDF Base 14 Fonts
---------------------
The following 14 builtin font names must be supported by every PDF aplication. They are available as the Python list ``fitz.Base14_Fonts``:

* Courier
* Courier-Oblique
* Courier-Bold
* Courier-BoldOblique
* Helvetica
* Helvetica-Oblique
* Helvetica-Bold
* Helvetica-BoldOblique
* Times-Roman
* Times-Bold
* Times-Italic
* Times-BoldItalic
* Symbol
* ZapfDingbats

------------

.. _AdobeManual:

Adobe PDF Reference 1.7
---------------------------

This PDF Reference manual published by Adobe is frequently quoted throughout this documentation. It can be viewed and downloaded from here: http://www.adobe.com/content/dam/Adobe/en/devnet/acrobat/pdfs/pdf_reference_1-7.pdf.

------------

.. _ReferenialIntegrity:

Ensuring Consistency of Important Objects in PyMuPDF
------------------------------------------------------------
PyMuPDF is a Python binding for the C library MuPDF. While a lot of effort has been invested by MuPDF's creators to approximate some sort of an object-oriented behavior, they certainly could not overcome basic shortcomings of the C language in that respect.

Python on the other hand implements the OO-model in a very clean way. The interface code between PyMuPDF and MuPDF consists of two basic files: ``fitz.py`` and ``fitz_wrap.c``. They are created by the excellent SWIG tool for each new version.

When you use one of PyMuPDF's objects or methods, this will result in excution of some code in ``fitz.py``, which in turn will call some C code compiled with ``fitz_wrap.c``.

Because SWIG goes a long way to keep the Python and the C level in sync, everything works fine, if a certain set of rules is being strictly followed. For example: **never access** a :ref:`Page` object, after you have closed (or deleted or set to ``None``) the owning :ref:`Document`. Or, less obvious: **never access** a page or any of its children (links or annotations) after you have executed one of the document methods ``select()``, ``deletePage()``, ``insertPage()`` ... and more.

But just no longer accessing invalidated objects is actually not enough: They should rather be actively deleted entirely, to also free C-level resources.

The reason for these rules lies in the fact that there is a hierachical 2-level one-to-many relationship between a document and its pages and between a page and its links and annotations. To maintain a consistent situation, any of the above actions must lead to a complete reset - in **Python and, synchronously, in C**.

SWIG cannot know about this and consequently does not do it.

The required logic has therefore been built into PyMuPDF itself in the following way.

1. If a page "loses" its owning document or is being deleted itself, all of its currently existing annotations and links will be made unusable in Python, and their C-level counterparts will be deleted and deallocated.

2. If a document is closed (or deleted or set to ``None``) or if its structure has changed, then similarly all currently existing pages and their children will be made unusable, and corresponding C-level deletions will take place. "Structure changes" include methods like ``select()``, ``delePage()``, ``insertPage()``, ``insertPDF()`` and so on: all of these will result in a cascade of object deletions.

The programmer will normally not realize any of this. If he, however, tries to access invalidated objects, exceptions will be raised.

Invalidated objects cannot be directly deleted as with Python statements like ``del page`` or ``page = None``, etc. Instead, their ``__del__`` method must be invoked.

All pages, links and annotations have the property ``parent``, which points to the owning object. This is the property that can be checked on the application level: if ``obj.parent == None`` then the object's parent is gone, and any reference to its properties or methods will raise an exception informing about this "orphaned" state.

A sample session:

>>> page = doc[n]
>>> annot = page.firstAnnot
>>> annot.type                    # everything works fine
[5, 'Circle']
>>> page = None                   # this turns 'annot' into an orphan
>>> annot.type
<... omitted lines ...>
RuntimeError: orphaned object: parent is None
>>>
>>> # same happens, if you do this:
>>> annot = doc[n].firstAnnot     # deletes the page again immediately!
>>> annot.type                    # so, 'annot' is 'born' orphaned
<... omitted lines ...>
RuntimeError: orphaned object: parent is None

This shows the cascading effect:

>>> doc = fitz.open("some.pdf")
>>> page = doc[n]
>>> annot = page.firstAnnot
>>> page.rect
fitz.Rect(0.0, 0.0, 595.0, 842.0)
>>> annot.type
[5, 'Circle']
>>> del doc                       # or doc = None or doc.close()
>>> page.rect
<... omitted lines ...>
RuntimeError: orphaned object: parent is None
>>> annot.type
<... omitted lines ...>
RuntimeError: orphaned object: parent is None

.. note:: Objects outside the above relationship are not included in this mechanism. If you e.g. created a table of contents by ``toc = doc.getToC()``, and later close or change the document, then this cannot and does not change variable ``toc`` in any way. It is your responsibility to refresh such variables as required.

------------

.. _FormXObject:

Design of Method :meth:`Page.showPDFpage`
--------------------------------------------

Purpose and Capabilities
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The method displays an image of a ("source") page of another PDF document within a specified rectangle of the current ("containing") page.

* **In contrast** to :meth:`Page.insertImage`, this display is vector-based and hence remains accurate across zooming levels.
* **Just like** :meth:`Page.insertImage`, the size of the display is adjusted to the given rectangle.

The following variations of the display are currently supported:

* Bool parameter ``keep_proportion`` controls whether to maintain the width-height-ratio (default) or not.
* Rectangle parameter ``clip`` controls which part of the source page to show, and hence can be used for cropping.  Default is the full page.
* Bool parameter ``overlay`` controls whether to put the image on top (foreground, default) of current page content or not (background).

Use cases include (but are not limited to) the following:

1. "Stamp" a series of pages of the current document with the same image, like a company logo or a watermark.
2. Combine arbitrary input pages into one output page to support “booklet” or double-sided printing (known as "4-up", "n-up").
3. Split up (large) input pages into several arbitrary pieces. This is also called “posterization”, because you e.g. can split an A4 page horizontally and vertically, print the 4 pieces as A4 pages on a printer which cannot output larger paper, and end up with an A2 version of your original page.

Technical Implementation
~~~~~~~~~~~~~~~~~~~~~~~~~

This is done using PDF **form XObjects**, see section 4.9 on page 355 of :ref:`AdobeManual`. On execution of a ``Page.showPDFpage(rect, src, pno, ...)``, the following things happen:

    1. The ``/Resources`` and ``/Contents`` objects of page ``pno`` in document ``src`` are copied over to the current document, jointly creating a **new form XObject** with the following properties. The PDF ``xref`` number of this object is returned by the method.

        a. ``/BBox`` equals ``/Mediabox`` of the source page
        b. ``/Matrix`` equals the identity matrix ``[1 0 0 1 0 0]``
        c. ``/Resources`` equals that of the source page. This involves a “deep-copy” of hierarchically nested other objects (including fonts, images, etc.). The complexity involved here is covered by MuPDF’s grafting [#f1]_ technique functions.
        d. This is a stream object type, and its stream is exactly equal to the ``/Contents`` object of the source (if the source has multiple such objects, these are first concatenated and stored as one new stream into the new form XObject).

    2. A **second form XObject** is then created which the containing page uses to invoke the previous one. This object has the following properties:

        a. ``/BBox`` equals the ``/CropBox`` of the source page (or ``clip``, if specified).
        b. ``/Matrix`` represents the mapping of ``/BBox`` to the display rectangle of the containing page (parameter 1 of ``showPDFpage``).
        c. ``/XObject`` references the previous XObject via the fixed name ``fullpage``.
        d. The stream of this object contains exactly one fixed statement: ``/fullpage Do``.

    3. The ``/Resources`` and ``/Contents`` objects of the invoking page are now modified as follows.
    
        a. Add an entry to the ``/XObject`` dictionary of ``/Resources`` with the name ``fitz-xref-uid``, which is unique for this page. Uniqueness is required because the same source might be displayed more than once on the containing page. ``xref`` is the PDF cross reference number of XObject 1, and ``uid`` is a globally unique [#f2]_ integer provided by the MuPDF library.
        b. Depending on ``overlay``, prepend or append the following statement to the contents object: ``/fitz-xref-uid Do``.

    4. Return ``xref`` to the caller.

Observe the following guideline for optimum results:

Unfortunately, as per this writing, PDF garbage collection (a feature of the underlying C-library MuPDF, and an optional argument of :meth:`Document.save`) does not detect identical form XObjects. Process steps 1 therefore **irrevocably** leads to a **new XObject** for every source page, if no precautions are taken. And this may be very large. The second XObject is very small, specific to the containing page, and therefore different each time. To avoid excess source page copies, use parameter ``reuse_xref = xref`` with the ``xref`` value returned by previous executions. When the method detects ``reuse_xref > 0``, it will not create XObject 1 again, but instead point to the ``xref`` \erenced object.

If, in a second PyMuPDF session, a target PDF is updated again with the same source PDF page, the above mechanism cannot work and duplicates of XObject 1 will be created.

.. rubric:: Footnotes

.. [#f1] MuPDF supports "deep-copying" objects between PDF documents. To avoid duplicate data in the target, it uses "graftmaps", a form of scratchpad: for each object to be copied, its xref number is looked up in the graftmap. If found, copying is skipped. Otherwise, the xref is recorded and the copy takes place. PyMuPDF makes use of this technique in two places so far: :meth:`Document.insertPDF` and :meth:`Page.showPDFpage`. This process is fast and very efficient, as our tests have shown, because it prevents multiple copies of typically large and frequently referenced data, like images and also fonts. Whether the target document originally had identical data is however not checked by the grafting technique. Therefore, using save-option ``garbage = 4`` may still be a reasonable consideration, when copying to a non-empty target.

.. [#f2] Arguably, ``uid`` alone would suffice to ensure uniqueness: this integer is maintained threadsafe as part of the global context. However, if a PDF is updated again later, ``uid`` would start over from 1. A reference name like ``/fitz-uid`` would therefore no longer be guarantied unique if more objects are shown on the containing page. Theoretically, the uniqueness of ``/fitz-xref-uid`` could also break, when PDF garbage collection leads to renumbering the PDF objects ... but chances for this seem tolerably low. What would be the effect of a non-uniqueness? If a page contains several identical XObject references, intentionally pointing to different XObjects, unexpected behaviour will result. Which in turn can only happen if garbage collection (1) changes the original ``xref`` and (2) a new :meth:`Page.showPDFpage` happens to generate an XObject with the now-free xref number ...