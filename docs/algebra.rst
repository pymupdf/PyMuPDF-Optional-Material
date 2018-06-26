.. _Algebra:

Operator Algebra for Geometry Objects
======================================
Instances of classes :ref:`Point`, :ref:`IRect`, :ref:`Rect` and :ref:`Matrix` are collectively also called "geometry" objects.

We have defined operators for these classes that allow dealing with them (almost) like ordinary numbers in terms of addition, subtraction, multiplication, division, and some others.

This chapter is a synopsis of what is possible.

General Remarks
-----------------
1. Operators can be either **binary** (i.e. involving two objects) or **unary**.

2. The result of **binary** operatorions is either a **new object** of the same class as the **left operand** or a bool.

3. The result of **unary** operations is either a **new object** of the same class, a bool or a float.

4. ``+, -, *, /`` are defined for all classes. They do what you would expect from them.

5. Rectangles have two additional binary operators: ``&`` (intersection) and ``|`` (union).

6. Binary operators fully support in-place operations: if ``"°"`` denotes any binary operator, then ``a °= b`` is the same as ``a = a ° b``.

7. For binary operations, the **second** operand may have a different type as the left one. Python number sequences (lists, tuples, arrays) are also allowed here. We allude to this fact by saying "point-like object" when we mean, that a :ref:`Point` is possible as well as a sequence of two numbers. Similar applies to "rect-like" (sequence length 4) or "matrix-like" (sequence length 6).

Unary Operations
------------------

+---------------+---------------------------------------------------------------+
| **Operation** | **Result**                                                    |
+===============+===============================================================+
| bool(o)       | is false if and only if the components of ``o`` are all zero. |
|               |                                                               |
+---------------+---------------------------------------------------------------+
| abs(o)        | is the Euclidean norm (square root of the sum of component    |
|               | squares), if ``o`` is a :ref:`Point` or a :ref:`Matrix`.      |
|               | For rectangles, its area is returned.                         |
|               |                                                               |
+---------------+---------------------------------------------------------------+
| +o            | is a copy of ``o``                                            |
+---------------+---------------------------------------------------------------+
| -o            | is a copy of ``o`` with negated components.                   |
|               |                                                               |
+---------------+---------------------------------------------------------------+
| ~m            | is the inverse of :ref:`Matrix` ``m``.                        |
|               |                                                               |
+---------------+---------------------------------------------------------------+



Binary Operations
------------------
For the operators ``+, -, *, /``, the **second operand** may be a number, which will be applied to each component. Otherwise:

+---------------+---------------------------------------------------------------+
| **Operation** | **Result**                                                    |
+===============+===============================================================+
|         a + b |                                                               |
|               | component-wise execution, ``b`` must be ``a``\ -like.         |
|         a - b |                                                               |
+---------------+---------------------------------------------------------------+
|         a * m | ``a`` can be any geometry object and ``m`` must matrix-like.  |
|               | If ``a`` is a **point** or a **rectangle**, then              |
|         a / m | ``a.transform(m)``, resp. ``a.transform(~m)`` is executed.    |
|               | If ``a`` is a **matrix**, then ``a * m``,                     |
|               | resp. ``a * ~m`` is executed.                                 |
+---------------+---------------------------------------------------------------+
|         a & b | **intersection rectangle:** ``a`` must be a rectangle and     |
|               | ``b`` rect-like.                                              |
|               | Delivers the **largest rectangle**                            |
|               | contained in both operands.                                   |
+---------------+---------------------------------------------------------------+
|         a | b | **union rectangle:** ``a`` must be a rectangle, and ``b``     |
|               | can be point-like or rect-like.                               |
|               | Delivers the **smallest rectangle** containing both operands. |
+---------------+---------------------------------------------------------------+
|      "b in a" | if ``b`` is a number, then ``b in tuple(a)`` is returned.     |
|               | If ``b`` is point-like or rect-like, then ``a`` must be       |
|               | a rectangle, and the result of ``a.contains(b)`` is returned. |
+---------------+---------------------------------------------------------------+
|        a == b | is true if ``abs(a - b) == 0`` and ``type(a) == type(b)``     |
|               | (but maybe there is ``id(a) != id(b)``).                      |
+---------------+---------------------------------------------------------------+

