.. _TextPage:

================
TextPage
================

This class represents text and images shown on a document page. All MuPDF document types are supported.

============================== ==============================================
**Method**                     **Short Description**
============================== ==============================================
:meth:`TextPage.extractText`   Extract the page's plain text
:meth:`TextPage.extractTEXT`   synonym of previous
:meth:`TextPage.extractHTML`   Extract the page's content in HTML format
:meth:`TextPage.extractJSON`   Extract the page's content in JSON format
:meth:`TextPage.extractXHTML`  Extract the page's content in XHTML format
:meth:`TextPage.extractXML`    Extract the page's text in XML format
:meth:`TextPage.extractDICT`   Extract the page's content in *dict* format
:meth:`TextPage.search`        Search for a string in the page
============================== ==============================================

**Class API**

.. class:: TextPage

   .. method:: extractText

   .. method:: extractTEXT

      Extract all text from a ``TextPage`` object. Returns a string of the page's complete text. The text is UTF-8 unicode and in the same sequence as specified at the time of document creation.

      :rtype: str

   .. method:: extractHTML

      Extract all text and images in HTML format. This version contains complete formatting and positioning information. Images are included (encoded as base64 strings). You need an HTML package to interpret the output in Python. Your internet browser should be able to adequately display this information, but see :ref:`HTMLQuality`.

      :rtype: str

   .. method:: extractDICT

      Extract content as a Python dictionary. Provides same information detail as HTML. See below for the structure.

      :rtype: dict

   .. method:: extractJSON

      Extract content as a string in JSON format. Created by applying ``json.dumps()`` to the output of :meth:`extractDICT`. Any images are base64 encoded. You will probably use this method ever only for outputting the result in some text file or the like.

      :rtype: str

   .. method:: extractXHTML

      Extract all text in XHTML format. Text information detail is comparable with :meth:`extractTEXT`, but also contains images (base64 encoded). This method makes no attempt to re-create the original visual appearance.

      :rtype: str

   .. method:: extractXML

      Extract all text in XML format. This contains complete formatting information about every single character on the page: font, size, line, paragraph, location, etc. Contains no images. You need an XML package to interpret the output in Python.

      :rtype: str

   .. method:: search(string, hit_max = 16)

      Search for ``string``.

      :arg str string: The string to search for.
      :arg int hit_max: Maximum number of expected hits (default 16).
      :rtype: list
      :returns: a list of :ref:`Rect` objects (without transformation), each surrounding a found ``string`` occurrence.

   .. note:: All of the above can be achieved by using the appropriate :meth:`Page.getText` and :meth:`Page.searchFor` methods. Also see further down and in the :ref:`Page` chapter for examples on how to create a valid file format by adding respective headers and trailers.

Structure of :meth:`extractDICT` / :meth:`extractJSON`:
-----------------------------------------------------------------------------
Both methods return equivalent information: :meth:`extractJSON` is a string that must be interpreted using a JSON module for use in Python. You will probably use :meth:`extractDICT` for this.

:meth:`extractJSON` may be useful for text file output and similar. This string is created by applying ``json.dumps()`` to :meth:`extractDICT` (with a plugin encoding binary content as base64 strings).

:meth:`extractDICT` has the following structure.

Page Dictionary
~~~~~~~~~~~~~~~~~
=============== ============================================
Key             Value
=============== ============================================
width           page width in pixels *(float)*
height          page height in pixels *(float)*
blocks          *list* of blocks (*dict*)
=============== ============================================

Block Dictionaries
~~~~~~~~~~~~~~~~~~
Blocks come in two different formats: **image blocks** and **text blocks**.

**Image block:**

=============== ===============================================================
Key             Value
=============== ===============================================================
type            1 = image *(int)*
bbox            block / image rectangle, formatted as ``list(fitz.Rect)``
ext             image type *(str)*, as its file extension, see below
width           original image width *(float)*
height          original image height *(float)*
image           image content *(bytearray)*, may be empty if not supported!
=============== ===============================================================

Possible values of key ``"ext"`` are ``"bmp"``, ``"gif"``, ``"jpeg"``, ``"jpx"`` (JPEG 2000), ``"jxr"`` (JPEG XR), ``"png"``, ``"pnm"``, and ``"tiff"``.


**Text block:**

=============== ==================================================
Key             Value
=============== ==================================================
type            0 = text *(int)*
bbox            block rectangle, formatted as ``list(fitz.Rect)``
lines           *list* of text lines (*dict*)
=============== ==================================================

Line Dictionary
~~~~~~~~~~~~~~~~~

=============== =====================================================
Key             Value
=============== =====================================================
bbox            line rectangle, formatted as ``list(fitz.Rect)``
wmode           writing mode *(int)*: 0 = horizontal, 1 = vertical
dir             writing direction *(list of floats)*: ``[x, y]``
spans           *list* of spans (*dict*)
=============== =====================================================

The value of key ``"dir"`` should be interpreted as follows:

* ``x``: positive = "left-right", negative = "right-left", 0 = neither
* ``y``: positive = "top-bottom", negative = "bottom-top", 0 = neither

The values indicate the "relative writing speed" in each direction, such that x\ :sup:`2` + y\ :sup:`2` = 1. In other words ``dir = [cos(beta), sin(beta)]`` is a unit vector, where ``beta`` is the writing angle relative to the horizontal.

Span Dictionary
~~~~~~~~~~~~~~~~
Spans contain the actual text. In contrast to MuPDF versions prior to v1.12, a span no longer includes positioning information. Therefore, to reconstruct the text of a line, the text pieces of all spans must be concatenated. A span since v1.12 also contains font information. A line contains more than one span only, when the font or its attributes of the text are changing.

=============== =====================================================
Key             Value
=============== =====================================================
font            font name *(str)*
size            font size *(float)*
flags           font characteristics *(int)*
text            text *(str)*
=============== =====================================================

``flags`` is an integer encoding bools of font properties:

* bit 0: superscripted
* bit 1: italic
* bit 2: serifed
* bit 3: monospaced
* bit 4: bold
