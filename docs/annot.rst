
.. _Annot:

================
Annot
================
Quote from the :ref:`AdobeManual`: "An annotation associates an object such as a note, sound, or movie with a location on a page of a PDF document, or provides a way to interact with the user by means of the mouse and keyboard."

This class supports accessing such annotations - not only for PDF files, but for all MuPDF supported document types. However, only a few methods and properties apply to non-PDF documents.

There is a parent-child relationship between an annotation and its page. If the page object becomes unusable (closed document, any document structure change, etc.), then so does every of its existing annotation objects - an exception is raised saying that the object is "orphaned", whenever an annotation property or method is accessed.


=========================== ==============================================================
**Attribute**               **Short Description**
=========================== ==============================================================
:meth:`Annot.getPixmap`     image of the annotation as a pixmap
:meth:`Annot.setInfo`       PDF only: change metadata of an annotation
:meth:`Annot.setBorder`     PDF only: changes the border of an annotation
:meth:`Annot.setFlags`      PDF only: changes the flags of an annotation
:meth:`Annot.setRect`       PDF only: changes the rectangle of an annotation
:meth:`Annot.setColors`     PDF only: changes the colors of an annotation
:meth:`Annot.updateImage`   PDF only: applies border and color values to shown image
:meth:`Annot.fileInfo`      PDF only: returns attached file information
:meth:`Annot.fileGet`       PDF only: returns attached file content
:meth:`Annot.fileUpd`       PDF only: sets attached file new content
:attr:`Annot.border`        PDF only: border details
:attr:`Annot.colors`        PDF only: border / background and fill colors
:attr:`Annot.flags`         PDF only: annotation flags
:attr:`Annot.info`          PDF only: various information
:attr:`Annot.lineEnds`      PDF only: start / end appearance of line-type annotations
:attr:`Annot.next`          link to the next annotation
:attr:`Annot.parent`        page object of the annotation
:attr:`Annot.rect`          rectangle containing the annotation
:attr:`Annot.type`          PDF only: type of the annotation
:attr:`Annot.vertices`      PDF only: point coordinates of Polygons, PolyLines, etc.
:attr:`Annot.widget_name`   PDF only: "Widget" field name
:attr:`Annot.widget_text`   PDF only: "Widget" text contents
:attr:`Annot.widget_type`   PDF only: "Widget" field type
=========================== ==============================================================

**Class API**

.. class:: Annot

   .. method:: getPixmap(matrix = fitz.Ientity, colorspace = fitz.csRGB, alpha = False)

      Creates a pixmap from the annotation as it appears on the page in untransformed coordinates. The pixmap's :ref:`IRect` equals ``Annot.rect.irect`` (see below).

      :arg matrix: a matrix to be used for image creation. Default is the ``fitz.Identity`` matrix.
      :type matrix: :ref:`Matrix`

      :arg colorspace: a colorspace to be used for image creation. Default is ``fitz.csRGB``.
      :type colorspace: :ref:`Colorspace`

      :arg bool alpha: whether to include transparency information. Default is ``False``.

      :rtype: :ref:`Pixmap`

   .. method:: setInfo(d)

      Changes the info dictionary. This is includes dates, contents, subject and author (title). Changes for ``name`` will be ignored.

      :arg dict d: a dictionary compatible with the ``info`` property (see below). All entries must be ``unicode``, ``bytes``, or strings. If ``bytes`` values in Python 3 they will be treated as being UTF8 encoded.

   .. method:: setRect(rect)

      Changes the rectangle of an annotation. The annotation can be moved around and both sides of the rectangle can be independently scaled. However, the annotation appearance will never get rotated, flipped or sheared.

      :arg rect: the new rectangle of the annotation. This could e.g. be a rectangle ``rect = Annot.rect * M`` with a suitable :ref:`Matrix` M (only scaling and translating will yield the expected effect).

      :type rect: :ref:`Rect`

   .. method:: setBorder(value)

      PDF only: Change border width and dashing properties. Any other border properties will be deleted.

      :arg value: a number or a dictionary specifying the desired border properties. If a dictionary, its ``width`` and ``dashes`` keys are used (see property ``annot.border``). If a number is specified or a dictionary like ``{"width": w}``, only the border width will be changed and any dashes will remain unchanged. Conversely, with a dictionary ``{"dashes": [...]}``, only line dashing will be changed. To remove dashing and get a contiguous line, specify ``{"dashes": []}``.

      :type value: float or dict

   .. method:: setFlags(flags)

      Changes the flags of the annotation. See :ref:`Annotation Flags` for possible values and use the ``|`` operator to combine several.

      :arg int flags: an integer specifying the required flags.

   .. method:: setColors(d)

      Changes the colors associated with the annotation.

      :arg dict d: a dictionary containing color specifications. For accepted dictionary keys and values see below. The most practical way should be to first make a copy of the ``colors`` property and then modify this dictionary as required. 

   .. method:: updateImage()

      Attempts to modify the displayed graphical image such that it coincides with the values currently contained in the ``border`` and ``colors`` properties. This is achieved by modifying the contents stream of the associated appearance ``XObject``. Not all possible formats of content streams are currently supported: if the stream contains invocations of yet other ``XObject`` objects, a ``ValueError`` is raised.

   .. method:: fileInfo()

      Returns basic information of an attached file (file attachment annotations only).

      :rtype: dict
      :returns: a dictionary with keys ``filename``, ``size`` (uncompressed file size), ``length`` (compressed length).

   .. method:: fileGet()

      Returns the uncompressed content of the attached file.

      :rtype: bytes
      :returns: the content of the attached file.

   .. method:: fileUpd(buffer, filename=None)

      Updates the content of an attached file with new data. Optionally, the filename can be changed, too.

      :arg buffer: the new file content.

      :type buffer: bytes or bytearray

      :arg str filename: new filename to associate with the file.

      :rtype: int
      :returns: zero

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

      Meaningful for PDF only: A dictionary specifying the starting and the ending appearance of annotations of types ``Line``, ``PolyLine``, among others. An example would be ``{'start': 'None', 'end': 'OpenArrow'}``. ``{}`` if not specified or not applicable. For possible values and descriptions in this list, see the :ref:`AdobeManual`, table 8.27 on page 630.

      :rtype: dict

   .. attribute:: vertices

      PDF only: A list containing point ("vertices") coordinates (each given by 2 floats specifying the x and y coordinate respectively) for various types of annotations:
      
      * ``Line`` - the starting and ending coordinates (4 floats).
      * ``[2, 'FreeText', 'FreeTextCallout']`` - 4 or 6 floats designating the starting, the (optional) knee point, and the ending coordinates.
      * ``PolyLine`` / ``Polygon`` - the coordinates of the edges connected by line pieces ( ``2 * n`` floats for ``n`` points).
      * text markup annotations - ``8 * n`` floats specifying the ``QuadPoints`` of the ``n`` marked text spans (see :ref:`AdobeManual`, page 634).
      * ``Ink`` - list of one to many sublists of vertex coordinates. Each such sublist represents a separate line in the drawing.

      :rtype: list

   .. attribute:: widget_name

      PDF only: The field name for an annotation of type ``(19, "Widget")``.

      :rtype: str

   .. attribute:: widget_text

      PDF only: The text field content for an annotation of type ``(19, "Widget")``.

      :rtype: str

   .. attribute:: widget_type

      PDF only: The field type for an annotation of type (19, "Widget").

      :rtype: tuple
      :returns: a tuple ``(int, str)``. If not applicable ``(-1, '')`` is returned. E.g. for a text field ``(3, 'Tx')`` is returned.

   .. attribute:: colors

      Meaningful for PDF only: A dictionary of two lists of floats in range ``0 <= float <= 1`` specifying the common (``common``) or ``stroke`` and the interior (``fill``) ``non-stroke`` colors. The common color is used for borders and everything that is actively painted or written (*"stroked"*). The fill color is used for the interior of objects like line ends, circles and squares. The lengths of these lists implicitely determine the colorspaces used: 1 = GRAY, 3 = RGB, 4 = CMYK. So ``[1.0, 0.0, 0.0]`` stands for RGB and color ``red``. Both lists can be ``[]`` if not specified. The dictionary will be empty ``{}`` if no PDF. The value of each float is mapped to integer values from ``0 (<=> 0.0)`` to ``255 (<=> 1.0)``.

      :rtype: dict

   .. attribute:: border

      Meaningful for PDF only: A dictionary containing border characteristics. It will be empty ``{}`` if not PDF or when no border information is provided. Technically, the PDF entries ``/Border``, ``/BS`` and ``/BE`` will be checked to build this information. The following keys can occur:

      * ``width`` - a float indicating the border thickness in points.

      * ``effect`` - a list specifying a border line effect like ``[1, 'C']``. The first entry "intensity" is an integer (from 0 to 2 for maximum intensity). The second is either 'S' for "no effect" or 'C' for a "cloudy" line.

      * ``dashes`` - a list of integers (arbitrarily limited to 10) specifying a line dash pattern in user units (usually points). ``[]`` means no dashes, ``[n]`` means equal on-off lengths of ``n`` points, longer lists will be interpreted as specifying alternating on-off length values. See the :ref:`AdobeManual` page 217 for more details.

      * ``style`` - 1-byte border style: ``S`` (Solid) = solid rectangle surrounding the annotation, ``D`` (Dashed) = dashed rectangle surrounding the annotation, the dash pattern is specified by the ``dashes`` entry, ``B`` (Beveled) = a simulated embossed rectangle that appears to be raised above the surface of the page, ``I`` (Inset) = a simulated engraved rectangle that appears to be recessed below the surface of the page, ``U`` (Underline) = a single line along the bottom of the annotation rectangle.

      :rtype: dict
      
Example
--------
Change the graphical image of an annotation. Also update the "author" and the text to be shown in the popup window:
::
 doc = fitz.open("circle-in.pdf")
 page = doc[0]                          # page 0
 annot = page.firstAnnot                # get the annotation
 annot.setBorder({"dashes": [3]})       # set dashes to "3 on, 3 off ..."
 
 # set border / popup color to blue and fill color to some light blue
 annot.setColors({"common":[0, 0, 1], "fill":[0.75, 0.8, 0.95]})
 info = annot.info                      # get info dict
 info["title"] = "Jorj X. McKie"        # author name in popup title
 
 # text in popup window ...
 info["content"] = "I changed border and colors and enlarged the image by 20%."
 info["subject"] = "Demonstration of PyMuPDF"     # some readers also show this
 annot.setInfo(info)                    # update info dict
 r = annot.rect                         # take annot rect
 r.x1 = r.x0 + r.width  * 1.2           # new location has same top-left
 r.y1 = r.y0 + r.height * 1.2           # but 20% longer sides
 annot.setRect(r)                       # update rectangle
 annot.updateImage()                    # update appearance
 doc.save("circle-out.pdf", garbage=4)  # save

This is how the circle annotation looks like, before and after the change:

|circle|
 
.. |circle| image:: img-circle.png
