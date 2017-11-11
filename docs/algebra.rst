.. _Algebra:

Operator Algebra for Geometry Objects
======================================
Instances of classes :ref:`Point`, :ref:`IRect`, :ref:`Rect` and :ref:`Matrix` are collectively also called "geometry" objects.

We have defined operators for these classes that allow dealing with them almost like ordinary numbers in terms of addition, subtraction, multiplication, division, and some others.

This chapter explains what is possible, instead of duplicating the same or similar text in each of the respective chapters.

General Remarks
-----------------
1. Operators can be either **binary** (i.e. involving two objects) or **unary**.

2. The result of binary operatorions **always** is a **new object** of the same type as the left operand.

3. The result of unary operations is either a bool, a float or the same object type.

4. All binary operators fully support in-place operations, i.e. something like ``a += b`` meaning ``a = a + b``.

5. The following binary operators are defined for all classes: ``+, -, *, /``. They have a similar meaning as the corresponding numerical ones.

6. Rectangles have additional binary operators ``&, |``, details below.

7. For binary operations, the **second** operand may have a different type as the left one. Often, Python sequences (lists, tuples) are allowed here, too, instead of one of the four classes. We allude to this fact by saying "point-like object" when we mean, that a :ref:`Point` is possible as well as a sequence of two numbers. Similar applies to "rect-like" (sequence length 4) or "matrix-like" (sequence length 6).

Unary Operations
------------------
* ``bool(o)`` - is false if and only if the object's components are all zero.
* ``abs(o)`` - is the object's Euclidean norm (square root of the sum of component squares) if ``o`` is a :ref:`Point` or a :ref:`Matrix`. For rectangles, the area is returned (result of ``getArea()``).
* ``-o`` - is an object copy with negated components.
* ``+o`` - is an object copy.
* ``~m`` - is the inverse of :ref:`Matrix` ``m``. Other objects have no inverse w/r to multiplication.

Binary Operations
------------------
* ``a + b``, ``a - b`` - are the component-wise counterparts of the resp. numerical operations. In all cases, ``b`` may be a number (added to or subtracted from each component). In all cases, ``b`` can be an object with the same length as ``a``, meaning point-like if ``a`` is a :ref:`Point`, etc.
* ``a * b``, ``a / b`` - second operand ``b`` must be either matrix-like or numeric. As usual, a number means applying it to all components of `a`. For a matrix-like ``b``, ``transform(b)`` (resp. ``transform(~b)``) is executed (for points and rectangles ``a``), or a matrix multiplication for matrices ``a`` takes place.
* ``a & b`` - only defined if ``a`` is a rectangle and rect-likes ``b``. The result is the intersection rectangle of the two.
* ``a | b`` - only defined if ``a`` is a rectangle. ``b`` can be point-like or rect-like. Result is the rectangle that contains both,``a`` and ``b``.
* ``b in a`` - if ``b`` is a number, ``b in tuple(a)`` is returned. If ``b`` is point-like or rect-like, then ``a`` must be a rectangle, and the result of ``a.contains(b)`` is returned.
* ``a == b`` - is true if all components and the object types are equal (the objects themselves may be unequal).