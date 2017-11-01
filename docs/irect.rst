.. _IRect:

==========
IRect
==========

IRect is a rectangular bounding box similar to :ref:`Rect`, except that all corner coordinates are integers. IRect is used to specify an area of pixels, e.g. to receive image data during rendering. Otherwise, many similarities exist, e.g. considerations concerning emptiness and finiteness of rectangles also apply to ``IRects``.

============================== ===========================================
**Attribute / Method**          **Short Description**
============================== ===========================================
:meth:`IRect.contains`         checks containment of another object
:meth:`IRect.getArea`          calculate rectangle area
:meth:`IRect.getRect`          return a :ref:`Rect` with same coordinates
:meth:`IRect.getRectArea`      calculate rectangle area
:meth:`IRect.intersect`        common part with another rectangle
:meth:`IRect.intersects`       checks for non-empty intersection
:meth:`IRect.normalize`        makes a rectangle finite
:meth:`IRect.translate`        shift rectangle
:attr:`IRect.bottom_left`      bottom left point, synonym ``bl``
:attr:`IRect.bottom_right`     bottom right point, synonym ``br``
:attr:`IRect.height`           height of the rectangle
:attr:`IRect.isEmpty`          whether rectangle is empty
:attr:`IRect.isInfinite`       whether rectangle is infinite
:attr:`IRect.rect`             equals result of method ``getRect()``
:attr:`IRect.top_left`         top left point, synonym ``tl``
:attr:`IRect.top_right`        top_right point, synonym ``tr``
:attr:`IRect.width`            width of the rectangle
:attr:`IRect.x0`               X-coordinate of the top left corner
:attr:`IRect.x1`               X-coordinate of the bottom right corner
:attr:`IRect.y0`               Y-coordinate of the top left corner
:attr:`IRect.y1`               Y-coordinate of the bottom right corner
============================== ===========================================

**Class API**

.. class:: IRect

   .. method:: __init__(self)

   .. method:: __init__(self, x0, y0, x1, y1)

   .. method:: __init__(self, irect)

   .. method:: __init__(self, list)

      Overloaded constructors. Also see examples below and those for the :ref:`Rect` class.

      If another ``irect`` is specified, a **new copy** will be made.

      If ``list`` is specified, it must be a Python sequence type of 4 integers. Non-integer numbers will be truncated, non-numeric entries will be replaced with ``-1``.

      The other parameters mean integer coordinates.

   .. method:: getRect()

      A convenience function returning a :ref:`Rect` with the same coordinates as floating point values.

      :rtype: :ref:`Rect`

   .. method:: getRectArea([unit])

   .. method:: getArea([unit])

      Calculates the area of the rectangle and, with no parameter, equals ``abs(IRect)``. Like an empty rectangle, the area of an infinite rectangle is also zero.

      :arg str unit: Specify required unit: respective squares of ``px`` (pixels, default), ``in`` (inches), ``cm`` (centimeters), or ``mm`` (millimeters).

      :rtype: float

   .. method:: intersect(ir)

      The intersection (common rectangular area) of the current rectangle and ``ir`` is calculated and replaces the current rectangle. If either rectangle is empty, the result is also empty. If one of the rectangles is infinite, the other one is taken as the result - and hence also infinite if both rectangles were infinite.

      :arg ir: Second rectangle.
      :type ir: :ref:`IRect`

   .. method:: translate(tx, ty)

      Modifies the rectangle to perform a shift in x and / or y direction.

      :arg int tx: Number of pixels to shift horizontally. Negative values mean shifting left.

      :arg int ty: Number of pixels to shift vertically. Negative values mean shifting down.

   .. method:: contains(x)

      Checks whether ``x`` is contained in the rectangle. It may be an ``IRect``, ``Rect``,``Point`` or number. If ``x`` is an empty rectangle, this is always true. Conversely, if the rectangle is empty this is always ``False``, if ``x`` is not an empty rectangle and not a number. If ``x`` is a number, it will be checked to be one of the four components. ``x in irect`` and ``irect.contains(x)`` are equivalent.

      :arg x: the object to check.
      :type x: :ref:`IRect` or :ref:`Rect` or :ref:`Point` or int

      :rtype: bool

   .. method:: intersects(r)

      Checks whether the rectangle and ``r`` (``IRect`` or :ref:`Rect`) have a non-empty rectangle in common. This will always be ``False`` if either is infinite or empty.
      
      :arg r: the rectangle to check.
      :type r: :ref:`IRect` or :ref:`Rect`

      :rtype: bool

   .. method:: normalize()

      Makes sure the rectangle is finite. This is done by shuffling the rectangle corners. After completion of this method, the bottom right corner will indeed be south-eastern to the top left one. See :ref:`Rect` for a more detailed discussion on rectangle properties.
      
   .. attribute:: top_left

   .. attribute:: tl

      Equals ``Point(x0, y0)``.

      :type: :ref:`Point`

   .. attribute:: top_right

   .. attribute:: tr

      Equals ``Point(x1, y0)``.

      :type: :ref:`Point`

   .. attribute:: bottom_left

   .. attribute:: bl

      Equals ``Point(x0, y1)``.

      :type: :ref:`Point`

   .. attribute:: bottom_right

   .. attribute:: br

      Equals ``Point(x1, y1)``.

      :type: :ref:`Point`

   .. attribute:: width

      Contains the width of the bounding box. Equals ``x1 - x0``.

      :type: int

   .. attribute:: height

      Contains the height of the bounding box. Equals ``y1 - y0``.

      :type: int

   .. attribute:: x0

      X-coordinate of the left corners.

      :type: int

   .. attribute:: y0

      Y-coordinate of the top corners.

      :type: int

   .. attribute:: x1

      X-coordinate of the right corners.

      :type: int

   .. attribute:: y1

      Y-coordinate of the bottom corners.

      :type: int

   .. attribute:: isInfinite

      ``True`` if rectangle is infinite, ``False`` otherwise.

      :type: bool

   .. attribute:: isEmpty

      ``True`` if rectangle is empty, ``False`` otherwise.

      :type: bool


Remark
------
A rectangle's coordinates can also be accessed via index, e.g. ``r.x0 == r[0]``, and the ``tuple()`` and ``list()`` functions yield sequence objects of its components.

IRect Algebra
------------------
For a general background, please see chapter :ref:`Algebra`.

Examples
---------
Algebra provides handy ways to perform inclusion and intersection checks between Rects, IRects and Points.

**Example 1:**
::
  >>> ir = fitz.IRect(10, 10, 410, 610)
  >>> ir
  fitz.IRect(10, 10, 410, 610)
  >>> ir.height
  600
  >>> ir.width
  400
  >>> ir.getArea('mm')     # calculate area in square millimeters
  29868.51852

**Example 2:**
::
  >>> m = fitz.Matrix(45)
  >>> ir = fitz.IRect(10, 10, 410, 610)
  >>> ir * m                          # rotate rectangle by 45 degrees
  fitz.IRect(-425, 14, 283, 722)
  >>>
  >>> ir | fitz.Point(5, 5)           # enlarge rectangle to contain a point
  fitz.IRect(5, 5, 410, 610)
  >>>
  >>> ir + 5                          # shift the rect by 5 points
  fitz.IRect(15, 15, 415, 615)
  >>>
  >>> ir & fitz.Rect(0.0, 0.0, 15.0, 15.0)
  fitz.IRect(10, 10, 15, 15)

**Example 3:**
::
  >>> # test whether two rectangle are disjoint
  >>> if not r1.intersects(r2): print("disjoint rectangles")
  >>>
  >>> # test whether r2 containes x (x is point-like or rect-like)
  >>> if r2.contains(x): print("x is contained in r2")
  >>>
  >>> # or even simpler:
  >>> if x in r2: print("x is contained in r2")
