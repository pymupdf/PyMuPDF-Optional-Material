.. _Shape:

Shape
================

This class allows creating interconnected graphical elements on a PDF page. Its methods have the same meaning and name as the corresponding :ref:`Page` methods. Their :ref:`CommonParms` are however exported to a separate method, ``finish()``. In addition, all draw methods return a :ref:`Point` object to support connected drawing paths. This point always equals the **"current point"**, that PDF maintains during path construction.

The class now also supports the text insertion methods ``insertText()`` and ``insertTextbox()``. They need a slightly different handling compared to the draw methods (see below for details):

1. They do not use :attr:`Shape.contents`. Instead they directly modify :attr:`Shape.totalcont`.
2. They do not use nor need :meth:`Shape.finish`.
3. They provide their own ``color`` and ``morph`` arguments.
4. They do not use nor change :attr:`Shape.lastPoint`.

As with the draw methods, text insertion requires using :meth:`Shape.commit` to update the page.

================================ =================================================
**Method / Attribute**             **Description**
================================ =================================================
:meth:`Shape.commit`             update the page's ``/Contents`` object
:meth:`Shape.drawBezier`         draw a cubic Bézier curve
:meth:`Shape.drawCircle`         draw a circle around a point
:meth:`Shape.drawCurve`          draw a cubic Bézier using one helper point
:meth:`Shape.drawLine`           draw a line
:meth:`Shape.drawOval`           draw an ellipse
:meth:`Shape.drawPolyline`       connect a sequence of points
:meth:`Shape.drawRect`           draw a rectangle
:meth:`Shape.drawSector`         draw a circular sector or piece of pie
:meth:`Shape.drawSquiggle`       draw a squiggly line
:meth:`Shape.drawZigzag`         draw a zigzag line
:meth:`Shape.finish`             finish a set of draws
:meth:`Shape.insertText`         insert text lines
:meth:`Shape.insertTextbox`      insert text into a rectangle
:attr:`Shape.contents`           draw commands since last ``finish()``
:attr:`Shape.doc`                stores the page's document
:attr:`Shape.height`             stores the page's height
:attr:`Shape.lastPoint`          stores the current point
:attr:`Shape.page`               stores the owning page
:attr:`Shape.width`              stores the page's width
:attr:`Shape.totalcont`          accumulated string to be stored in ``/Contents``
================================ =================================================

**Class API**

.. class:: Shape

   .. method:: __init__(self, page)

      Create a new drawing. During importing PyMuPDF, the ``fitz.Page`` object is being given the convenience method ``newShape()`` to construct a ``Shape`` object. During instantiation, a check will be made whether we do have a PDF page. An exception is otherwise raised.

      :arg page: an existing page of a PDF document.
      :type page: :ref:`Page`

   .. method:: drawLine(p1, p2)

      Draw a line from :ref:`Point` objects ``p1`` to ``p2``.

      :arg p1: starting point
      :type p1: :ref:`Point`

      :arg p2: end point
      :type p2: :ref:`Point`

      :rtype: :ref:`Point`
      :returns: the end point, ``p2``.

   .. method:: drawSquiggle(p1, p2, breadth = 2)

      Draw a squiggly (wavy, undulated) line from :ref:`Point` objects ``p1`` to ``p2``. An integer number of full wave periods will always be drawn, one period having a length of ``4 * breadth``. The breadth parameter will be adjusted as necessary to meet this condition. The drawn line will always turn "left" when leaving ``p1`` and always join ``p2`` from the "right".

      :arg p1: starting point
      :type p1: :ref:`Point`

      :arg p2: end point
      :type p2: :ref:`Point`

      :arg float breadth: the amplitude of each wave. The condition ``2 * breadth < abs(p2 - p1)`` must be true to fit in at least one wave. See the following picture, which shows two points connected by one full period.

      :rtype: :ref:`Point`
      :returns: the end point, ``p2``.

      .. image:: img_breadth.png

      Here is an example of three connected lines, forming a closed, filled triangle. Little arrows indicate the stroking direction.

      .. image:: img_squiggly.png

      .. note:: Waves drawn are **not** trigonometric (sine / cosine). If you need that, have a look at `draw-sines.py <https://github.com/rk700/PyMuPDF/blob/master/demo/draw-sines.py>`_.

   .. method:: drawZigzag(p1, p2, breadth = 2)

      Draw a zigzag line from :ref:`Point` objects ``p1`` to ``p2``. An integer number of full zigzag periods will always be drawn, one period having a length of ``4 * breadth``. The breadth parameter will be adjusted to meet this condition. The drawn line will always turn "left" when leaving ``p1`` and always join ``p2`` from the "right".

      :arg p1: starting point
      :type p1: :ref:`Point`

      :arg p2: end point
      :type p2: :ref:`Point`

      :arg float breadth: the amplitude of the movement. The condition ``2 * breadth < abs(p2 - p1)`` must be true to fit in at least one period.

      :rtype: :ref:`Point`
      :returns: the end point, ``p2``.

   .. method:: drawPolyline(points)

      Draw several connected lines between points contained in the sequence ``points``. This can be used for creating arbitrary polygons by setting the last item equal to the first one.

      :arg sequence points: a sequence of :ref:`Point` objects. Its length must at least be 2 (in which case it is equivalent to ``drawLine()``).

      :rtype: :ref:`Point`
      :returns: ``points[-1]`` - the last point in the argument sequence.

   .. method:: drawBezier(p1, p2, p3, p4)

      Draw a standard cubic Bézier curve from ``p1`` to ``p4``, using ``p2`` and ``p3`` as control points.

      :arg p1: starting point
      :type p1: :ref:`Point`

      :arg p2: control point 1
      :type p2: :ref:`Point`

      :arg p3: control point 2
      :type p3: :ref:`Point`

      :arg p4: end point
      :type p4: :ref:`Point`

      :rtype: :ref:`Point`
      :returns: the end point, ``p4``.

      Example:

      .. image:: img_drawBezier.png

   .. method:: drawOval(rect)

      Draw an ellipse inside the given rectangle. If ``rect`` is a square, a standard circle is drawn. The drawing starts and ends at the middle point of the left rectangle side in a counter-clockwise movement.

      :arg rect: rectangle, must be finite and not empty.
      :type rect: :ref:`Rect`

      :rtype: :ref:`Point`
      :returns: the middle point of the left rectangle side.

   .. method:: drawCircle(center, radius)

      Draw a circle given its center and radius. The drawing starts and ends at point ``start = center - (radius, 0)`` in a counter-clockwise movement. ``start`` corresponds to the middle point of the enclosing square's left border.

      The method is a shortcut for ``drawSector(center, start, 360, fullSector = False)``. To draw a circle in a clockwise movement, change the sign of the degree.

      :arg center: the center of the circle.
      :type center: :ref:`Point`

      :arg float radius: the radius of the circle. Must be positive.

      :rtype: :ref:`Point`
      :returns: ``center - (radius, 0)``.

   .. method:: drawCurve(p1, p2, p3)

      A special case of ``drawBezier()``: Draw a cubic Bézier curve from ``p1`` to ``p3``. On each of the two lines from ``p1`` to ``p2`` and from ``p2`` to ``p3`` one control point is generated. This guaranties that the curve's curvature does not change its sign. If these two connecting lines intersect with an angle of 90 degress, then the resulting curve is a quarter ellipse (or quarter circle, if of same length) circumference.

      :arg p1: starting point.
      :type p1: :ref:`Point`

      :arg p2: helper point.
      :type p2: :ref:`Point`

      :arg p3: end point.
      :type p3: :ref:`Point`

      :rtype: :ref:`Point`
      :returns: the end point, ``p3``.

      Example: a filled quarter ellipse segment.

      .. image:: img_drawCurve.png

   .. method:: drawSector(center, point, angle, fullSector = True)

      Draw a circular sector, optionally connecting the arc to the circle's center (like a piece of pie).

      :arg center: the center of the circle.
      :type center: :ref:`Point`

      :arg point: one of the two end points of the pie's arc segment. The other one is calculated from the ``angle``.
      :type point: :ref:`Point`

      :arg float angle: the angle of the sector in degrees. Used to calculate the other end point of the arc. Depending on its sign, the arc is drawn counter-clockwise (postive) or clockwise.

      :arg bool fullSector: whether to draw connecting lines from the ends of the arc to the circle center. If a fill color is specified, the full "pie" is colored, otherwise just the sector.

      :returns: the other end point of the arc. Can be used as starting point for a following invocation to create logically connected pies charts.
      :rtype: :ref:`Point`

      Examples:

      .. image:: img_drawSector1.png

      .. image:: img_drawSector2.png


   .. method:: drawRect(rect)

      Draw a rectangle. The drawing starts and ends at the top-left corner in a counter-clockwise movement.
      
      :arg rect: where to put the rectangle on the page.
      :type rect: :ref:`Rect`

      :rtype: :ref:`Point`
      :returns: ``rect.top_left`` (top-left corner of the rectangle).

   .. method:: insertText(point, text, fontsize = 11, fontname = "Helvetica", fontfile = None, idx = 0, set_simple = False, color = (0, 0, 0), rotate = 0, morph = None)

      Insert text lines beginning at a :ref:`Point` ``point``.

      :arg point: the bottom-left position of the first ``text`` character in pixels. ``point.x`` specifies the distance from left border, ``point.y`` the distance from top of page. This is independent from text orientation as requested by ``rotate``. However, there must always be sufficient room "above", which can mean the distance from any of the four page borders.
      :type point: :ref:`Point`

      :arg text: the text to be inserted. May be specified as either a string type or as a sequence type. For sequences, or strings containing line breaks ``\n``, several lines will be inserted. No care will be taken if lines are too wide, but the number of inserted lines will be limited by "vertical" space on the page (in the sense of reading direction as established by the ``rotate`` parameter). Any rest of ``text`` is discarded - the return code however contains the number of inserted lines. Only single byte character codes are currently supported.
      :type text: str or sequence

      :arg int rotate: determines whether to rotate the text. Acceptable values are multiples of 90 degrees. Default is 0 (no rotation), meaning horizontal text lines oriented from left to right. 180 means text is shown upside down from **right to left**. 90 means counter-clockwise rotation, text running **upwards**. 270 (or -90) means clockwise rotation, text running **downwards**. In any case, ``point`` specifies the bottom-left coordinates of the first character's rectangle. Multiple lines, if present, always follow the reading direction established by this parameter. So line 2 is located **above** line 1 in case of ``rotate = 180``, etc.

      :rtype: int
      :returns: number of lines inserted.

      For a description of the other parameters see :ref:`CommonParms`.

   .. method:: insertTextbox(rect, buffer, fontsize = 11, fontname = "Helvetica", fontfile = None, idx = 0, set_simple = False, color = (0, 0, 0), expandtabs = 8, align = TEXT_ALIGN_LEFT, charwidths = None, rotate = 0, morph = None)

      PDF only: Insert text into the specified rectangle. The text will be split into lines and words and then filled into the available space, starting from one of the four rectangle corners, depending on ``rotate``. Line feeds will be respected as well as multiple spaces will be.

      :arg rect: the area to use. It must be finite, not empty and completely contained in the page.
      :type rect: :ref:`Rect`

      :arg buffer: the text to be inserted. Must be specified as a string or a sequence of strings. Line breaks are respected also when occurring in a sequence entry.
      :type text: str or sequence

      :arg int align: align each text line. Default is 0 (left). Centered, right and justified are the other supported options, see :ref:`TextAlign`.

      :arg int expandtabs: controls handling of tab characters ``\t`` using the ``string.expandtabs()`` method **per each line**.

      :arg sequence charwidths: specify a sequence of character widths (floats) for the specified font. If omitted, it will be created by the function on **each invocation**. For performance, provide this parameter if you insert several text boxes with the same font. Use low-level function :meth:`Document._getCharWidths` to create one. Only single byte character codes are currently supported. Results are unpredictable, if larger codes occur (and the ``charwidths`` sequence is longer than 256).

      :arg int rotate: requests text to be rotated in the rectangle. This value must be a multiple of 90 degrees. Default is 0 (no rotation). Effectively, four different values are processed: 0, 90, 180 and 270 (= -90), each causing the text to start in a different rectangle corner. Bottom-left is 90, bottom-right is 180, and -90 / 270 is top-right. See the example how text is filled in a rectangle.

      :rtype: float
      :returns:
          **If positive or zero**: successful execution. The value returned is the unused rectangle space in pixels. This may safely be ignored - or be used to optimize the rectangle, position subsequent items, etc.

          **If negative**: no execution. The value returned is the space deficit to store the text. Enlarge rectangle, decrease ``fontsize``, decrease text amount, etc.

      .. image:: img_rotate.png

      For a description of the other parameters see :ref:`CommonParms`.

   .. method:: finish(width = 1, color = (0, 0, 0), fill = None, roundCap = True, dashes = None, closePath = True, even_odd = False, morph = (pivot, matrix))

      Finish a set of ``draw*()`` methods by applying :ref:`CommonParms` to all of them. This method also supports morphing the resulting compound drawing using a pivotal :ref:`Point`.

      :arg sequence morph: morph the compound drawing around some arbitrary pivotal :ref:`Point` ``pivot`` by applying :ref:`Matrix` ``matrix`` to it. Default is no morphing (``None``). The matrix can contain any values in its first 4 components, ``matrix.e == matrix.f == 0`` must be true, however. This means that any combination of scaling, shearing, rotating, flipping, etc. is possible, but translations are not.

      :arg bool even_odd: request the **"even-odd rule"** for filling operations. Default is ``False``, so that the **"nonzero winding number rule"** is used. These rules are alternative methods to apply the fill color where areas overlap. Only with fairly complex shapes a different behavior is to be expected with these rules. For an in-depth explanation, see :ref:`AdobeManual`, pp. 232 ff. Here is an example to demonstrate the difference.

      .. image:: even-odd.png

      .. note:: Method **"even-odd"** counts the number of overlaps of areas. Pixels in areas overlapping an odd number of times are regarded **inside**, otherwise **outside**. In contrast, the default method **"nonzero winding"** also looks at the area orientation: it counts ``+1`` if an area is drawn counter-clockwise and ``-1`` else. If the result is zero,the pixel is regarded **outside**, otherwise **inside**. In the top two shapes, three circles are drawn in standard manner (anti-clockwise, look at the arrows). The lower two shapes contain one (top-left) circle drawn clockwise. As can be seen, area orientation is irrelevant for the even-odd rule.

   .. method:: commit(overlay = True)

      Update the page's ``/Contents`` with the accumulated drawing commands. If a ``Shape`` is not committed, the page will not be changed. The method must be preceeded with at least one ``finish()`` or text insertion method.

      :arg bool overlay: determine whether to put the drawing in foreground (default) or background. Relevant only, if the page has a non-empty ``/Contents`` object.

   .. attribute:: doc

      For reference only: the page's document.

      :type: :ref:`Document`

   .. attribute:: page

      For reference only: the owning page.

      :type: :ref:`Page`

   .. attribute:: height

      Copy of the page's height

      :type: float

   .. attribute:: width

      Copy of the page's width.

      :type: float

   .. attribute:: contents

      Accumulated command buffer for draw methods since last finish.

      :type: str

   .. attribute:: totalcont

      Total accumulated command buffer for draws and text insertions. This will be used by :meth:`Shape.commit`.

      :type: str

   .. attribute:: lastPoint

      For reference only: the current point of the drawing path. It is ``None`` at ``Shape`` creation and after each ``finish()`` and ``commit()``.

      :type: :ref:`Point`

Usage
------
A drawing object is constructed by ``img = page.newShape()``. After this, as many draw, finish and text insertions methods as required may follow. Each sequence of draws must be finished before the drawing is committed. The overall coding pattern looks like this:

>>> img = page.newShape()
>>> img.draw1(...)
>>> img.draw2(...)
>>> ...
>>> img.finish(width=..., color = ..., fill = ..., morph = ...)
>>> img.draw3(...)
>>> img.draw4(...)
>>> ...
>>> img.finish(width=..., color = ..., fill = ..., morph = ...)
>>> ...
>>> img.insertText*
>>> ...
>>> img.commit()
>>> ....

Notes
~~~~~~
1. Each ``finish()`` combines the preceding draws into one logical shape, giving it common colors, line width, morphing, etc. If ``closePath`` is specified, it will also connect the end point of the last draw with the starting point of the first one.

2. To successfully create compound graphics, let each draw method use the end point of the previous one as its starting point. In the above pseudo code, ``draw2`` should hence use the returned :ref:`Point` of ``draw1`` as its starting point. Failing to do so, would automatically start a new path and ``finish()`` may not work as expected (but it won't complain either).

3. Text insertions may occur anywhere before the commit (they neither touch :attr:`Shape.contents` nor :attr:`Shape.lastPoint`). They are appended to ``Shape.totalcont`` directly, whereas draws will be appended by ``Shape.finish``.

4. Each ``commit`` takes all text insertions and shapes and places them in foreground or background on the page - thus providing a way to control graphical layers.

5. Only ``commit`` will update the page's contents, the other methods are basically string manipulations. With many draw / text operations, this will result in a much better performance, than issuing the corresponding page methods separately (they each do their own commit).

Examples
---------
1. Create a full circle of pieces of pie in different colors.

>>> img  = page.newShape()       # start a new shape
>>> cols = (...)                 # a sequence of RGB color triples
>>> pieces = len(cols)           # number of pieces to draw
>>> beta = 360. / pieces         # angle of each piece of pie
>>> center = fitz.Point(...)     # center of the pie
>>> p0     = fitz.Point(...)     # starting point
>>> for i in range(pieces):
        p0 = img.drawSector(center, p0, beta,
                            fullSector = True) # draw piece
        # now fill it but do not connect ends of the arc
        img.finish(fill = cols[i], closePath = False)
>>> img.commit()                 # update the page

Here is an example for 5 colors:

.. image:: img_cake.png

2. Create a regular n-edged polygon (fill yellow, red border). We use ``drawSector()`` only to calculate the points on the circumference, and empty the draw command buffer before drawing the polygon.

>>> img  = page.newShape()       # start a new shape
>>> beta = -360.0 / n            # our angle, drawn clockwise
>>> center = fitz.Point(...)     # center of circle
>>> p0     = fitz.Point(...)     # start here (1st edge)
>>> points = [p0]                # store polygon edges
>>> for i in range(n):           # calculate the edges
        p0 = img.drawSector(center, p0, beta)
        points.append(p0)
>>> img.contents = ""            # do not draw the circle sectors
>>> img.drawPolyline(points)     # draw the polygon
>>> img.finish(color = (1,0,0), fill = (1,1,0), closePath = False)
>>> img.commit()

Here is the polygon for n = 7:

.. image:: img_7edges.png

.. _CommonParms:

Common Parameters
-------------------

**fontname** (*str*)

  In general, there are three options:

  1. Use one of the standard :ref:`Base-14-Fonts`. In this case, ``fontfile`` **must not** be specified and ``"Helvetica"`` is used if this parameter is omitted, too.
  2. Choose a font already in use by the page. Then specify its **reference** name prefixed with a slash "/", see example below.
  3. Specify a font file present on your system. In this case choose an arbitrary, but new name for this parameter (without "/" prefix).

  If inserted text should re-use one of the page's fonts, use its reference name appearing in :meth:`getFontList` like so:
  
  Suppose the font list has the entry ``[1024, 0, 'Type1', 'CJXQIC+NimbusMonL-Bold', 'R366']``, then specify ``fontname = "/R366", fontfile = None`` to use font ``CJXQIC+NimbusMonL-Bold``.

----

**fontfile** (*str*)

  File path of a font existing on your computer. If you specify ``fontfile``, make sure you use a ``fontname`` **not occurring** in the above list. This new font will be embedded in the PDF upon ``doc.save()``. Similar to new images, a font file will be embedded only once. A table of MD5 codes for the binary font contents is used to ensure this.

----

**idx** (*int*)

  Font files may contain more than one font. Use this parameter to select the right one. This setting cannot be reverted. Subsequent changes are ignored.

----

**set_simple** (*bool*)

  Fonts installed from files are installed as **Type0** fonts by default. If you want to use 1-byte characters only, set this to true. This setting cannot be reverted. Subsequent changes are ignored.

----

**fontsize** (*float*)

  Font size of text. This also determines the line height as ``fontsize * 1.2``.

----

**dashes** (*str*)

  Causes lines to be dashed. A continuous line with no dashes is drawn with ``"[]0"`` or ``None``. For (the rather complex) details on how to achieve dashing effects, see :ref:`AdobeManual`, page 217. Simple versions look like ``"[3 4]"``, which means dashes of 3 and gaps of 4 pixels length follow each other. ``"[3 3]"`` and ``"[3]"`` do the same thing.

----

**color / fill** (*list, tuple*)

  Line and fill colors are always specified as RGB triples of floats from 0 to 1. To simplify color specification, method ``getColor()`` in ``fitz.utils`` may be used. It accepts a string as the name of the color and returns the corresponding triple. The method knows over 540 color names - see section :ref:`ColorDatabase`.

----

**overlay** (*bool*)

  Causes the item to appear in foreground (default) or background.

----

**morph** (*sequence*)

  Causes "morphing" of either a shape, created by the ``draw*()`` methods, or the text inserted by page methods ``insertTextbox()`` / ``insertText()``. If not ``None``, it must be a pair ``(pivot, matrix)``, where ``pivot`` is a :ref:`Point` and ``matrix`` is a :ref:`Matrix`. The matrix can be anything except translations, i.e. ``matrix.e == matrix.f == 0`` must be true. The point is used as a pivotal point for the matrix operation. For example, if ``matrix`` is a rotation or scaling operation, then ``pivot`` is its center. Similarly, if ``matrix`` is a left-right or up-down flip, then the mirroring axis will be the vertical, respectively horizontal line going through ``pivot``, etc.

  .. note:: Several methods contain checks whether the to be inserted items will actually fit into the page (like :meth:`Shape.insertText`, or :meth:`Shape.drawRect`). For the result of a morphing operation there is however no such guaranty: this is entirely the rpogrammer's responsibility.

----

**roundCap** (*bool*)

  Cause lines, dashes and edges to be rounded (default). If false, sharp edges and square line and dashes ends will be generated. Rounded lines / dashes will end in a semi-circle with a diameter equal to line width and make longer by the radius of this semi-circle.

----

**closePath** (*bool*)

  Causes the end point of a drawing to be automatically connected with the starting point (by a straight line).

