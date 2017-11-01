.. _Rect:

==========
Rect
==========

``Rect`` represents a rectangle defined by four floating point numbers x0, y0, x1, y1. They are viewed as being coordinates of two diagonally opposite points. The first two numbers are regarded as the "top left" corner P\ :sub:`x0,y0` and P\ :sub:`x1,y1` as the "bottom right" one. However, these two properties need not coincide with their ostensive meanings - read on.

The following remarks are also valid for :ref:`IRect` objects:

* Rectangle borders are always parallel to the respective X- and Y-axes.
* The constructing points can be anywhere in the plane - they need not even be different, and e.g. "top left" need not be the geometrical "north-western" point.
* For any given quadruple of numbers, the geometrically "same" rectangle can be defined in (up to) four different ways: Rect(P\ :sub:`x0,y0`, P\ :sub:`x1,y1`\ ), Rect(P\ :sub:`x1,y1`, P\ :sub:`x0,y0`\ ), Rect(P\ :sub:`x0,y1`, P\ :sub:`x1,y0`\ ), and Rect(P\ :sub:`x1,y0`, P\ :sub:`x0,y1`\ ).

Hence some useful classification:

* A rectangle is called **finite** if ``x0 <= x1`` and ``y0 <= y1`` (i.e. the bottom right point is "south-eastern" to the top left one), otherwise **infinite**. Of the four alternatives above, only one is finite (disregarding degenerate cases).

* A rectangle is called **empty** if ``x0 = x1`` or ``y0 = y1``, i.e. if its area is zero.

.. note:: As paradox as it may sound: a rectangle can be both, infinite **and** empty ...

============================= =======================================================
**Methods / Attributes**      **Short Description**
============================= =======================================================
:meth:`Rect.contains`         checks containment of another object
:meth:`Rect.getArea`          calculate rectangle area
:meth:`Rect.getRectArea`      calculate rectangle area
:meth:`Rect.includePoint`     enlarge rectangle to also contain a point
:meth:`Rect.includeRect`      enlarge rectangle to also contain another one
:meth:`Rect.intersect`        common part with another rectangle
:meth:`Rect.intersects`       checks for non-empty intersections
:meth:`Rect.normalize`        makes a rectangle finite
:meth:`Rect.round`            create smallest :ref:`Irect` containing rectangle
:meth:`Rect.transform`        transform rectangle with a matrix
:attr:`Rect.bottom_left`      bottom left point, synonym ``bl``
:attr:`Rect.bottom_right`     bottom right point, synonym ``br``
:attr:`Rect.height`           rectangle height
:attr:`Rect.irect`            equals result of method ``round()``
:attr:`Rect.isEmpty`          whether rectangle is empty
:attr:`Rect.isInfinite`       whether rectangle is infinite
:attr:`Rect.top_left`         top left point, synonym ``tl``
:attr:`Rect.top_right`        top_right point, synonym ``tr``
:attr:`Rect.width`            rectangle width
:attr:`Rect.x0`               top left corner's X-coordinate
:attr:`Rect.x1`               bottom right corner's X-coordinate
:attr:`Rect.y0`               top left corner's Y-coordinate
:attr:`Rect.y1`               bottom right corner's Y-coordinate
============================= =======================================================

**Class API**

.. class:: Rect

   .. method:: __init__(self)

   .. method:: __init__(self, x0, y0, x1, y1)

   .. method:: __init__(self, top_left, bottom_right)

   .. method:: __init__(self, top_left, x1, y1)

   .. method:: __init__(self, x0, y0, bottom_right)

   .. method:: __init__(self, rect)

   .. method:: __init__(self, list)

      Overloaded constructors: ``top_left``, ``bottom_right`` stand for :ref:`Point` objects, ``list`` is a Python sequence type with length 4, ``rect`` means another ``Rect``, while the other parameters mean float coordinates. If ``list`` is specified, it is the user's responsibility to only provide numeric entries - **no error checking is done**, and invalid entries will receive a value of ``-1.0``.

      If ``rect`` is specified, the constructor creates a **new copy** of ``rect``.

      Without parameters, the rectangle ``Rect(0.0, 0.0, 0.0, 0.0)`` is created.

   .. method:: round()

      Creates the smallest containing :ref:`IRect` (this is **not** the same as simply rounding the rectangle's edges!).
      
      1. If the rectangle is **infinite**, the "normalized" (finite) version of it will be taken. The result of this method is always a finite ``IRect``.
      2. If the rectangle is **empty**, the result is also empty.
      3. **Possible paradox:** The result may be empty, **even if** the rectangle is **not** empty! In such cases, the result obviously does **not** contain the rectangle. This is because MuPDF's algorithm allows for a small tolerance (1e-3). Example:

      >>> r = fitz.Rect(100, 100, 200, 100.001)
      >>> r.isEmpty
      False
      >>> r.round()
      fitz.IRect(100, 100, 200, 100)
      >>> r.round().isEmpty
      True

      To reproduce the effect on your platform, you may need to adjust the numbers a little.

      :rtype: :ref:`IRect`

   .. method:: transform(m)

      Transforms the rectangle with a matrix and **replaces the original**. If the rectangle is empty or infinite, this is a no-operation.

      :arg m: The matrix for the transformation.
      :type m: :ref:`Matrix`

      :rtype: ``Rect``
      :returns: the smallest rectangle that contains the transformed original.

   .. method:: intersect(r)

      The intersection (common rectangular area) of the current rectangle and ``r`` is calculated and **replaces the current** rectangle. If either rectangle is empty, the result is also empty. If ``r`` is infinite, this is a no-operation.

      :arg r: Second rectangle
      :type r: :ref:`Rect`

   .. method:: includeRect(r)

      The smallest rectangle containing the current one and ``r`` is calculated and **replaces the current** one. If either rectangle is infinite, the result is also infinite. If one is empty, the other one will be taken as the result.

      :arg r: Second rectangle
      :type r: :ref:`Rect`

   .. method:: includePoint(p)

      The smallest rectangle containing the current one and point ``p`` is calculated and **replaces the current** one. **Infinite rectangles remain unchanged.** To create a rectangle containing a series of points, start with (the empty) ``fitz.Rect(p1, p1)`` and successively perform ``includePoint`` operations for the other points.

      :arg p: Point to include.
      :type p: :ref:`Point`

   .. method:: getRectArea([unit])

   .. method:: getArea([unit])

      Calculate the area of the rectangle and, with no parameter, equals ``abs(rect)``. Like an empty rectangle, the area of an infinite rectangle is also zero. So, at least one of ``fitz.Rect(p1, p2)`` and ``fitz.Rect(p2, p1)`` has a zero area. 

      :arg str unit: Specify required unit: respective squares of ``px`` (pixels, default), ``in`` (inches), ``cm`` (centimeters), or ``mm`` (millimeters).
      :rtype: float

   .. method:: contains(x)

      Checks whether ``x`` is contained in the rectangle. It may be an ``IRect``, ``Rect``, ``Point`` or number. If ``x`` is an empty rectangle, this is always true. If the rectangle is empty this is always ``False`` for all non-empty rectangles and for all points. If ``x`` is a number, it will be checked against the four components. ``x in rect`` and ``rect.contains(x)`` are equivalent.

      :arg x: the object to check.
      :type x: :ref:`IRect` or :ref:`Rect` or :ref:`Point` or number

      :rtype: bool

   .. method:: intersects(r)

      Checks whether the rectangle and ``r`` (a ``Rect`` or :ref:`IRect`) have a non-empty rectangle in common. This will always be ``False`` if either is infinite or empty.
      
      :arg r: the rectangle to check.
      :type r: :ref:`IRect` or :ref:`Rect`

      :rtype: bool

   .. method:: normalize()

      **Replace** the rectangle with its finite version. This is done by shuffling the rectangle corners. After completion of this method, the bottom right corner will indeed be south-eastern to the top left one.

   .. attribute:: irect

      Equals result of method ``round()``.

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

      Contains the width of the rectangle. Equals ``x1 - x0``.

      :rtype: float

   .. attribute:: height

      Contains the height of the rectangle. Equals ``y1 - y0``.

      :rtype: float

   .. attribute:: x0

      X-coordinate of the left corners.

      :type: float

   .. attribute:: y0

      Y-coordinate of the top corners.

      :type: float

   .. attribute:: x1

      X-coordinate of the right corners.

      :type: float

   .. attribute:: y1

      Y-coordinate of the bottom corners.

      :type: float

   .. attribute:: isInfinite

      ``True`` if rectangle is infinite, ``False`` otherwise.

      :type: bool

   .. attribute:: isEmpty

      ``True`` if rectangle is empty, ``False`` otherwise.

      :type: bool

Remark
------
A rectangle's coordinates can also be accessed via index, e.g. ``r.x0 == r[0]``, and the ``tuple()`` and ``list()`` functions yield sequence objects of its components.

Rect Algebra
-----------------
For a general background, see chapter :ref:`Algebra`.

Examples
----------

**Example 1 - different ways of construction:**

>>> p1 = fitz.Point(10, 10)
>>> p2 = fitz.Point(300, 450)
>>>
>>> fitz.Rect(p1, p2)
fitz.Rect(10.0, 10.0, 300.0, 450.0)
>>>
>>> fitz.Rect(10, 10, 300, 450)
fitz.Rect(10.0, 10.0, 300.0, 450.0)
>>>
>>> fitz.Rect(10, 10, p2)
fitz.Rect(10.0, 10.0, 300.0, 450.0)
>>>
>>> fitz.Rect(p1, 300, 450)
fitz.Rect(10.0, 10.0, 300.0, 450.0)

**Example 2 - what happens during rounding:**

>>> r = fitz.Rect(0.5, -0.01, 123.88, 455.123456)
>>>
>>> r
fitz.Rect(0.5, -0.009999999776482582, 123.87999725341797, 455.1234436035156)
>>>
>>> r.round()     # = r.irect
fitz.IRect(0, -1, 124, 456)

**Example 3 - inclusion and itersection:**

>>> m = fitz.Matrix(45)
>>> r = fitz.Rect(10, 10, 410, 610)
>>> r * m
fitz.Rect(-424.2640686035156, 14.142135620117188, 282.84271240234375, 721.2489013671875)
>>>
>>> r | fitz.Point(5, 5)
fitz.Rect(5.0, 5.0, 410.0, 610.0)
>>>
>>> r + 5
fitz.Rect(15.0, 15.0, 415.0, 615.0)
>>>
>>> r & fitz.Rect(0, 0, 15, 15)
fitz.Rect(10.0, 10.0, 15.0, 15.0)

**Example 4 - containment:**

>>> r = fitz.Rect(...)     # any rectangle
>>> ir = r.irect           # its IRect version
>>> # even though you get ...
>>> ir in r
True
>>> # ... and ...
>>> r in ir
True
>>> # ... r and ir are still different types!
>>> r == ir
False
>>> # corners are always part of non-epmpty rectangles
>>> r.bottom_left in r
True
>>>
>>> # numbers are checked against coordinates
>>> r.x0 in r
True

**Example 5 - create a finite copy:**

Create a copy that is **guarantied to be finite** in two ways:

>>> r = fitz.Rect(...)     # any rectangle
>>>
>>> # alternative 1
>>> s = fitz.Rect(r.top_left, r.top_left)   # just a point
>>> s | r.bottom_right     # s is a finite rectangle!
>>>
>>> # alternative 2
>>> s = (+r).normalize()
>>> # r.normalize() changes r itself!

**Example 6 - adding a Pytohn sequence:**

Enlarge rectangle by 5 pixels in every direction:

>>> r  = fitz.Rect(...)
>>> r1 = r + (-5, -5, 5, 5)