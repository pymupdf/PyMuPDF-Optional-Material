.. _TextPage:

================
TextPage
================

``TextPage`` represents the text of a page.

============================== ==============================================
**Method**                     **Short Description**
============================== ==============================================
:meth:`TextPage.extractText`   Extract the page's plain text
:meth:`TextPage.extractTEXT`   synonym of previous
:meth:`TextPage.extractHTML`   Extract the page's text in HTML format
:meth:`TextPage.extractJSON`   Extract the page's text in JSON format
:meth:`TextPage.extractXHTML`  Extract the page's text in XHTML format
:meth:`TextPage.extractXML`    Extract the page's text in XML format
:meth:`TextPage.search`        Search for a string in the page
============================== ==============================================

**Class API**

.. class:: TextPage

   .. method:: extractText

   .. method:: extractTEXT

      Extract the text from a ``TextPage`` object. Returns a string of the page's complete text. The text is UTF-8 unicode and in the same sequence as the PDF creator specified it. If this looks awkward for your document, consider using a program that re-arranges the text according to a more familiar layout, e.g. `PDF2TextJS.py <https://github.com/rk700/PyMuPDF/blob/master/examples/PDF2TextJS.py>`_ in the examples directory. Or use another extraction method which also provides text position information like :meth:`TextPage.extractHTML`, :meth:`TextPage.extractXML`, or :meth:`Page.extractTextList`.

      :rtype: str

   .. method:: extractHTML

      Extract all text and images in HTML format. This version contains complete formatting and positioning information on line level. Images will be included as base64 strings. You need a HTML package to interpret the output. Also see :ref:`HTMLQuality`.

      :rtype: str

   .. method:: extractJSON

      Extract all text in JSON format. Provides same information detail as HTML (including images). You need a JSON module to interpret the output. The result will be nested Python dictionaries and lists. See below for the structure.

      :rtype: str

   .. method:: extractXHTML()

      Extract all text in XHTML format. Text information detail is comparable with ``extractTEXT``, but also contains images. This method makes no attempt to re-create the original visual appearance.

      :rtype: str

   .. method:: extractXML()

      Extract all text in XML format. This contains complete formatting information about every single character on the page: font, size, line, paragraph, location, etc. Contains no images.

      :rtype: str

   .. method:: search(string, hit_max = 16)

      Search for ``string``.

      :arg str string: The string to search for.
      :arg int hit_max: Maximum number of expected hits (default 16).
      :rtype: list
      :returns: a list of :ref:`Rect` objects (without transformation), each surrounding a found ``string`` occurrence.

   .. note:: All of the above can be achieved by using the appropriate :meth:`Page.getText` and :meth:`Page.searchFor` methods. Also see further down and in the :ref:`Page` chapter for examples on how to create a valid file format by adding respective headers and trailers.

Structure of :meth:`TextPage.extractJSON`
------------------------------------------------
A text page in JSON format is a nested object consisting of dictionaries and lists.

Page Dictionary
~~~~~~~~~~~~~~~~~
=============== ============================================
Key             Value
=============== ============================================
width           page width in pixels *(float)*
height          page height in pixels *(float)*
blocks          list of blocks *(list)*
=============== ============================================

Block Dictionaries
~~~~~~~~~~~~~~~~~~
Blocks come in two types with a different structure: image blocks and text blocks.

**Image block:**

=============== ===================================================
Key             Value
=============== ===================================================
type            1 = image *(int)*
bbox            block / image rectangle, formatted as ``list(fitz.Rect)``
imgtype         image type *(int)*, see list below
width           original image width *(float)*
height          original image height *(float)*
image           image content *(base64 str)*, may be ``None``
=============== ===================================================

Image type values:

* 0 (unknown): image type could not be determined and is provided as PNG if possible
* 1 (raw): uncompressed samples
* 2 (FAX)
* 3 (flate)
* 4 (LZW)
* 5 (RLD)
* 6 (BMP)
* 7 (GIF)
* 8 (JPEG)
* 9 (JPX)
* 10 (JXR)
* 11 (PNG)
* 12 (PNM)
* 13 (TIFF)

**Text block:**

=============== ==================================================
Key             Value
=============== ==================================================
type            0 = text *(int)*
bbox            block rectangle, formatted as ``list(fitz.Rect)``
lines           list of text lines *(list)*
=============== ==================================================

Line Dictionary
~~~~~~~~~~~~~~~~~

=============== =====================================================
Key             Value
=============== =====================================================
bbox            line rectangle, formatted as ``list(fitz.Rect)``
wmode           writing mode *(int)*: 0 = horizontal, 1 = vertical
dir             writing direction *(tuple of floats)*: ``[x, y]``
spans           list of spans *(list)*
=============== =====================================================

The entries of writing direction ``dir`` should be interpreted as follows:

* ``x``: positive = "left-right", negative = "right-left", 0 = neither
* ``y``: positive = "top-bottom", negative = "bottom-top", 0 = neither

The values indicate the "relative writing speed" in each direction, such that x\ :sup:`2` + y\ :sup:`2` = 1. In other words ``dir = [cos(beta), sin(beta)]`` where ``beta`` is the writing angle relative to the horizontal.

Span Dictionary
~~~~~~~~~~~~~~~~
Spans contain the actual text. In contrast to MuPDF versions up to 1.11, a span no longer includes positioning information. Therefore, to reconstruct the text a line, span text pieces must be concatenated. A span now contains font information. A line contains more than one span only, when any changes of the font or its attributes occur.

=============== =====================================================
Key             Value
=============== =====================================================
font            name of font *(str)*
size            font size *(float)*
flags           font characteristics *(int)*
text            text *(str)*
=============== =====================================================

``flags`` is a set of bools describing the font:

* bit 0: superscripted text
* bit 1: italic
* bit 2: serifed
* bit 3: monospaced
* bit 4: bold

Full Document Output in JSON Format
-------------------------------------
Converting a document to JSON format requires a little programmer attention. Use the following schema to create a valid (i.e. de-serializable JSON) document:

>>> doc = fitz.open(...)    # maybe any document type!
>>> jsonfile = open("document.json", "w")
>>> pno = 0
>>> jsonfile.write(fitz.ConversionHeader("json", filename = doc.name))
>>> for page in doc:
        if pno > 0:
            jsonfile.write(",\n")    # comma needed between pages!
        jsonfile.write(page.getText("json"))
        pno += 1
>>> jsonfile.write(fitz.ConversionTrailer("json"))
>>> jsonfile.close()

The document level dictionary then looks like so:

=============== =====================================================
Key             Value
=============== =====================================================
document        specified filename *(str)*
pages           list of pages *(list)*
=============== =====================================================
