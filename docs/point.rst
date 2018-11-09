.. _Point:

================
Point
================

``Point`` represents a point in the plane, defined by its x and y coordinates.

============================ ============================================
**Attribute / Method**       **Description**
============================ ============================================
:meth:`Point.distance_to`    calculate distance to point or rect
:meth:`Point.transform`      transform point with a matrix
:attr:`Point.abs_unit`       same as unit, but positive coordinates
:attr:`Point.unit`           point coordinates divides by abs(point)
:attr:`Point.x`              the X-coordinate
:attr:`Point.y`              the Y-coordinate
============================ ============================================

**Class API**

.. class:: Point

   .. method:: __init__(self)

   .. method:: __init__(self, x, y)

   .. method:: __init__(self, point)

   .. method:: __init__(self, sequence)

      Overloaded constructors.
      
      Without parameters, ``Point(0, 0)`` will be created.

      With another point specified, a **new copy** will be crated, "sequence" must be Python sequence object of 2 floats (see :ref:`SequenceTypes`).

     :arg float x: x coordinate of the point

     :arg float y: y coordinate of the point

   .. method:: distance_to(x [, unit])

      Calculates the distance to ``x``, which may be a :ref:`Rect`, :ref:`IRect` or :ref:`Point`. The distance is given in units of either ``px`` (pixels, default), ``in`` (inches), ``mm`` (millimeters) or ``cm`` (centimeters).

      .. note:: If ``x`` is a rectangle, the distance is calculated to the finite version of it.

     :arg x: the object to which the distance is calculated.
     :type `x`: :ref:`Rect` or :ref:`IRect` or :ref:`Point`

     :arg str unit: the unit to be measured in. One of ``px``, ``in``, ``cm``, ``mm``.

     :returns: distance to object ``x``.
     :rtype: float

   .. method:: transform(m)

      Applies matrix ``m`` to the point and replaces it with the result.

     :arg m: The matrix to be applied.
     :type m: :ref:`Matrix`

     :rtype: :ref:`Point`

   .. attribute:: unit

      Result of dividing the coordinates by ``abs(point)``. This results in a vector of length 1 pointing in the same direction as the point does. Its x, resp. y values are equal to the cosine, resp. sine of the angle this vector (and the point itself) has with the x axis.

      :type: :ref:`Point`

   .. attribute:: abs_unit

      Same as :attr:`unit` above, replacing the coordinates with their absolute values.

      :type: :ref:`Point`

   .. attribute:: x

      The x coordinate

      :type: float

   .. attribute:: y

      The y coordinate

      :type: float

Remark
------
This class adheres to the sequence protocol, so components can be manipulated via their index. Also refer to :ref:`SequenceTypes`.

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
>>>
>>> fitz.Point(1, 2) / (1, 2, 3, 4, 5, 6)
fitz.Point(2.0, -2.0)
