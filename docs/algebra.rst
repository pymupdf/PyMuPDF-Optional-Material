.. _Algebra:

Operator Algebra for Geometry Objects
======================================
Instances of classes :ref:`Point`, :ref:`IRect`, :ref:`Rect` and :ref:`Matrix` are collectively also called "geometry" objects.

We have defined operators for these classes that allow dealing with them (almost) like ordinary numbers in terms of addition, subtraction, multiplication, division, and some others.

This chapter is a synopsis of what is possible.

General Remarks
-----------------
1. Operators can be either **binary** (i.e. involving two objects) or **unary**.

2. The result of binary operatorions is either a **new object** of the same class as the **left operand** or a bool.

3. The result of unary operations is either a bool, a float or the same object type.

4. All binary operators fully support in-place operations, i.e. something like ``a °= b`` is equivalent to ``a = a ° b``.

5. The following binary operators are defined for all classes: ``+, -, *, /``. They have a similar meaning as the corresponding numerical ones.

6. Rectangles have additional binary operators ``&, |``, details below.

7. For binary operations, the **second** operand may have a different type as the left one. Often, Python sequences (lists, tuples, arrays) are also allowed here. We allude to this fact by saying "point-like object" when we mean, that a :ref:`Point` is possible as well as a sequence of two numbers. Similar applies to "rect-like" (sequence length 4) or "matrix-like" (sequence length 6).

Unary Operations
------------------
* ``bool(o)`` - is false if and only if the components of ``o`` are all zero.
* ``abs(o)`` - is the Euclidean norm (square root of the sum of component squares) if ``o`` is a :ref:`Point` or a :ref:`Matrix`. For rectangles, the area is returned (result of ``getArea()``).
* ``+o`` - is a copy of ``o``.
* ``-o`` - is an object copy with negated components.
* ``~m`` - is the inverse of :ref:`Matrix` ``m``. The other geometry objects are not invertible w/r to multiplication.

Binary Operations
------------------
* ``a + b``, ``a - b`` - are the component-wise counterparts of the resp. numerical operations. In all cases, ``b`` may be a number (which is added to or subtracted from each component) or an object with the same length as ``a``, meaning point-like if ``a`` is a :ref:`Point`, etc.
* ``a * b``, ``a / b`` - ``b`` must be either matrix-like or numeric.
    - A number ``b`` is always valid and will be applied to all components of ``a``.
    - If ``a`` is a point or a rectangle, then ``a.transform(b)`` (resp. ``a.transform(~b)``) is executed if ``b`` is matrix-like.
    - If ``a`` is a matrix, then ``a * b``, resp. ``a * ~b`` is executed, if ``b`` is matrix-like.
* ``a & b`` - **intersection rectangle:** ``a`` must be a rectangle and ``b`` rect-like.
* ``a | b`` - **union rectangle:** ``a`` must be a rectangle, and ``b`` can be point-like or rect-like.
* ``b in a`` - if ``b`` is a number, then ``b in tuple(a)`` is returned. If ``b`` is point-like or rect-like, then ``a`` must be a rectangle, and the result of ``a.contains(b)`` is returned.
* ``a == b`` - is true if all components and the object types are equal (but maybe ``id(a) != id(b)``).