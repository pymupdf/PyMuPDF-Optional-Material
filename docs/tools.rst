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

      A convenience method returning a unique positive integer which will increase by 1 with every invocation. The numbers generated are guarantied to be unique within this execution of PyMuPDF. Its implementation is also threadsafe (should this ever be become relevant for PyMuPDF).

      Because it is implemented as an ordinary 4-bytes signed integer, wraparounds may theoretically indeed occur after over 2.147 billion executions, but the smallest number ever returned will be 1.

      :rtype: int
      :returns: a unique positive integer.

   .. method:: store_shrink(percent)

      Reduce the storables cache by a percentage of its current size.

      :arg int percent: the percentage of current size to free. If 100+ the store will be emptied, if zero, nothing will happen. MuPDF's caching strategy is "least recently used", so low-usage elements get deleted first.

      :rtype: int
      :returns: the new current store size.

   .. attribute:: store_maxsize

      Maximum storables cache size in bytes. PyMuPDF is generated with a value of 268'435'456 (256 MB). If this value is zero, then an "unlimited" growth is permitted.

   .. attribute:: store_size

      Current storables cache size in bytes. This value may change (i.e. will usually increase) with every use of a PyMuPDF function. It will (automatically) decrease only when :attr:`Tools.store_maxize` would be exceeded: in this case, MuPDF will evict low-usage objects until the value is again below.

.. rubric:: Footnotes

.. [#f1] This memory area serves as a cache for objects that have already been read and interpreted, thus improving performance. The most bulky object types are images and also fonts. When an application starts up the MuPDF library (in our case this happens as part of ``import fitz``), it must specify a maximum size for this area. PyMuPDF's uses the default value (256 MB) to limit memory consumption. Use the methods here to control or investigate store usage. For example: even after a document has been closed and all related objects have been deleted, the store usage may still not drop down to zero. So you might want to enforce that before opening another document.
