.. _Algebra:

Operator Algebra for Geometry Objects
======================================
Instances of classes :ref:`Point`, :ref:`IRect`, :ref:`Rect` and :ref:`Matrix` are collectively also called "geometry" objects.

They all are special cases of Python sequences, see :ref:`SequenceTypes` for more background.

We have defined operators for these classes that allow dealing with them (almost) like ordinary numbers in terms of addition, subtraction, multiplication, division, and some others.

This chapter is a synopsis of what is possible.

General Remarks
-----------------
1. Operators can be either **binary** (i.e. involving two objects) or **unary**.

2. The resulting type of **binary** operations is either a **new object** of the **left operand's class** or a bool.

3. The result of **unary** operations is either a **new object** of the same class, a bool or a float.

4. ``+, -, *, /`` are defined for all classes. They do what you would expect from them.

5. Rectangles have two additional binary operators: ``&`` (intersection) and ``|`` (union).

6. Binary operators fully support in-place operations: if ``"°"`` denotes any binary operator, then ``a °= b`` is the same as ``a = a ° b``.

7. For binary operations, the **second** operand may always be a number sequence of the same size as the left one. We allude to this fact by e.g. saying "x-like object" if a number sequence of same length as x is allowed.

Unary Operations
------------------

+---------+-----------------------------------------------------------------+
|         | **Result**                                                      |
+=========+=================================================================+
| bool(O) | is false exactly if all components of "O" are zero              |
+---------+-----------------------------------------------------------------+
| abs(O)  | the rectangle area -- equal to norm(O) for the other tyes       |
+---------+-----------------------------------------------------------------+
| norm(O) | square root of the component squares (Euclidean norm)           |
+---------+-----------------------------------------------------------------+
| +O      | new copy of "O"                                                 |
+---------+-----------------------------------------------------------------+
| -O      | new copy of "O" with negated components                         |
+---------+-----------------------------------------------------------------+
| ~m      | inverse of :ref:`Matrix` "m", or the null matrix if not defined |
+---------+-----------------------------------------------------------------+



Binary Operations
------------------
For every geometry object "a" and every number "b", the operations "a ° b" and "a °= b" are always defined if "°" is any of the operators ``+, -, *, /``. The respective operation is simply executed for each component of "a". If the second operand is **not a number**, then the following is defined:

+--------+---------------------------------------------------------------+
|        | **Result**                                                    |
+========+===============================================================+
| a+b,   | component-wise execution, "b" must be "a"-like.               |
| a-b    |                                                               |
+--------+---------------------------------------------------------------+
| a*m,   | "a" can be any geometry object and "m" must be matrix-like.   |
| a/m    | ``"a/m"`` is always treated as ``"a*~m"``.                    |
|        | If "a" is a **point** or a **rectangle**, then                |
|        | ``"a.transform(m)"`` is executed. If "a" is a matrix, then    |
|        | matrix concatenation takes place.                             |
+--------+---------------------------------------------------------------+
| a&b    | **intersection rectangle:** "a" must be a rectangle and       |
|        | "b" rect-like. Delivers the **largest rectangle**             |
|        | contained in both operands.                                   |
+--------+---------------------------------------------------------------+
| a|b    | **union rectangle:** "a" must be a rectangle, and "b"         |
|        | may be point-like or rect-like.                               |
|        | Delivers the **smallest rectangle** containing both operands. |
+--------+---------------------------------------------------------------+
| b in a | if "b" is a number, then ``"b in tuple(a)"`` is returned.     |
|        | If "b" is point-like or rect-like, then "a" must be a         |
|        | rectangle, and ``"a.contains(b)"`` is returned.               |
+--------+---------------------------------------------------------------+
| a==b   | ``True`` if ``bool(a-b)`` is ``False`` ("b" may be "a"-like). |
+--------+---------------------------------------------------------------+

.. note:: Please note an important difference to usual arithmetics:

            Matrix multiplication is **not commutative**, i.e. in general there is ``m * n != n * m`` for two matrices. Also, there are non-zero matrices which have no inverse, for example ``m = Matrix(1, 0, 1, 0, 1, 0)``. If you try to divide by any of these you will receive a ``ZeroDivisionError`` exception using operator ``"/"``, e.g. for ``fitz.Matrix(1, 1) / m``. If you formulate ``fitz.Matrix(1, 1) * ~m``, the result will be ``fitz.Matrix()`` (the null matrix).


Some Examples
--------------

Manipulation with numbers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
For the usual arithmetic operations, numbers are always allowed as second operand. In addition, you can formulate ``"x in OBJ"``, where x is a number and OBJ one of these objects. It is implemented as ``"x in tuple(OBJ)"``.

>>> fitz.Rect(1, 2, 3, 4) + 5
fitz.Rect(6.0, 7.0, 8.0, 9.0)
>>> 3 in fitz.Rect(1, 2, 3, 4)
True
>>> 

The following will create the upper left quarter of a document page rectangle:

>>> page.rect
Rect(0.0, 0.0, 595.0, 842.0)
>>> page.rect / 2
Rect(0.0, 0.0, 297.5, 421.0)
>>> 

The following will deliver the **middle point of a line** connecting two points p1 and p2:

>>> p1 = fitz.Point(1, 2)
>>> p2 = fitz.Point(4711, 3141)
>>> mp = p1 + (p2 - p1) / 2
>>> mp
Point(2356.0, 1571.5)
>>> 

Manipulation with "like" Objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The second operand of a binary operation can always be "like" the left operand. "Like" in this context means "a sequence of numbers of the same length". With the above examples:

>>> p1 + p2
Point(4712.0, 3143.0)
>>> p1 + (4711, 3141)
Point(4712.0, 3143.0)
>>> p1 += (4711, 3141)
>>> p1
Point(4712.0, 3143.0)
>>> 

To shift a rectangle for 5 pixels to the right, do this:

>>> fitz.Rect(100, 100, 200, 200) + (5, 0, 5, 0)
Rect(105.0, 100.0, 205.0, 200.0)
>>>

Points, rectangles and matrices can be *transformed* with matrices. In PyMuPDF, we treat this like a **"multiplication"** (or resp. **division**), where the second operand may be "like" a matrix. Division in this context means "multiplication with the matrix inverse". 

>>> m = fitz.Matrix(1, 2, 3, 4, 5, 6)
>>> n = fitz.Matrix(6, 5, 4, 3, 2, 1)
>>> p = fitz.Point(1, 2)
>>> p * m
Point(12.0, 16.0)
>>> p * (1, 2, 3, 4, 5, 6)
Point(12.0, 16.0)
>>> p / m
Point(2.0, -2.0)
>>> p / (1, 2, 3, 4, 5, 6)
Point(2.0, -2.0)
>>>
>>> m * n  # matrix multiplication
Matrix(14.0, 11.0, 34.0, 27.0, 56.0, 44.0)
>>> m / n  # matrix division
Matrix(2.5, -3.5, 3.5, -4.5, 5.5, -7.5)
>>>
>>> m / m  # result is equal to the Identity matrix
Matrix(1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
>>> 


As a specialty, rectangles support additional binary operations:

* **intersection** -- the common area of rectangle-likes, operator ``"&"``
* **inclusion** -- enlarge to include a point-like or rect-like, operator ``"|"``
* **containment** check -- whether a point-like or rect-like is inside

Here is an example for creating the smallest rectangle enclosing given points:

>>> # first define arbitrary point-likes
>>> for i in range(10):
        for j in range(10):
            points.append((i, j))
>>> # start with an empty rectangle
>>> r = fitz.Rect(points[0], points[0])
>>> for p in points[1:]:  # and include remaining points one by one
        r |= p
>>> r  # here is the to be expected result:
Rect(0.0, 0.0, 9.0, 9.0)
>>> (4, 5) in r  # this point-like lies inside the rectangle
True
>>> # and this rect-like is also inside
>>> (4, 4, 5, 5) in r
True
>>>

