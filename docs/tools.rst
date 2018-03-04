.. _Tools:

Tools
================

This class is a collection of low-level MuPDF utility methods and attributes, mainly around memory management.

================================ =================================================
**Method / Attribute**             **Description**
================================ =================================================
:meth:`Tools.gen_id`             generate a unique identifyer
:meth:`Tools.store_shrink`       shrink the storables cache [#f1]_
:attr:`Tools.store_maxsize`      maximum storables cache size
:attr:`Tools.store_size`         current storables cache size
================================ =================================================

**Class API**

.. class:: Tools

   .. method:: gen_id()

      A convenience method returning a unique positive integer which will increase by 1 with every invocation. The numbers generated are guarantied to be unique within this execution of PyMuPDF (its implementation is also threadsafe should this ever be become relevant for PyMuPDF). Example usages include using it as a unique key in a database - its creation should be faster than using timestamps by an order of magnitude.

      .. note:: Because it is implemented as an ordinary 4-bytes signed integer, wraparounds may theoretically indeed occur though after over 2.147e+9 executions.

      :rtype: int
      :returns: a unique positive integer.

   .. method:: store_shrink(percent)

      Reduce the storables cache by a percentage of its current size.

      :arg int percent: the percentage of current size to free. If 100+ the store will be emptied, if zero, nothing will happen. MuPDF's caching strategy is "least recently used", so low-usage elements get deleted first.

      :rtype: int
      :returns: the new current store size. Depending on the situation, the size reduction may be larger than the requested percentage.

   .. attribute:: store_maxsize

      Maximum storables cache size in bytes. PyMuPDF is generated with a value of 268'435'456 (256 MB, the default value), which you should therefore always see here. If this value is zero, then an "unlimited" growth is permitted.

   .. attribute:: store_size

      Current storables cache size in bytes. This value may change (and will usually increase) with every use of a PyMuPDF function. It will (automatically) decrease only when :attr:`Tools.store_maxize` is going to be exceeded: in this case, MuPDF will evict low-usage objects until the value is again in range.

Example Session
----------------

>>> import fitz
>>> tools = fitz.Tools()
# print the maximum and current cache sizes
>>> tools.store_maxsize
268435456
>>> tools.store_size
0
>>> doc = fitz.open("demo1.pdf")
# pixmap creation puts lots of object in cache (text, images, fonts),
# apart from the pixmap itself
>>> pix = doc[0].getPixmap(alpha=False)
>>> tools.store_size
454519
# release (at least) 50% of the storage
>>> tools.store_shrink(50)
13471
>>> tools.store_size
13471
# get a few unique numbers
>>> tools.gen_id()
1
>>> tools.gen_id()
2
>>> tools.gen_id()
3
# close document and see how much cache is still in use
>>> doc.close()
>>> tools.store_size
0
>>> 


.. rubric:: Footnotes

.. [#f1] This memory area is internally used by MuPDF, and it serves as a cache for objects that have already been read and interpreted, thus improving performance. The most bulky object types are images and also fonts. When an application starts up the MuPDF library (in our case this happens as part of ``import fitz``), it must specify a maximum size for this area. PyMuPDF's uses the default value (256 MB) to limit memory consumption. Use the methods here to control or investigate store usage. For example: even after a document has been closed and all related objects have been deleted, the store usage may still not drop down to zero. So you might want to enforce that before opening another document.
