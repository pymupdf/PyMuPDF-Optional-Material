.. _Quad:

==========
Quad
==========

Represents a four-sided mathematical shape (quadrilateral or tetragon) in the plane, defined as a sequence of four :ref:`Point` objects ul, ur, ll, lr (conveniently called upper left, upper right, lower left, lower right). In (Py) MuPDF, only quads with four 90-degree angles and non-empty areas are of actual interest. Such "interesting" quads can be obtained as results of text search methods (:meth:`Page.searchFor`), and they are used to define text marker annotations (see e.g. :meth:`Page.addSquigglyAnnot` and friends).

.. note:: If ``m`` is a *rotation* or a *translation* :ref:`Matrix`, and ``rect`` a rectangle, then ``rect.tl * m``, ``rect.tr * m``, ``rect.bl * m``,  and ``rect.br * m`` are the corners of a **rectangular quad**. This is **not in general true** -- examples are shear matrices which produce parallelograms.

.. note:: This class provides an attribute to claculate the envelopping rectangle. Vice versa, rectangles now have the attribute :attr:`Rect.quad`, resp. :attr:`IRect.quad` to obtain their respective tetragon versions.

============================= =======================================================
**Methods / Attributes**      **Short Description**
============================= =======================================================
:meth:`Quad.transform`        transform with a matrix
:attr:`Quad.ul`               upper left point
:attr:`Quad.ur`               upper right point
:attr:`Quad.ll`               lower left point
:attr:`Quad.lr`               lower right point
:attr:`Quad.isEmpty`          true if corners define an empty area
:attr:`Quad.isRectangular`    true if all angles are 90 degrees
:attr:`Quad.rect`             smallest containing :ref:`Rect`
:attr:`Quad.width`            the longest width value
:attr:`Quad.height`           the longest height value
============================= =======================================================

**Class API**

.. class:: Quad

   .. method:: __init__(self)

   .. method:: __init__(self, ul, ur, ll, lr)

   .. method:: __init__(self, quad)

   .. method:: __init__(self, sequence)

      Overloaded constructors: ``ul``, ``ur``, ``ll``, ``lr`` stand for :ref:`Point` objects (the 4 corners), "sequence" is a Python sequence type with 4 :ref:`Point` objects.

      If "quad" is specified, the constructor creates a **new copy** of it.

      Without parameters, a quad consisting of 4 copies of ``Point(0, 0)`` is created.


   .. method:: transform(matrix)

      Modify the quadrilateral by transforming each of its corners with a matrix.

   .. attribute:: rect

      The smallest rectangle containing the quad, represented by the blue area in the following picture.

      .. image:: img-quads.jpg

      :type: :ref:`Rect`

   .. attribute:: ul

      Upper left point.

      :type: :ref:`Point`

   .. attribute:: ur

      Upper right point.

      :type: :ref:`Point`

   .. attribute:: ll

      Lower left point.

      :type: :ref:`Point`

   .. attribute:: lr

      Lower right point.

      :type: :ref:`Point`

   .. attribute:: isEmpty

      True if enclosed area is zero, i.e. all points are on the same line. If this is false, the quad may still not look like a rectangle (but more like a triangle, trapezoid, etc.).

      :type: bool

   .. attribute:: isRectangular

      True if all angles are 90 degrees. This also implies that the area is **not empty**.

      :type: bool

   .. attribute:: width

      The maximum length of the top and the bottom side.

      :type: float

   .. attribute:: height

      The maximum length of the left and the right side.

      :type: float

Remark
------
This class adheres to the sequence protocol, so components can be dealt with via their indices, too. Also refer to :ref:`SequenceTypes`.

We are still in process to extend algebraic operations to quads. Multiplication and division with / by numbers and matrices are already defined. Addition, subtraction and any unary operations may follow when we see an actual need.
