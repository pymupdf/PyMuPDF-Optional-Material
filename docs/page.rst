.. _Page:

================
Page
================

Class representing a document page. A page object is created by :meth:`Document.loadPage` or, equivalently, via indexing the document like ``doc[n]`` - it has no independent constructor.

There is a parent-child relationship between a document and its pages. If the document is closed or deleted, all page objects (and their respective children, too) in existence will become unusable. If a page property or method is being used, an exception is raised saying that the page object is "orphaned".

Several page methods have a :ref:`Document` counterpart for convenience. At the end of this chapter you will find a synopsis.

Adding Page Content
-------------------
This is available for PDF documents only. There are basically two groups of methods:

1. Methods making **permanent** changes. This group contains ``insertText()``, ``insertTextbox()`` and all ``draw*()`` methods. They provide "stand-alone", shortcut versions for the same-named methods of the :ref:`Shape` class. For detailed descriptions have a look in that chapter. Some remarks on the relationship between the :ref:`Page` and :ref:`Shape` methods:

  * In contrast to :ref:`Shape`, the results of page methods are not interconnected: they do not share properties like colors, line width / dashing, morphing, etc.
  * Each page ``draw*()`` method invokes a :meth:`Shape.finish` and then a :meth:`Shape.commit` and consequently accepts the combined arguments of both these methods.
  * Text insertion methods (``insertText()`` and ``insertTextbox()``) do not need :meth:`Shape.finish` and therefore only invoke :meth:`Shape.commit`.

2. Methods adding **annotations**. Annotations can be added, modified and deleted without necessarily having full document permissions. Their effect is **not permanent** in the sense, that manipulating them does not require to rebuild the document. **Adding** and **deleting** annotations are page methods. **Changing** existing annotations is possible via methods of the :ref:`Annot` class.

================================ =========================================
**Method / Attribute**           **Short Description**
================================ =========================================
:meth:`Page.addCircleAnnot`      PDF only: add a circle annotation
:meth:`Page.addFileAnnot`        PDF only: add a file attachment annotation
:meth:`Page.addFreetextAnnot`    PDF only: add a text annotation
:meth:`Page.addHighlightAnnot`   PDF only: add a "highlight" annotation
:meth:`Page.addInkAnnot`         PDF only: add an ink annotation
:meth:`Page.addLineAnnot`        PDF only: add a line annotation
:meth:`Page.addPolygonAnnot`     PDF only: add a polygon annotation
:meth:`Page.addPolylineAnnot`    PDF only: add a multi-line annotation
:meth:`Page.addRectAnnot`        PDF only: add a rectangle annotation
:meth:`Page.addStampAnnot`       PDF only: add a "rubber stamp" annotation
:meth:`Page.addSquigglyAnnot`    PDF only: add a "squiggly" annotation
:meth:`Page.addStrikeoutAnnot`   PDF only: add a "strike-out" annotation
:meth:`Page.addTextAnnot`        PDF only: add comment and a note icon
:meth:`Page.addUnderlineAnnot`   PDF only: add an "underline" annotation
:meth:`Page.addWidget`           PDF only: add a PDF Form field
:meth:`Page.bound`               rectangle of the page
:meth:`Page.deleteAnnot`         PDF only: delete an annotation
:meth:`Page.deleteLink`          PDF only: delete a link
:meth:`Page.drawBezier`          PDF only: draw a cubic Bézier curve
:meth:`Page.drawCircle`          PDF only: draw a circle
:meth:`Page.drawCurve`           PDF only: draw a special Bézier curve
:meth:`Page.drawLine`            PDF only: draw a line
:meth:`Page.drawOval`            PDF only: draw an oval / ellipse
:meth:`Page.drawPolyline`        PDF only: connect a point sequence
:meth:`Page.drawRect`            PDF only: draw a rectangle
:meth:`Page.drawSector`          PDF only: draw a circular sector
:meth:`Page.drawSquiggle`        PDF only: draw a squiggly line
:meth:`Page.drawZigzag`          PDF only: draw a zig-zagged line
:meth:`Page.getFontList`         PDF only: get list of used fonts
:meth:`Page.getImageList`        PDF only: get list of used images
:meth:`Page.getLinks`            get all links
:meth:`Page.getPixmap`           create a :ref:`Pixmap`
:meth:`Page.getSVGimage`         create a page image in SVG format
:meth:`Page.getText`             extract the page's text
:meth:`Page.insertFont`          PDF only: insert a font for use by the page
:meth:`Page.insertImage`         PDF only: insert an image
:meth:`Page.insertLink`          PDF only: insert a new link
:meth:`Page.insertText`          PDF only: insert text
:meth:`Page.insertTextbox`       PDF only: insert a text box
:meth:`Page.loadLinks`           return the first link on a page
:meth:`Page.newShape`            PDF only: start a new :ref:`Shape`
:meth:`Page.searchFor`           search for a string
:meth:`Page.setCropBox`          PDF only: modify the visible page
:meth:`Page.setRotation`         PDF only: set page rotation
:meth:`Page.showPDFpage`         PDF only: display PDF page image
:meth:`Page.updateLink`          PDF only: modify a link
:attr:`Page.CropBox`             the page's /CropBox
:attr:`Page.CropBoxPosition`     displacement of the /CropBox
:attr:`Page.firstAnnot`          first :ref:`Annot` on the page
:attr:`Page.firstLink`           first :ref:`Link` on the page
:attr:`Page.MediaBox`            the page's /MediaBox
:attr:`Page.MediaBoxSize`        bottom-right point of /MediaBox
:attr:`Page.number`              page number
:attr:`Page.parent`              owning document object
:attr:`Page.rect`                rectangle (mediabox) of the page
:attr:`Page.rotation`            PDF only: page rotation
:attr:`Page.xref`                PDF :data:`xref`
================================ =========================================

**Class API**

.. class:: Page

   .. method:: bound()

      Determine the rectangle (before transformation) of the page. Same as property :attr:`Page.rect` below. For PDF documents this **usually** also coincides with objects ``/MediaBox`` and ``/CropBox``, but not always. The best description hence is probably "``/CropBox``, transformed such that top-left coordinates are (0, 0)". Also see attributes :attr:`Page.CropBox` and :attr:`Page.MediaBox`.

      :rtype: :ref:`Rect`

   .. method:: addTextAnnot(point, text)

      PDF only: Add a comment icon ("sticky note") with accompanying text.

      :arg point-like point: the top left point of a 18 x 18 rectangle containing the MuPDF-provided "note" icon.

      :arg str text: the commentary text. This will be shown on double clicking or hovering over the icon. May contain any Latin characters.

      :rtype: :ref:`Annot`
      :returns: the created annotation. Use methods of :ref:`Annot` to make any changes.

      .. image:: img-sticky-note.png
         :scale: 70

   .. index::
      pair: rect; Page.addFreetextAnnot args
      pair: fontsize; Page.addFreetextAnnot args
      pair: fontname; Page.addFreetextAnnot args
      pair: color; Page.addFreetextAnnot args
      pair: rotate; Page.addFreetextAnnot args

   .. method:: addFreetextAnnot(rect, text, fontsize = 12, fontname = "Helvetica", color = (0,0,0), rotate = 0)

      PDF only: Add text in a given rectangle.

      :arg rect-like rect: the rectangle into which the text should be inserted.

      :arg str text: the text. May contain any Latin characters.
      :arg float fontsize: the font size. Default is 12.
      :arg str fontname: the font name. Default is "Helvetica". Accepted alternatives are "Courier", "Times-Roman", "ZapfDingbats" and "Symbol". The name may be abbreviated to the first two characters, "Co" for "Courier". Lower case is also accepted.
      :arg sequence color: the text and rectangle border color. Default is black. Text is automatically wrapped to a new line at box width. Lines not fitting to the box will be invisible.
      :arg int rotate: the text orientation. Accepted values are 0, 90, 270, else zero is used.

      :rtype: :ref:`Annot`
      :returns: the created annotation. The text and rectangle border will be drawn in the same specified color. Rectangle background is white. These properties can only be changed using special parameters of :meth:`Annot.update`. Changeable properties are text color, box interior and border color and text font size.

   .. method:: addFileAnnot(pos, buffer, filename, ufilename = None, desc = None)

      PDF only: Add a file attachment annotation with a "PushPin" icon at the specified location.

      :arg point-like pos: the top-left point of a 18x18 rectangle containing the MuPDF-provided "PushPin" icon.

      :arg bytes/bytearray buffer: the data to be stored (actual file content, calculated data, etc.).
      :arg str filename: the filename.
      :arg str ufilename: the optional PDF unicode filename. Defaults to filename.
      :arg str desc: an optional description of the file. Defaults to filename.

      :rtype: :ref:`Annot`
      :returns: the created annotation. Use methods of :ref:`Annot` to make any changes.

      .. image:: img-fileattach.jpg
         :scale: 70

   .. method:: addInkAnnot(list)

      PDF only: Add a "freehand" scribble annotation.

      :arg sequence list: a list of one or more lists, each containing point-like items. Each item in these sublists is interpreted as a :ref:`Point` through which a connecting line is drawn. Separate sublists thus represent separate drawing lines.

      :rtype: :ref:`Annot`
      :returns: the created annotation in default appearance (black line of width 1). Use annotation methods with a subsequent :meth:`Annot.update` to modify.

   .. method:: addLineAnnot(p1, p2)

      PDF only: Add a line annotation.

      :arg point-like p1: the starting point of the line.

      :arg point-like p2: the end point of the line.

      :rtype: :ref:`Annot`
      :returns: the created annotation. It is drawn with line color black and line width 1. To change, or attach other information (like author, creation date, line properties, colors, line ends, etc.) use methods of :ref:`Annot`. The **rectangle** is automatically created to contain both points, each one surrounded by a circle of radius 3 (= 3 * line width) to make room for any line end symbols. Use methods of :ref:`Annot` to make any changes.

   .. method:: addRectAnnot(rect)

   .. method:: addCircleAnnot(rect)

      PDF only: Add a rectangle, resp. circle annotation.

      :arg rect-like rect: the rectangle in which the circle or rectangle is drawn, must be finite and not empty. If the rectangle is not equal-sided, an ellipse is drawn.

      :rtype: :ref:`Annot`
      :returns: the created annotation. It is drawn with line color black, no fill color and line width 1. Use methods of :ref:`Annot` to make any changes.

   .. method:: addPolylineAnnot(points)

   .. method:: addPolygonAnnot(points)

      PDF only: Add an annotation consisting of lines which connect the given points. A **Polygon's** first and last points are automatically connected, which does not happen for a **PolyLine**. The **rectangle** is automatically created as the smallest rectangle containing the points, each one surrounded by a circle of radius 3 (= 3 * line width). The following shows a 'PolyLine' that has been modified with colors and line ends.

      :arg list points: a list of point-like objects.

      :rtype: :ref:`Annot`
      :returns: the created annotation. It is drawn with line color black, no fill color and line width 1. Use methods of :ref:`Annot` to make any changes to achieve something like this:

      .. image:: img-polyline.png
         :scale: 70

   .. method:: addUnderlineAnnot(rect)

   .. method:: addStrikeoutAnnot(rect)

   .. method:: addSquigglyAnnot(rect)

   .. method:: addHighlightAnnot(rect)

      PDF only: These annotations are used for marking some text that has previously been located via :meth:`searchFor`. Colors are automatically chosen: yellowish for highlighting, red for strike out and blue for underlining. Note that :meth:`searchFor` now supports quadrilaterals as an output option. Correspondingly, the ``rect`` parameter for these annotations may either be rectangles or quadrilaterals.

      :arg rect-like/quad-like rect: the rectangle or quad containing the to-be-marked text.

      :rtype: :ref:`Annot`
      :returns: the created annotation. Per annot type, certain color decisions are being made (e.g. "red" for 'StrikeOut', "yellow" for 'Highlight'). To change them, set the "stroke" color accordingly (:meth:`Annot.setColors`) and then perform an :meth:`Annot.update`.

      .. image:: img-markers.jpg
         :scale: 80

   .. method:: addStampAnnot(rect, stamp = 0)

      PDF only: Add a "rubber stamp" like annotation to e.g. indicate the document's intended use ("DRAFT", "CONFIDENTIAL", etc.).

      :arg rect-like rect: rectangle where to place the annotation.

      :arg int stamp: id number of the stamp text. For available stamps see :ref:`StampIcons`.

      .. note::  The stamp's text (e.g. "APPROVED") and its border line will automatically be sized and put centered in the given rectangle. :attr:`Annot.rect` is automatically calculated to fit and will usually be smaller than this parameter. The appearance can be changed using :meth:`Annot.setOpacity` and by setting the "stroke" color (no "fill" color supported).

      .. image :: img-stampannot.jpg
         :scale: 80

   .. method:: addWidget(widget)

      PDF only: Add a PDF Form field ("widget") to a page. This also **turns the PDF into a Form PDF**. Because of the large amount of different options available for widgets, we have developed a new class :ref:`Widget`, which contains the possible PDF field attributes. It must be used for both, form field creation and updates.

      :arg widget: a :ref:`Widget` object which must have been created upfront.
      :type widget: :ref:`Widget`

      :returns: a widget annotation.

      .. note:: Make sure to use parameter ``clean = True`` when saving the file. This will cause recalculation of the annotations appearance.

   .. method:: deleteAnnot(annot)

      PDF only: Delete the specified annotation from the page and return the next one.

      :arg annot: the annotation to be deleted.
      :type annot: :ref:`Annot`

      :rtype: :ref:`Annot`
      :returns: the annotation following the deleted one.

   .. method:: deleteLink(linkdict)

      PDF only: Delete the specified link from the page. The parameter must be an **original item** of :meth:`getLinks()` (see below). The reason for this is the dictionary's ``"xref"`` key, which identifies the PDF object to be deleted.

      :arg dict linkdict: the link to be deleted.

   .. method:: insertLink(linkdict)

      PDF only: Insert a new link on this page. The parameter must be a dictionary of format as provided by :meth:`getLinks()` (see below).

      :arg dict linkdict: the link to be inserted.

   .. method:: updateLink(linkdict)

      PDF only: Modify the specified link. The parameter must be a (modified) **original item** of :meth:`getLinks()` (see below). The reason for this is the dictionary's ``"xref"`` key, which identifies the PDF object to be changed.

      :arg dict linkdict: the link to be modified.

   .. method:: getLinks()

      Retrieves **all** links of a page.

      :rtype: list
      :returns: A list of dictionaries. The entries are in the order as specified during PDF generation. For a description of the dictionary entries see below. Always use this method if you intend to make changes to the links of a page.

   .. index::
      pair: overlay; Page.insertText args
      pair: fontsize; Page.insertText args
      pair: fontname; Page.insertText args
      pair: fontfile; Page.insertText args
      pair: color; Page.insertText args
      pair: fill; Page.insertText args
      pair: render_mode; Page.insertText args
      pair: border_width; Page.insertText args
      pair: rotate; Page.insertText args
      pair: encoding; Page.insertText args
      pair: morph; Page.insertText args

   .. method:: insertText(point, text, fontsize=11, fontname="helv", fontfile=None, idx=0, color=(0, 0, 0), fill=None, render_mode=0, border_width=1, encoding=TEXT_ENCODING_LATIN, rotate=0, morph=None, overlay=True)

      PDF only: Insert text starting at point-like ``point``. See :meth:`Shape.insertText`.

   .. index::
      pair: overlay; Page.insertTextbox args
      pair: fontsize; Page.insertTextbox args
      pair: fontname; Page.insertTextbox args
      pair: fontfile; Page.insertTextbox args
      pair: color; Page.insertTextbox args
      pair: fill; Page.insertTextbox args
      pair: render_mode; Page.insertTextbox args
      pair: border_width; Page.insertTextbox args
      pair: encoding; Page.insertTextbox args
      pair: expandtabs; Page.insertTextbox args
      pair: align; Page.insertTextbox args
      pair: rotate; Page.insertTextbox args
      pair: morph; Page.insertTextbox args

   .. method:: insertTextbox(rect, buffer, fontsize=11, fontname="helv", fontfile=None, idx=0, color=(0, 0, 0), fill=None, render_mode=0, border_width=1, encoding=TEXT_ENCODING_LATIN, expandtabs=8, align=TEXT_ALIGN_LEFT, charwidths=None, rotate=0, morph=None, overlay=True)

      PDF only: Insert text into the specified rect-like ``rect``. See :meth:`Shape.insertTextbox`.

   .. index::
      pair: overlay; Page.drawLine args
      pair: closePath; Page.drawLine args
      pair: morph; Page.drawLine args
      pair: dashes; Page.drawLine args
      pair: roundCap; Page.drawLine args
      pair: color; Page.drawLine args
      pair: fill; Page.drawLine args
      pair: width; Page.drawLine args

   .. method:: drawLine(p1, p2, color = (0, 0, 0), width = 1, dashes = None, roundCap = True, overlay = True, morph = None)

      PDF only: Draw a line from ``p1`` to ``p2`` (point-likes). See :meth:`Shape.drawLine`.

   .. index::
      pair: overlay; Page.drawZigzag args
      pair: closePath; Page.drawZigzag args
      pair: morph; Page.drawZigzag args
      pair: dashes; Page.drawZigzag args
      pair: roundCap; Page.drawZigzag args
      pair: color; Page.drawZigzag args
      pair: fill; Page.drawZigzag args
      pair: width; Page.drawZigzag args

   .. method:: drawZigzag(p1, p2, breadth = 2, color = (0, 0, 0), width = 1, dashes = None, roundCap = True, overlay = True, morph = None)

      PDF only: Draw a zigzag line from ``p1`` to ``p2`` (point-likes). See :meth:`Shape.drawZigzag`.

   .. index::
      pair: overlay; Page.drawSquiggle args
      pair: closePath; Page.drawSquiggle args
      pair: morph; Page.drawSquiggle args
      pair: dashes; Page.drawSquiggle args
      pair: roundCap; Page.drawSquiggle args
      pair: color; Page.drawSquiggle args
      pair: fill; Page.drawSquiggle args
      pair: width; Page.drawSquiggle args

   .. method:: drawSquiggle(p1, p2, breadth = 2, color = (0, 0, 0), width = 1, dashes = None, roundCap = True, overlay = True, morph = None)

      PDF only: Draw a squiggly (wavy, undulated) line from ``p1`` to ``p2`` (point-likes). See :meth:`Shape.drawSquiggle`.

   .. index::
      pair: overlay; Page.drawCircle args
      pair: closePath; Page.drawCircle args
      pair: morph; Page.drawCircle args
      pair: dashes; Page.drawCircle args
      pair: roundCap; Page.drawCircle args
      pair: color; Page.drawCircle args
      pair: fill; Page.drawCircle args
      pair: width; Page.drawCircle args

   .. method:: drawCircle(center, radius, color = (0, 0, 0), fill = None, width = 1, dashes = None, roundCap = True, overlay = True, morph = None)

      PDF only: Draw a circle around ``center`` (point-like) with a radius of ``radius``. See :meth:`Shape.drawCircle`.

   .. index::
      pair: overlay; Page.drawOval args
      pair: closePath; Page.drawOval args
      pair: morph; Page.drawOval args
      pair: dashes; Page.drawOval args
      pair: roundCap; Page.drawOval args
      pair: color; Page.drawOval args
      pair: fill; Page.drawOval args
      pair: width; Page.drawOval args

   .. method:: drawOval(rect, color = (0, 0, 0), fill = None, width = 1, dashes = None, roundCap = True, overlay = True, morph = None)

      PDF only: Draw an oval (ellipse) within the given rectangle (rect-like). See :meth:`Shape.drawOval`.

   .. index::
      pair: overlay; Page.drawSector args
      pair: closePath; Page.drawSector args
      pair: morph; Page.drawSector args
      pair: dashes; Page.drawSector args
      pair: roundCap; Page.drawSector args
      pair: color; Page.drawSector args
      pair: fill; Page.drawSector args
      pair: width; Page.drawSector args
      pair: fullSector; Page.drawSector args

   .. method:: drawSector(center, point, angle, color = (0, 0, 0), fill = None, width = 1, dashes = None, roundCap = True, fullSector = True, overlay = True, closePath = False, morph = None)

      PDF only: Draw a circular sector, optionally connecting the arc to the circle's center (like a piece of pie). See :meth:`Shape.drawSector`.

   .. index::
      pair: overlay; Page.drawPolyline args
      pair: closePath; Page.drawPolyline args
      pair: morph; Page.drawPolyline args
      pair: dashes; Page.drawPolyline args
      pair: roundCap; Page.drawPolyline args
      pair: color; Page.drawPolyline args
      pair: fill; Page.drawPolyline args
      pair: width; Page.drawPolyline args

   .. method:: drawPolyline(points, color = (0, 0, 0), fill = None, width = 1, dashes = None, roundCap = True, overlay = True, closePath = False, morph = None)

      PDF only: Draw several connected lines defined by a sequence of point-likes. See :meth:`Shape.drawPolyline`.


   .. index::
      pair: overlay; Page.drawBezier args
      pair: closePath; Page.drawBezier args
      pair: morph; Page.drawBezier args
      pair: dashes; Page.drawBezier args
      pair: roundCap; Page.drawBezier args
      pair: color; Page.drawBezier args
      pair: fill; Page.drawBezier args
      pair: width; Page.drawBezier args

   .. method:: drawBezier(p1, p2, p3, p4, color = (0, 0, 0), fill = None, width = 1, dashes = None, roundCap = True, overlay = True, closePath = False, morph = None)

      PDF only: Draw a cubic Bézier curve from ``p1`` to ``p4`` with the control points ``p2`` and ``p3`` (all are point-likes). See :meth:`Shape.drawBezier`.

   .. index::
      pair: overlay; Page.drawCurve args
      pair: closePath; Page.drawCurve args
      pair: morph; Page.drawCurve args
      pair: dashes; Page.drawCurve args
      pair: roundCap; Page.drawCurve args
      pair: color; Page.drawCurve args
      pair: fill; Page.drawCurve args
      pair: width; Page.drawCurve args

   .. method:: drawCurve(p1, p2, p3, color = (0, 0, 0), fill = None, width = 1, dashes = None, roundCap = True, overlay = True, closePath = False, morph = None)

      PDF only: This is a special case of ``drawBezier()``. See :meth:`Shape.drawCurve`.

   .. index::
      pair: overlay; Page.drawRect args
      pair: closePath; Page.drawRect args
      pair: morph; Page.drawRect args
      pair: dashes; Page.drawRect args
      pair: roundCap; Page.drawRect args
      pair: color; Page.drawRect args
      pair: fill; Page.drawRect args
      pair: width; Page.drawRect args

   .. method:: drawRect(rect, color = (0, 0, 0), fill = None, width = 1, dashes = None, roundCap = True, overlay = True, morph = None)

      PDF only: Draw a rectangle. See :meth:`Shape.drawRect`.

      .. note:: An efficient way to background-color a PDF page with the old Python paper color is

          >>> col = fitz.utils.getColor("py_color")
          >>> page.drawRect(page.rect, color=col, fill=col, overlay=False)

   .. index::
      pair: fontname; Page.insertFont args
      pair: fontfile; Page.insertFont args
      pair: fontbuffer; Page.insertFont args
      pair: set_simple; Page.insertFont args
      pair: encoding; Page.insertFont args

   .. method:: insertFont(fontname="helv", fontfile=None, fontbuffer=None, set_simple=False, encoding=TEXT_ENCODING_LATIN)

      PDF only: Add a new font to be used by text output methods and return its :data:`xref`. If not already present in the file, the font definition will be added. Supported are the built-in :data:`Base14_Fonts` and the CJK fonts via **"reserved"** fontnames. Fonts can also be provided as a file path or a memory area containing the image of a font file.

      :arg str fontname: The name by which this font shall be referenced when outputting text on this page. In general, you have a "free" choice here (but consult the :ref:`AdobeManual`, page 56, section 3.2.4 for a formal description of building legal PDF names). However, if it matches one of the :data:`Base14_Fonts` or one of the CJK fonts, ``fontfile`` and ``fontbuffer`` **are ignored**.
      
      In other words, you cannot insert a font via ``fontfile`` / ``fontbuffer`` and also give it a reserved ``fontname``.

      .. note:: A reserved fontname can be specified in any mixture of upper or lower case and still match the right built-in font definition: fontnames "helv", "Helv", "HELV", "Helvetica", etc. all lead to the same font definition "Helvetica". But from a :ref:`Page` perspective, these are **different references**. You can exploit this when using different ``encoding`` variants (Latin, Greek, Cyrillic) of the same font on a page.

      :arg str fontfile: a path to a font file. If used, ``fontname`` must be **different from all reserved names**.

      :arg bytes/bytearray fontbuffer: the image of a font file. If used, ``fontname`` must be **different from all reserved names**. This parameter would typically be used to transfer fonts between different pages of the same or different PDFs.

      :arg int set_simple: applicable for ``fontfile`` / ``fontbuffer`` cases only: enforce treatment as a "simple" font, i.e. one that only uses character codes up to 255.
      :arg int encoding: applicable for the "Helvetica", "Courier" and "Times" sets of :data:`Base14_Fonts` only. Select one of the available encodings Latin (0), Cyrillic (2) or Greek (1). Only use the default (0 = Latin) for "Symbol" and "ZapfDingBats".

      :rytpe: int
      :returns: the :data:`xref` of the installed font.

      .. note:: Built-in fonts will not lead to the inclusion of a font file. So the resulting PDF file will remain small. However, your PDF reader software is responsible for generating an appropriate appearance -- and there **are** differences on whether or how each one of them does this. This is especially true for the CJK fonts, but also for Symbol and ZapfDingbats in some cases. Following are the **Font Names** and their correspondingly installed **Base Font** names:

         **Base-14 Fonts** [#f1]_

         ============= ============================ =========================================
         **Font Name** **Installed Base Font**      **Comments**
         ============= ============================ =========================================
         helv          Helvetica                    normal
         heit          Helvetica-Oblique            italic
         hebo          Helvetica-Bold               bold
         hebi          Helvetica-BoldOblique        bold-italic
         cour          Courier                      normal
         coit          Courier-Oblique              italic
         cobo          Courier-Bold                 bold
         cobi          Courier-BoldOblique          bold-italic
         tiro          Times-Roman                  normal
         tiit          Times-Italic                 italic
         tibo          Times-Bold                   bold
         tibi          Times-BoldItalic             bold-italic
         symb          Symbol
         zadb          ZapfDingbats
         ============= ============================ =========================================

         **CJK Fonts** [#f2]_

         ============= ============================ =========================================
         **Font Name** **Installed Base Font**      **Comments**
         ============= ============================ =========================================
         china-s       Heiti                        simplified Chinese
         china-ss      Song                         simplified Chinese (serif)
         china-t       Fangti                       traditional Chinese
         china-ts      Ming                         traditional Chinese (serif)
         japan         Gothic                       Japanese
         japan-s       Mincho                       Japanese (serif)
         korea         Dotum                        Korean
         korea-s       Batang                       Korean (serif)
         ============= ============================ =========================================

   .. index::
      pair: overlay; Page.insertImage args
      pair: filename; Page.insertImage args
      pair: pixmap; Page.insertImage args
      pair: stream; Page.insertImage args

   .. method:: insertImage(rect, filename = None, pixmap = None, stream = None, overlay = True)

      PDF only: Fill the given rectangle (rect-like) with an image. The image's width-height-proportion will be **adjusted to fit** -- so it may appear distorted. Specify the rectangle appropriately if you want to avoid this. The image is taken from a pixmap, a file or a memory area - of these parameters **exactly one** must be specified.

      :arg rect-like rect: where to put the image on the page. Must be finite and not empty.

      :arg str filename: name of an image file (all MuPDF supported formats - see :ref:`ImageFiles`). If the same image is to be inserted multiple times, choose one of the other two options to avoid some overhead.

      :arg bytes/bytearray stream: memory resident image (all MuPDF supported formats - see :ref:`ImageFiles`).

      :arg pixmap: pixmap containing the image.
      :type pixmap: :ref:`Pixmap`

      For a description of ``overlay`` see :ref:`CommonParms`.

      This example puts the same image on every page of a document:

      >>> doc = fitz.open(...)
      >>> rect = fitz.Rect(0, 0, 50, 50)       # put thumbnail in upper left corner
      >>> img = open("some.jpg", "rb").read()  # an image file
      >>> for page in doc:
              page.insertImage(rect, stream = img)
      >>> doc.save(...)

      Notes:
      
      1. If that same image had already been present in the PDF, then only a reference will be inserted. This of course considerably saves disk space and processing time. But to detect this fact, existing PDF images need to be compared with the new one. This is achieved by storing an MD5 code for each image in a table and only compare the new image's code against the table entries. Generating this MD5 table, however, is done only when doing the first image insertion - which therefore may have an extended response time.

      2. You can use this method to provide a background or foreground image for the page, like a copyright, a watermark or a background color. Or you can combine it with ``searchFor()`` to achieve a textmarker effect. Please remember, that watermarks require a transparent image ...

      3. The image may be inserted uncompressed, e.g. if a ``Pixmap`` is used or if the image has an alpha channel. Therefore, consider using ``deflate = True`` when saving the file.

      4. The image content is stored in its original size - which may be much bigger than the size you are ever displaying. Consider decreasing the stored image size by using the pixmap option and then shrinking it or scaling it down (see :ref:`Pixmap` chapter). The file size savings can be very significant.

      5. The most efficient way to display the same image on multiple pages is :meth:`showPDFpage`. Consult :meth:`Document.convertToPDF` for how to obtain intermediary PDFs usable for that method. Demo script `fitz-logo.py <https://github.com/pymupdf/PyMuPDF/blob/master/demo/fitz-logo.py>`_ implements a fairly complete approach.

   .. method:: getText(output = 'text')

      Retrieves the content of a page in a large variety of formats.

      If ``'text'`` is specified, plain text is returned **in the order as specified during document creation** (i.e. not necessarily the normal reading order).

      :arg str output: A string indicating the requested format, one of ``"text"`` (default), ``"html"``, ``"dict"``, ``"xml"``, ``"xhtml"`` or ``"json"``.

      :rtype: (*str* or *dict*)
      :returns: The page's content as one string or as a dictionary. The information levels of JSON and DICT are exactly equal. In fact, JSON output is created via ``json.dumps(...)`` from DICT. Normally, you probably will use ``"dict"``, it is more convenient and faster.

      .. note:: You can use this method to convert the document into a valid HTML version by wrapping it with appropriate header and trailer strings, see the following snippet. Creating XML or XHTML documents works in exactly the same way. For XML you may also include an arbitrary filename like so: ``fitz.ConversionHeader("xml", filename = doc.name)``. Also see :ref:`HTMLQuality`.

      >>> doc = fitz.open(...)
      >>> ofile = open(doc.name + ".html", "w")
      >>> ofile.write(fitz.ConversionHeader("html"))
      >>> for page in doc: ofile.write(page.getText("html"))
      >>> ofile.write(fitz.ConversionTrailer("html"))
      >>> ofile.close()

   .. method:: getFontList()

      PDF only: Return a list of fonts referenced by the page. Same as :meth:`Document.getPageFontList`.

   .. method:: getImageList()

      PDF only: Return a list of images referenced by the page. Same as :meth:`Document.getPageImageList`.

   .. index::
      pair: matrix; Page.getSVGimage args

   .. method:: getSVGimage(matrix = fitz.Identity)

      Create an SVG image from the page. Only full page images are currently supported.

     :arg matrix-like matrix: a matrix, default is :ref:`Identity`.

     :returns: a UTF-8 encoded string that contains the image. Because SVG has XML syntax it can be saved in a text file with extension ``.svg``.

   .. index::
      pair: matrix; Page.getPixmap args
      pair: colorspace; Page.getPixmap args
      pair: clip; Page.getPixmap args
      pair: alpha; Page.getPixmap args

   .. method:: getPixmap(matrix = fitz.Identity, colorspace = fitz.csRGB, clip = None, alpha = True)

     Create a pixmap from the page. This is probably the most often used method to create pixmaps.

     :arg matrix-like matrix: a matrix-like object, default is :ref:`Identity`.

     :arg colorspace: Defines the required colorspace, one of ``GRAY``, ``RGB`` or ``CMYK`` (case insensitive). Or specify a :ref:`Colorspace`, e.g. one of the predefined ones: :data:`csGRAY`, :data:`csRGB` or :data:`csCMYK`.
     :type colorspace: string, :ref:`Colorspace`

     :arg irect-like clip: restrict rendering to this area.

     :arg bool alpha: A bool indicating whether an alpha channel should be included in the pixmap. Choose ``False`` if you do not really need transparency. This will save a lot of memory (25% in case of RGB ... and pixmaps are typically **large**!), and also processing time in most cases. Also note an important difference in how the image will appear:

        * ``True``: pixmap's samples will be pre-cleared with ``0x00``, including the alpha byte. This will result in **transparent** areas where the page is empty.

        .. image:: img-alpha-1.png

        * ``False``: pixmap's samples will be pre-cleared with ``0xff``. This will result in **white** where the page has nothing to show.

        .. image:: img-alpha-0.png

     :rtype: :ref:`Pixmap`
     :returns: Pixmap of the page.

   .. method:: loadLinks()

      Return the first link on a page. Synonym of property ``firstLink``.

      :rtype: :ref:`Link`
      :returns: first link on the page (or ``None``).

   .. index::
      pair: rotate; Page.setRotation args

   .. method:: setRotation(rotate)

      PDF only: Sets the rotation of the page.

      :arg int rotate: An integer specifying the required rotation in degrees. Should be an integer multiple of 90.

   .. index::
      pair: reuse_xref; Page.showPDFpage args
      pair: keep_proportion; Page.showPDFpage args
      pair: clip; Page.showPDFpage args
      pair: rotate; Page.showPDFpage args
      pair: overlay; Page.showPDFpage args

   .. method:: showPDFpage(rect, docsrc, pno=0, keep_proportion=True, overlay=True, reuse_xref=0, rotate=0, clip=None)

      PDF only: Display a page of another PDF as a **vector image** (otherwise similar to :meth:`Page.insertImage`). This is a multi-purpose method. For example, you can use it to
      
      * create "n-up" versions of existing PDF files, combining several input pages into **one output page** (see example `4-up.py <https://github.com/pymupdf/PyMuPDF/blob/master/examples/4-up.py>`_),
      * create "posterized" PDF files, i.e. every input page is split up in parts which each create a separate output page (see `posterize.py <https://github.com/pymupdf/PyMuPDF/blob/master/examples/posterize.py>`_),
      * include PDF-based vector images like company logos, watermarks, etc., see `svg-logo.py <https://github.com/pymupdf/PyMuPDF/blob/master/examples/svg-logo.py>`_, which puts an SVG-based logo on each page (requires additional packages to deal with SVG-to-PDF conversions).

      :arg rect-like rect: where to place the image on current page.

      :arg docsrc: source PDF document containing the page. Must be a different document object, but may be the same file.
      :type docsrc: :ref:`Document`

      :arg int pno: page number (0-based) to be shown.

      :arg bool keep_proportion: whether to maintain the width-height-ratio (default). If false, the source rectangle will fill the display rectangle completely.

      :arg bool overlay: put image in foreground (default) or background.

      :arg int rotate: show the source rectangle rotated. Must be an integer multiple of 90.

      :arg int reuse_xref: if a source page should be shown multiple times, specify the returned :data:`xref` of its first inclusion. This prevents duplicate source page copies, and thus improves performance and saves memory. Note that source document and page must still be provided!

      :arg rect-like clip: choose which part of the source page to show. Default is the full page rectangle.

      :returns: :data:`xref` of the stored page image if successful. Use this as the value of argument ``reuse_xref`` to show the same source page again.

      .. note:: The displayed source page is shown without any annotations or links. The source page's complete text and images will become an integral part of the containing page, i.e. they will be included in the output of all text extraction methods and appear in methods :meth:`getFontList` and :meth:`getImageList` (whether they are actually visible - see the ``clip`` parameter - or not).

      .. note:: Use the ``reuse_xref`` argument to prevent duplicates as follows. For a technical description of how this function is implemented, see :ref:`FormXObject`. The following example will put the same source page (probably a company logo or a watermark) on every page of PDF ``doc``. The first execution **actually** inserts the source page, the subsequent ones will only insert pointers to it via its :data:`xref`.

      >>> # the first showPDFpage will include source page docsrc[pno],
      >>> # subsequents will reuse it via its xref.
      >>> xref = 0
      >>> for page in doc:
              xref = page.showPDFpage(rect, docsrc, pno,
                                      reuse_xref = xref)

      Example: Show a page rotated by 90 and by -90 degrees:

      >>> import fitz
      >>> doc = fitz.open()
      >>> page=doc.newPage()
      >>> # upper half page
      >>> r1 = fitz.Rect(0, 0, page.rect.width, page.rect.height/2)
      >>> # lower half page
      >>> r2 = r1 + (0, page.rect.height/2, 0, page.rect.height/2)
      >>> src = fitz.open("PyMuPDF.pdf")
      >>> xref = page.showPDFpage(r1, src, 0, rotate=90)
      >>> page.showPDFpage(r2, src, 0, rotate=-90, reuse_xref=xref)
      >>> doc.save("show.pdf")

      .. image:: img-showpdfpage.jpg

   .. method:: newShape()

      PDF only: Create a new :ref:`Shape` object for the page.

      :rtype: :ref:`Shape`
      :returns: a new :ref:`Shape` to use for compound drawings. See description there.

   .. index::
      pair: hit_max; Page.searchFor args

   .. method:: searchFor(text, hit_max = 16, quads = False)

      Searches for ``text`` on a page. Identical to :meth:`TextPage.search`.

      :arg str text: Text to search for. Upper / lower case is ignored. The string may contain spaces.

      :arg int hit_max: Maximum number of occurrences accepted.
      :arg bool quads: Return :ref:`Quad` instead of :ref:`Rect` objects.

      :rtype: list

      :returns: A list of rectangles (quadrilaterals resp.) each of which surrounds one occurrence of ``text``.

   .. method:: setCropBox(r)

      PDF only: change the visible part of the page.

      :arg rect-like r: the new visible area of the page.

      After execution, :attr:`Page.rect` will equal this rectangle, shifted to the top-left position (0, 0). Example session:

      >>> page = doc.newPage()
      >>> page.rect
      fitz.Rect(0.0, 0.0, 595.0, 842.0)
      >>>
      >>> page.CropBox                   # CropBox and MediaBox still equal
      fitz.Rect(0.0, 0.0, 595.0, 842.0)
      >>>
      >>> # now set CropBox to a part of the page
      >>> page.setCropBox(fitz.Rect(100, 100, 400, 400))
      >>> # this will also change the "rect" property:
      >>> page.rect
      fitz.Rect(0.0, 0.0, 300.0, 300.0)
      >>>
      >>> # but MediaBox remains unaffected
      >>> page.MediaBox
      fitz.Rect(0.0, 0.0, 595.0, 842.0)
      >>>
      >>> # revert everything we did
      >>> page.setCropBox(page.MediaBox)
      >>> page.rect
      fitz.Rect(0.0, 0.0, 595.0, 842.0)

   .. attribute:: rotation

      PDF only: contains the rotation of the page in degrees and ``-1`` for other document types.

      :type: int

   .. attribute:: CropBoxPosition

      Contains the displacement of the page's ``/CropBox`` for a PDF, otherwise the top-left coordinates of :attr:`Page.rect`.

      :type: :ref:`Point`

   .. attribute:: CropBox

      The page's ``/CropBox`` for a PDF, else :attr:`Page.rect`.

      :type: :ref:`Rect`

   .. attribute:: MediaBoxSize

      Contains the width and height of the page's ``/MediaBox`` for a PDF, otherwise the bottom-right coordinates of :attr:`Page.rect`.

      :type: :ref:`Point`

   .. attribute:: MediaBox

      The page's ``/MediaBox`` for a PDF, otherwise :attr:`Page.rect`.

      :type: :ref:`Rect`

      .. note:: For most PDF documents and for all other types, ``page.rect == page.CropBox == page.MediaBox`` is true. However, for some PDFs the visible page is a true subset of ``/MediaBox``. In this case the above attributes help to correctly locate page elements.

   .. attribute:: firstLink

      Contains the first :ref:`Link` of a page (or ``None``).

      :type: :ref:`Link`

   .. attribute:: firstAnnot

      Contains the first :ref:`Annot` of a page (or ``None``).

      :type: :ref:`Annot`

   .. attribute:: number

      The page number.

      :type: int

   .. attribute:: parent

      The owning document object.

      :type: :ref:`Document`


   .. attribute:: rect

      Contains the rectangle of the page. Same as result of :meth:`Page.bound()`.

      :type: :ref:`Rect`

   .. attribute:: xref

      The page's PDF :data:`xref`. Zero if not a PDF.

      :type: :ref:`Rect`

-----

Description of ``getLinks()`` Entries
----------------------------------------
Each entry of the ``getLinks()`` list is a dictionay with the following keys:

* ``kind``:  (required) an integer indicating the kind of link. This is one of ``LINK_NONE``, ``LINK_GOTO``, ``LINK_GOTOR``, ``LINK_LAUNCH``, or ``LINK_URI``. For values and meaning of these names refer to :ref:`linkDest Kinds`.

* ``from``:  (required) a :ref:`Rect` describing the "hot spot" location on the page's visible representation (where the cursor changes to a hand image, usually).

* ``page``:  a 0-based integer indicating the destination page. Required for ``LINK_GOTO`` and ``LINK_GOTOR``, else ignored.

* ``to``:   either a ``fitz.Point``, specifying the destination location on the provided page, default is ``fitz.Point(0, 0)``, or a symbolic (indirect) name. If an indirect name is specified, ``page = -1`` is required and the name must be defined in the PDF in order for this to work. Required for ``LINK_GOTO`` and ``LINK_GOTOR``, else ignored.

* ``file``: a string specifying the destination file. Required for ``LINK_GOTOR`` and ``LINK_LAUNCH``, else ignored.

* ``uri``:  a string specifying the destination internet resource. Required for ``LINK_URI``, else ignored.

* ``xref``: an integer specifying the PDF :data:`xref` of the link object. Do not change this entry in any way. Required for link deletion and update, otherwise ignored. For non-PDF documents, this entry contains ``-1``. It is also ``-1`` for **all** entries in the ``getLinks()`` list, if **any** of the links is not supported by MuPDF - see the note below.

Notes on Supporting Links
---------------------------
MuPDF's support for links has changed in **v1.10a**. These changes affect link types :data:`LINK_GOTO` and :data:`LINK_GOTOR`.

Reading (pertains to method ``getLinks()`` and the ``firstLink`` property chain)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If MuPDF detects a link to another file, it will supply either a ``LINK_GOTOR`` or a ``LINK_LAUNCH`` link kind. In case of ``LINK_GOTOR`` destination details may either be given as page number (eventually including position information), or as an indirect destination.

If an indirect destination is given, then this is indicated by ``page = -1``, and ``link.dest.dest`` will contain this name. The dictionaries in the ``getLinks()`` list will contain this information as the ``to`` value.

**Internal links are always** of kind ``LINK_GOTO``. If an internal link specifies an indirect destination, it **will always be resolved** and the resulting direct destination will be returned. Names are **never returned for internal links**, and undefined destinations will cause the link to be ignored.

Writing
~~~~~~~~~

PyMuPDF writes (updates, inserts) links by constructing and writing the appropriate PDF object **source**. This makes it possible to specify indirect destinations for ``LINK_GOTOR`` **and** ``LINK_GOTO`` link kinds (pre ``PDF 1.2`` file formats are **not supported**).

.. caution:: If a ``LINK_GOTO`` indirect destination specifies an undefined name, this link can later on not be found / read again with MuPDF / PyMuPDF. Other readers however **will** detect it, but flag it as erroneous.

Indirect ``LINK_GOTOR`` destinations can in general of course not be checked for validity and are therefore **always accepted**.

Homologous Methods of :ref:`Document` and :ref:`Page`
--------------------------------------------------------
This is an overview of homologous methods on the :ref:`Document` and on the :ref:`Page` level.

====================================== =====================================
**Document Level**                     **Page Level**
====================================== =====================================
``Document.getPageFontlist(pno)``      :meth:`Page.getFontList`
``Document.getPageImageList(pno)``     :meth:`Page.getImageList`
``Document.getPagePixmap(pno, ...)``   :meth:`Page.getPixmap`
``Document.getPageText(pno, ...)``     :meth:`Page.getText`
``Document.searchPageFor(pno, ...)``   :meth:`Page.searchFor`
====================================== =====================================

The page number ``pno`` is 0-based and can be any negative or positive number ``< len(doc)``.

**Technical Side Note:**

Most document methods (left column) exist for convenience reasons, and are just wrappers for: ``Document[pno].<page method>``. So they **load and discard the page** on each execution.

However, the first two methods work differently. They only need a page's object definition statement - the page itself will not be loaded. So e.g. :meth:`Page.getFontList` is a wrapper the other way round and defined as follows: ``page.getFontList == page.parent.getPageFontList(page.number)``.

.. rubric:: Footnotes

.. [#f1] If your existing code already uses the installed base name as a font reference (as it was supported by PyMuPDF versions earlier than 1.14), this will continue to work.

.. [#f2] Not all PDF reader software -- which includes internet browsers and office software -- will display all of these fonts. And if they do, the difference between the **serifed** and the **non-serifed** version may hardly be noticable. But serifed and non-serifed versions lead to different installed base fonts, thus providing an option to achieve desired results with a specific PDF reader.