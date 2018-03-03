.. _Point:

================
Point
================

``Point`` represents a point in the plane, defined by its x and y coordinates.

============================ ====================================
**Attribute / Method**       **Short Description**
============================ ====================================
:meth:`Point.distance_to`    calculate distance to point or rect
:meth:`Point.transform`      transform point with a matrix
:attr:`Point.x`              the X-coordinate
:attr:`Point.y`              the Y-coordinate
============================ ====================================

**Class API**

.. class:: Point

   .. method:: __init__(self)

   .. method:: __init__(self, x, y)

   .. method:: __init__(self, point)

   .. method:: __init__(self, list)

      Overloaded constructors.
      
      Without parameters, ``Point(0, 0)`` will be created.

      With another ``point`` specified, a **new copy** will be crated. A ``list`` must be Python sequence object of length 2. For a ``list``, it is the user's responsibility to only provide numeric entries - **no error checking is done**, and invalid entries will receive a value of ``-1.0``.

     :arg float x: X coordinate of the point

     :arg float y: Y coordinate of the point

   .. method:: distance_to(x [, unit])

      Calculates the distance to ``x``, which may be a :ref:`Rect`, :ref:`IRect` or :ref:`Point`. The distance is given in units of either ``px`` (pixels, default), ``in`` (inches), ``mm`` (millimeters) or ``cm`` (centimeters).

      .. note:: If ``x`` is a rectangle, the distance is calculated as if the rectangle were finite.

     :arg x: the object to which the distance is calculated.
     :type `x`: :ref:`Rect` or :ref:`IRect` or :ref:`Point`

     :arg str unit: the unit to be measured in. One of ``px``, ``in``, ``cm``, ``mm``.

     :returns: distance to object ``x``.
     :rtype: float

   .. method:: transform(m)

      Applies matrix ``m`` to the point.

     :arg m: The matrix to be applied.

     :rtype: ``Point``

  .. attribute:: x
     x Coordinate

  .. attribute:: y
     y Coordinate

Remark
------
A point's ``p`` attributes ``x`` and ``y`` can also be accessed as indices, e.g. ``p.x == p[0]``, and the ``tuple()`` and ``list()`` functions yield sequence objects of its components.

Point Algebra
------------------
For a general background, see chapter :ref:`Algebra`.

Examples
---------
This should illustrate some basic uses:

>>> fitz.Point(1, 2) * fitz.Matrix(90)
fitz.Point(-2.0, 1.0)
>>>
>>> fitz.Point(1, 2) * 3
fitz.Point(3.0, 6.0)
>>>
>>> fitz.Point(1, 2) + 3
fitz.Point(4.0, 5.0)
>>>
>>> fitz.Point(25, 30) + fitz.Point(1, 2)
fitz.Point(26.0, 32.0)
>>> fitz.Point(25, 30) + (1, 2)
fitz.Point(26.0, 32.0)
>>>
>>> fitz.Point([1, 2])
fitz.Point(1.0, 2.0)
>>>
>>> -fitz.Point(1, 2)
fitz.Point(-1.0, -2.0)
>>>
>>> abs(fitz.Point(25, 30))
39.05124837953327
