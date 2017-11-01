
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

.. _AdobeManual:

Adobe PDF Reference 1.7
---------------------------

This PDF Reference manual published by Adobe is frequently quoted throughout this documentation. It can be viewed and downloaded from here: http://www.adobe.com/content/dam/Adobe/en/devnet/acrobat/pdfs/pdf_reference_1-7.pdf.

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