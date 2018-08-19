
.. _Annot:

================
Annot
================
Quote from the :ref:`AdobeManual`: "An annotation associates an object such as a note, sound, or movie with a location on a page of a PDF document, or provides a way to interact with the user by means of the mouse and keyboard."

This class supports accessing such annotations - not only for PDF files, but for all MuPDF supported document types. However, only a few methods and properties apply to non-PDF documents.

There is a parent-child relationship between an annotation and its page. If the page object becomes unusable (closed document, any document structure change, etc.), then so does every of its existing annotation objects - an exception is raised saying that the object is "orphaned", whenever an annotation property or method is accessed.


============================ ==============================================================
**Attribute**                **Short Description**
============================ ==============================================================
:meth:`Annot.getPixmap`      image of the annotation as a pixmap
:meth:`Annot.setInfo`        PDF only: change metadata of an annotation
:meth:`Annot.setBorder`      PDF only: changes the border of an annotation
:meth:`Annot.setFlags`       PDF only: changes the flags of an annotation
:meth:`Annot.setRect`        PDF only: changes the rectangle of an annotation
:meth:`Annot.setColors`      PDF only: changes the colors of an annotation
:meth:`Annot.setLineEnds`    PDF only: sets the line ending styles
:meth:`Annot.setOpacity`     PDF only: changes the annot's transparency
:meth:`Annot.updateImage`    PDF only: applies border and color values to shown image
:meth:`Annot.updateWidget`   PDF only: change an exsiting form field
:meth:`Annot.fileInfo`       PDF only: returns attached file information
:meth:`Annot.fileGet`        PDF only: returns attached file content
:meth:`Annot.fileUpd`        PDF only: sets attached file new content
:attr:`Annot.border`         PDF only: border details
:attr:`Annot.colors`         PDF only: border / background and fill colors
:attr:`Annot.flags`          PDF only: annotation flags
:attr:`Annot.info`           PDF only: various information
:attr:`Annot.lineEnds`       PDF only: start / end appearance of line-type annotations
:attr:`Annot.next`           link to the next annotation
:attr:`Annot.opacity`        the annot's transparency
:attr:`Annot.parent`         page object of the annotation
:attr:`Annot.rect`           rectangle containing the annotation
:attr:`Annot.type`           PDF only: type of the annotation
:attr:`Annot.vertices`       PDF only: point coordinates of Polygons, PolyLines, etc.
:attr:`Annot.widget_name`    PDF only: "Widget" field name
:attr:`Annot.widget_value`   PDF only: "Widget" field value
:attr:`Annot.widget_choices` PDF only: possible values for "Widget" list / combo boxes
:attr:`Annot.widget_type`    PDF only: "Widget" field type
============================ ==============================================================

**Class API**

.. class:: Annot

   .. index::
      pair: matrix; Annot.getPixmap args
      pair: colorspace; Annot.getPixmap args
      pair: alpha; Annot.getPixmap args

   .. method:: getPixmap(matrix = fitz.Identity, colorspace = fitz.csRGB, alpha = False)

      Creates a pixmap from the annotation as it appears on the page in untransformed coordinates. The pixmap's :ref:`IRect` equals ``Annot.rect.irect`` (see below).

      :arg matrix: a matrix to be used for image creation. Default is the ``fitz.Identity`` matrix.
      :type matrix: :ref:`Matrix`

      :arg colorspace: a colorspace to be used for image creation. Default is ``fitz.csRGB``.
      :type colorspace: :ref:`Colorspace`

      :arg bool alpha: whether to include transparency information. Default is ``False``.

      :rtype: :ref:`Pixmap`

   .. method:: setInfo(d)

      Changes the info dictionary. This includes dates, contents, subject and author (title). Changes for ``name`` will be ignored.

      :arg dict d: a dictionary compatible with the ``info`` property (see below). All entries must be strings.

   .. method:: setLineEnds(start, end)

      PDF only: Sets an annotation's line ending styles. Only 'FreeText', 'Line', 'PolyLine', and 'Polygon' annotations can have these properties. Each of these annotation types is defined by a list of points which are connected by lines. The symbol identified by ``start`` is attached to the first point, and ``end`` to the last point of this list. For unsupported annotation types, a no-operation with a warning message results. See :ref:`Annotation Line Ends` for details.

      :arg int start: The symbol number for the first point.
      :arg int end: The symbol number for the last point.

   .. method:: setOpacity(value)

      PDF only: Change an annotation's transparency. A visible effect only occurs for annotation types 'Circle', 'Square', 'Line', 'PolyLine' and 'Polygon'. Other cases result in a no-op.

      :arg float value: a float in range ``[0, 1]``. Any value outside is assumed to be 1. E.g. a value of 0.5 sets the transparency to 50%.

      Three overlapping 'Circle' annotations with each opacity set to 0.5:

      .. image:: img-opacity.jpg

   .. method:: setRect(rect)

      Changes the rectangle of an annotation. The annotation can be moved around and both sides of the rectangle can be independently scaled. However, the annotation appearance will never get rotated, flipped or sheared.

      :arg rect: the new rectangle of the annotation (finite and not empty). E.g. using a value of ``annot.rect + (5, 5, 5, 5)`` will shift the annot position 5 pixels to the right and downwards.

      :type rect: :ref:`Rect`

      .. note:: Rectangles of *line-type annotations* (i.e. 'Line', 'PolyLine' and 'Polygon') have originally been created automatically. For them, the method re-executes that process:

          1. Calculate a transformation matrix M, that transforms the old rectangle to the target one.
          2. Apply M to the annotation points.
          3. Re-calculate the final target rectangle as the smallest one that contains the points, each one surrounded by a little circle of radius 3 * line width. The extra space for the circles ensures that any line end symbols also are inside. So the actual resulting rectangle may not exactly equal the given ``rect`` parameter.

   .. method:: setBorder(border)

      PDF only: Change border width and dashing properties.

      :arg dict border: a dictionary with keys ``width`` (*float*), ``style`` (*str*) and ``dashes`` (*list*). Omitted values will leave the resp. property unchanged. To remove dashing and get a contiguous line, specify ``"dashes": []``.

      .. note:: For *line-type annotations* (see above) this method may lead to a changed rectangle if the line ``width`` is changing. This is because the rectangle in these cases is **calculated** and not provided via annotation construction.

   .. method:: setFlags(flags)

      Changes the annotation flags. See :ref:`Annotation Flags` for possible values and use the ``|`` operator to combine several.

      :arg int flags: an integer specifying the required flags.

   .. method:: setColors(d)

      PDF only: Changes the "stroke" and "fill" colors for supported annotation types.

      :arg dict d: a dictionary containing color specifications. For accepted dictionary keys and values see below. The most practical way should be to first make a copy of the ``colors`` property and then modify this dictionary as required.

      .. note:: This method **does not work** for widget annotations, and results in a no-op with a warning message. Use :meth:`updateWidget` instead. Certain annotation types have no fill colors. In these cases this value is ignored and a warning is issued.

   .. method:: updateImage()

      Modify the displayed image such that it coincides with the values contained in the ``width``, ``border``, ``colors`` and ``dashes`` properties. This is a no-op for annotation types ANNOT_LINE, ANNOT_POLYLINE, ANNOT_POLYGON, ANNOT_CIRCLE, and ANNOT_SQUARE, because their appearance is always completely rebuilt with any change.

   .. method:: updateWidget(widget)

      Modifies an existing form field. The existing and the changed widget attributes must all be provided by way of a :ref:`Widget` object. This is because the method will update the field with **all properties** of the :ref:`Widget` object.

      :arg widget: a widget object containing the **complete** (old and new) properties of the widget. Create the object via :attr:`widget` and apply your changes before passing it to this method.
      :type widget: :ref:`Widget`

      .. note:: As with :meth:`Page.addWidget`, make sure to use option ``clean = True`` when saving the file. This will cause an update of the annotation's appearance.

   .. method:: fileInfo()

      Basic information of the attached file.

      :rtype: dict
      :returns: a dictionary with keys ``filename``, ``ufilename``, ``desc`` (description), ``size`` (uncompressed file size), ``length`` (compressed length).

   .. method:: fileGet()

      Returns attached file content.

      :rtype: bytes
      :returns: the content of the attached file.

   .. index::
      pair: filename; Annot.fileUpd args
      pair: ufilename; Annot.fileUpd args
      pair: desc; Annot.fileUpd args

   .. method:: fileUpd(buffer = None, filename=None, ufilename=None, desc = None)

      Updates the content of an attached file.

      :arg bytes/bytearray buffer: the new file content. May be omitted to only change meta-information.

      :arg str filename: new filename to associate with the file.

      :arg str ufilename: new unicode filename to associate with the file.

      :arg str desc: new description of the file content.

   .. attribute:: opacity

      The annotation's transparency. If set, it is a value in range ``[0, 1]``. The PDF default is ``1.0``. However, in an effort to tell the difference, we return ``-1.0`` if not set (as well as for non-PDFs).

      :rtype: float

   .. attribute:: parent

      The owning page object of the annotation.

      :rtype: :ref:`Page`

   .. attribute:: rect

      The rectangle containing the annotation in untransformed coordinates.

      :rtype: :ref:`Rect`

   .. attribute:: next

      The next annotation on this page or ``None``.

      :rtype: ``Annot``

   .. attribute:: type

      Meaningful for PDF only: A number and one or two strings describing the annotation type, like ``[2, 'FreeText', 'FreeTextCallout']``. The second string entry is optional and may be empty. ``[]`` if not PDF. See the appendix :ref:`Annotation Types` for a list of possible values and their meanings.

      :rtype: list

   .. attribute:: info

      Meaningful for PDF only: A dictionary containing various information. All fields are (unicode) strings.

      * ``name`` - e.g. for ``[12, 'Stamp']`` type annotations it will contain the stamp text like ``Sold`` or ``Experimental``.

      * ``content`` - a string containing the text for type ``Text`` and ``FreeText`` annotations. Commonly used for filling the text field of annotation pop-up windows. For ``FileAttachment`` it should be used as description for the attached file. Initially just contains the filename.

      * ``title`` - a string containing the title of the annotation pop-up window. By convention, this is used for the annotation author.

      * ``creationDate`` - creation timestamp.

      * ``modDate`` - last modified timestamp.

      * ``subject`` - subject, an optional string.

      :rtype: dict


   .. attribute:: flags

      Meaningful for PDF only: An integer whose low order bits contain flags for how the annotation should be presented. See section :ref:`Annotation Flags` for details.

      :rtype: int

   .. attribute:: lineEnds

      Meaningful for PDF only: A tuple of two integers specifying the starting and the ending appearance of annotations of types 'FreeText', 'Line', 'PolyLine', and 'Polygon'. ``None`` if not specified or not applicable. For possible values and descriptions in this list, see :ref:`Annotation Line Ends` and the :ref:`AdobeManual`, table 8.27 on page 630.

      :rtype: dict

   .. attribute:: vertices

      PDF only: A list containing point ("vertices") coordinates (each given by a pair of floats) for various types of annotations:
      
      * ``Line`` - the starting and ending coordinates (2 float pairs).
      * ``[2, 'FreeText', 'FreeTextCallout']`` - 2 or 3 float pairs designating the starting, the (optional) knee point, and the ending coordinates.
      * ``PolyLine`` / ``Polygon`` - the coordinates of the edges connected by line pieces (n float pairs for n points).
      * text markup annotations - 4 float pairs specifying the ``QuadPoints`` of the marked text span (see :ref:`AdobeManual`, page 634).
      * ``Ink`` - list of one to many sublists of vertex coordinates. Each such sublist represents a separate line in the drawing.

      :rtype: list

   .. attribute:: widget

      PDF only: A class containing all properties of a **form field** - including the following three attributes. ``None`` for other annotation types.

      :rtype: :ref:`Widget`

   .. attribute:: widget_name

      PDF only: The field name for an annotation of type ``ANNOT_WIDGET``, ``None`` otherwise. Equals :attr:`Widget.field_name`.

      :rtype: str

   .. attribute:: widget_value

      PDF only: The field content for an annotation of type ``ANNOT_WIDGET``. Is ``None`` for non-PDFs, other annotation types, or if no value has been entered. For button types the value will be ``True`` or ``False``. Push button states have no permanent reflection in the file and are therefore always reported as ``False``. For text, list boxes and combo boxes, a string is returned for single values. If multiple selections have been made (may happen for list boxes and combo boxes), a list of strings is returned. For list boxes and combo boxes, the selectable values are contained in :attr:`widget_choices` below. Equals :attr:`Widget.field_value`.

      :rtype: bool, str or list

   .. attribute:: widget_choices

      PDF only: Contains a list of selectable values for list boxes and combo boxes (annotation type ``ANNOT_WIDGET``), else ``None``. Equals :attr:`Widget.choice_values`.

      :rtype: list

   .. attribute:: widget_type

      PDF only: The field type for an annotation of type ``ANNOT_WIDGET``, else ``None``.

      :rtype: tuple

      :returns: a tuple ``(int, str)``. E.g. for a text field ``(3, 'Text')`` is returned. For a complete list see :ref:`Annotation Types`. The first item equals :attr:`Widget.field_type`, and the second is :attr:`Widget.field_type_string`.

   .. attribute:: colors

      Meaningful for PDF only: A dictionary of two lists of floats in range ``0 <= float <= 1`` specifying the ``stroke`` and the interior (``fill``) colors. The stroke color is used for borders and everything that is actively painted or written ("stroked"). The fill color is used for the interior of objects like line ends, circles and squares. The lengths of these lists implicitely determine the colorspaces used: 1 = GRAY, 3 = RGB, 4 = CMYK. So ``[1.0, 0.0, 0.0]`` stands for RGB color red. Both lists can be ``[]`` if not specified. The dictionary will be empty ``{}`` if no PDF. The value of each float ``f`` is mapped to the integer value ``i`` in range 0 to 255 via the computation ``f = i / 255``.

      :rtype: dict

   .. attribute:: border

      Meaningful for PDF only: A dictionary containing border characteristics. It will be ``None`` for non-PDFs and an empty dictionary if no border information exists. The following keys can occur:

      * ``width`` - a float indicating the border thickness in points.

      * ``dashes`` - a list of integers (arbitrarily limited to 10) specifying a line dash pattern in user units (usually points). ``[]`` means no dashes, ``[n]`` means equal on-off lengths of ``n`` points, longer lists will be interpreted as specifying alternating on-off length values. See the :ref:`AdobeManual` page 217 for more details.

      * ``style`` - 1-byte border style: ``S`` (Solid) = solid rectangle surrounding the annotation, ``D`` (Dashed) = dashed rectangle surrounding the annotation, the dash pattern is specified by the ``dashes`` entry, ``B`` (Beveled) = a simulated embossed rectangle that appears to be raised above the surface of the page, ``I`` (Inset) = a simulated engraved rectangle that appears to be recessed below the surface of the page, ``U`` (Underline) = a single line along the bottom of the annotation rectangle.

      :rtype: dict
      
Example
--------
Change the graphical image of an annotation. Also update the "author" and the text to be shown in the popup window::

 doc = fitz.open("circle-in.pdf")
 page = doc[0]                          # page 0
 annot = page.firstAnnot                # get the annotation
 annot.setBorder({"dashes": [3]})       # set dashes to "3 on, 3 off ..."
 
 # set stroke and fill color to some blue
 annot.setColors({"stroke":(0, 0, 1), "fill":(0.75, 0.8, 0.95)})
 info = annot.info                      # get info dict
 info["title"] = "Jorj X. McKie"        # set author
 
 # text in popup window ...
 info["content"] = "I changed border and colors and enlarged the image by 20%."
 info["subject"] = "Demonstration of PyMuPDF"     # some PDF viewers also show this
 annot.setInfo(info)                    # update info dict
 r = annot.rect                         # take annot rect
 r.x1 = r.x0 + r.width  * 1.2           # new location has same top-left
 r.y1 = r.y0 + r.height * 1.2           # but 20% longer sides
 annot.setRect(r)                       # update rectangle
 doc.save("circle-out.pdf", garbage=4)  # save

This is how the circle annotation looks like before and after the change (pop-up windows displayed using Nitro PDF viewer):

|circle|
 
.. |circle| image:: img-circle.png
