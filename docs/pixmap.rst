.. _Pixmap:

================
Pixmap
================

Pixmaps ("pixel maps") are objects at the heart of MuPDF's rendering capabilities. They represent plane rectangular sets of pixels. Each pixel is described by a number of bytes ("components") plus an (optional since v1.10.0) alpha byte.

In PyMuPDF, there exist several ways to create a pixmap. Except one, all of them are available as overloaded constructors. A pixmap can be created ...

1. from a document page (via methods :meth:`Page.getPixmap` or :meth:`Document.getPagePixmap`)
2. empty based on :ref:`Colorspace` and :ref:`IRect` information
3. from an image file
4. from an in-memory image (bytearray)
5. from a memory area of plain pixels
6. from an image inside a PDF document
7. as a copy of another pixmap

.. NOTE:: A number of image formats is supported as input for points 3. and 4. above. See section :ref:`ImageFiles`.

Have a look at the **example** section to see some pixmap usage "at work".

============================= ===================================================
**Method / Attribute**        **Short Description**
============================= ===================================================
:meth:`Pixmap.clearWith`      clears (parts of) a pixmap
:meth:`Pixmap.copyPixmap`     copy parts of another pixmap
:meth:`Pixmap.gammaWith`      applies a gamma factor to the pixmap
:meth:`Pixmap.getPNGData`     returns a PNG as a memory area
:meth:`Pixmap.invertIRect`    invert the pixels of a given area
:meth:`Pixmap.setAlpha`       sets alpha values
:meth:`Pixmap.tintWith`       tints a pixmap with a color
:meth:`Pixmap.writeImage`     saves a pixmap in a variety of image formats
:meth:`Pixmap.writePNG`       saves a pixmap as a PNG file
:attr:`Pixmap.alpha`          indicates whether transparency is included
:attr:`Pixmap.colorspace`     contains the :ref:`Colorspace`
:attr:`Pixmap.height`         height of the region in pixels
:attr:`Pixmap.interpolate`    interpolation method indicator
:attr:`Pixmap.irect`          is the :ref:`IRect` of the pixmap
:attr:`Pixmap.n`              number of bytes per pixel including alpha byte
:attr:`Pixmap.samples`        the components data for all pixels
:attr:`Pixmap.size`           contains the pixmap's total length
:attr:`Pixmap.stride`         number of bytes of one image row
:attr:`Pixmap.width`          width of the region in pixels
:attr:`Pixmap.x`              X-coordinate of top-left corner of pixmap
:attr:`Pixmap.xres`           resolution in X-direction
:attr:`Pixmap.y`              Y-coordinate of top-left corner of pixmap
:attr:`Pixmap.yres`           resolution in Y-direction
============================= ===================================================

**Class API**

.. class:: Pixmap

   .. method:: __init__(self, colorspace, irect, alpha)

      This constructor creates an empty pixmap of a size and an origin specified by the irect object. So, for a ``fitz.IRect(x0, y0, x1, y1)``, ``fitz.Point(x0, y0)`` designates the top left corner of the pixmap. Note that the image area is **not initialized** and will contain crap data.

      :arg colorspace: The colorspace of the pixmap.
      :type colorspace: :ref:`Colorspace`

      :arg irect: Specifies the pixmap's area and its location.
      :type irect: :ref:`IRect`

      :arg bool alpha: Specifies whether transparency bytes should be included. Default is ``False``.

   .. method:: __init__(self, doc, xref)

      This constructor creates a pixmap with origin ``(0, 0)`` from an image contained in PDF document ``doc`` identified by its XREF number. The result will automatically be given the characteristics of the stored image (dimension, colorspace, alpha).

      :arg doc: an opened **PDF** document.
      :type doc: :ref:`Document`

      :arg int xref: the XREF number of the image.

   .. method:: __init__(self, colorspace, source, [alpha])

      This constructor creates a new pixmap as a copy of another one. If the two colorspaces differ, a conversion will take place. Any combination of supported colorspaces is possible.

      :arg colorspace: The desired colorspace of the pixmap. Must be one of PyMuPDF's supported colorspaces.
      :type colorspace: :ref:`Colorspace`

      :arg source: the source pixmap.
      :type source: ``Pixmap``

      :arg bool alpha: whether to also copy the source's alpha channel. If the source has no alpha, this parameter has no effect. If ``False`` the result will have no alpha.

   .. method:: __init__(self, filename)

      This constructor creates a pixmap from the image contained in file ``filename``. The image type and all other properties are determined automatically.

      :arg str filename: Path / name of the file. The origin of the resulting pixmap is ``(0, 0)``.

   .. method:: __init__(self, source)

      This constructor creates an identical pixmap copy with an alpha channel added. The alpha values are set to 255.

      :arg source: the source pixmap. It must have ``alpha == 0``.
      :type source: ``Pixmap``

   .. method:: __init__(self, img)

      This constructor creates a non-empty pixmap from ``img``, which is assumed to contain a supported image as a bytearray. The image type and all other properties are determined automatically.

      :arg bytearray img: Data containing a complete, valid image in one of the supported formats. E.g. this may have been obtained from a statement like ``img = bytearray(open('somepic.png', 'rb').read())``. The origin of the resulting pixmap is (0,0). Objects of type ``bytes`` are not supported in this case, because this is the same as ``string`` in Python 2 and thus cannot safely be distinguished from other constructors.

   .. method:: __init__(self, colorspace, width, height, samples, alpha)

      This constructor creates a non-empty pixmap from ``samples``, which is assumed to contain an image in "plain pixel" format. This means that each pixel is represented by ``n`` bytes (as controlled by the ``colorspace`` and ``alpha`` parameters). The origin of the resulting pixmap is (0,0). This method is useful when raw image data are provided by some other program - see examples below.

      :arg colorspace: Colorspace of the image. Together with ``alpha`` this parameter controls the interpretation of the ``samples`` area. The following must be true: ``(colorspace.n + alpha) * width * height == len(samples)``.
      :type colorspace: :ref:`Colorspace`

      :arg int width: Width of the image in pixels

      :arg int height: Height of the image in pixels

      :arg bytes samples:  an area containing all pixels of the image. Must include alpha values if specified. Type ``bytearray`` is also supported.

      :arg bool alpha: whether a transparency channel is included in samples.

      .. caution:: Make sure that ``samples`` remains available throughout the lifetime of the pixmap. MuPDF will not make a copy of it, but rather record a pointer to this area in the created pixmap. Failure to do so will likely destroy the pixmap's image or even crash the interpreter.

   .. method:: clearWith(value [, irect])

      Clears an area specified by the :ref:`IRect` ``irect`` within a pixmap. To clear the whole pixmap omit ``irect``.

      :arg int value: Values from 0 to 255 are valid. Each color byte of each pixel will be set to this value, while alpha will always be set to 255 (non-transparent) if present. Default is 0 (black).

      :arg irect: An ``IRect`` object specifying the area to be cleared.
      :type irect: :ref:`IRect`

   .. method:: tintWith(red, green, blue)

      Colorizes (tints) a pixmap with a color provided as a value triple (red, green, blue). Only colorspaces :data:`CS_GRAY` and :data:`CS_RGB` are supported.

      If the colorspace is :data:`CS_GRAY`, ``(red + green + blue)/3`` will be taken as the tinting value.

      :arg int red: The ``red`` component. Values from 0 to 255 are valid.

      :arg int green: The ``green`` component. Values from 0 to 255 are valid.

      :arg int blue: The ``blue`` component. Values from 0 to 255 are valid.

   .. method:: gammaWith(gamma)

      Applies a gamma factor to a pixmap, i.e. lightens or darkens it.

      :arg float gamma: ``gamma = 1.0`` does nothing, ``gamma < 1.0`` lightens, ``gamma > 1.0`` darkens the image.

   .. method:: setAlpha([alphavalues])

      Changes the alpha channel to values provided. The pixmap must have an alpha channel.

      :arg bytes alphavalues: the new alpha values. Type ``bytearray`` is also permitted. If provided, its length must be at least ``width * height``. If omitted, all alpha values are set to 255 (no transparency).

   .. method:: invertIRect(irect)

      Invert the color of all pixels in an area specified by :ref:`IRect` ``irect``. To invert everything, or omit this parameter.

      :arg irect: The area to be inverted.
      :type irect: :ref:`IRect`

   .. method:: copyPixmap(source, irect)

      Copies the :ref:`IRect` part of the ``source`` pixmap into the corresponding area of this one. The two pixmaps may have different dimensions and different colorspaces (provided each is either :data:`CS_GRAY` or :data:`CS_RGB`), but currently **must** have the same alpha property. The copy mechanism automatically adjusts discrepancies between source and target pixmap like so:

      If copying from :data:`CS_GRAY` to :data:`CS_RGB`, the source gray-shade value will be put into each of the three rgb component bytes. If the other way round, (r + g + b) / 3 will be taken as the gray-shade value of the target.

      Between the specified ``irect`` and the target pixmap's :ref:`Irect`, an "intersection" rectangle is calculated at first. Then the corresponding data of this intersection are being copied. If the intersection is empty, nothing will happen.

      If you want your ``source`` pixmap image to land at a specific position of the target, set its ``x`` and ``y`` attributes to the top left point of the desired rectangle before copying. See the example below for how this works.

      :arg source: The pixmap from where to copy.
      :type source: :ref:`Pixmap`

      :arg irect: The area to be copied.
      :type irect: :ref:`IRect`

   .. method:: writeImage(filename, output="png")

      Saves a pixmap as an image file. Depending on the output chosen, some or all colorspaces are supported and different file extensions can be chosen. Please see the table below. Since MuPDF v1.10a the ``savealpha`` option is no longer supported and will be ignored with a warning.

      :arg str filename: The filename to save to. Depending on the chosen output format, possible file extensions are ``.pam``, ``.pbm``, ``.pgm``, ``ppm``, ``.pnm``, ``.png`` and ``.tga``.

      :arg str output: The requested image format. The default is ``png`` for which this function is equal to ``writePNG()``, see below. Other possible values are ``pam``, ``pnm`` and ``tga``.

   .. method:: writePNG(filename)

      Saves the pixmap as a PNG file. Please note that only grayscale and RGB colorspaces are supported (this is **not** a MuPDF restriction). CMYK colorspaces must either be saved as ``*.pam`` files or be converted first.

      :arg str filename: The filename to save to (the extension ``png`` must be specified). Existing files will be overwritten without warning.

   .. method:: getPNGData()

      Returns an image area (bytearray) of the pixmap in PNG format. Please note that only grayscale and RGB colorspaces are supported (this is **not** a MuPDF restriction). CMYK colorspaces must be converted first.

      :rtype: bytearray

   .. attribute:: alpha

      Indicates whether the pixmap contains transparency information.

      :type: bool

   .. attribute:: colorspace

      The colorspace of the pixmap. This value may be ``None`` if the image is to be treated as a so-called *image mask* or *stencil mask* (currently happens for extracted PDF document images only).

      :type: :ref:`Colorspace`

   .. attribute:: stride

      Contains the length of one row of image data in ``samples``. This is primarily used for calculation purposes. The following expressions are true: ``len(samples) == height * stride``, ``width * n == stride``.

      :type: int

   .. attribute:: irect

      Contains the :ref:`IRect` of the pixmap.

      :type: :ref:`IRect`

   .. attribute:: samples

      The color and (if ``alpha == 1``) transparency values for all pixels. ``samples`` is a memory area of size ``width * height * n`` bytes. Each n bytes define one pixel. Each successive n bytes yield another pixel in scanline order. Subsequent scanlines follow each other with no padding. E.g. for an RGBA colorspace this means, ``samples`` is a sequence of bytes like ``..., R, G, B, A, ...``, and the four byte values R, G, B, A define one pixel.

      This area can also be used by other graphics libraries like PIL (Python Imaging Library) to do additional processing like saving the pixmap in other image formats. See example 3.

      :type: bytes

      .. note:: We have changed the type of ``samples`` from ``bytearray`` to ``bytes``. Some GUIs (Tk) require a read-only type here. We hope this does not break existing code!

   .. attribute:: size

      Contains ``len(pixmap)``. This will generally equal ``len(pix.samples) + 60`` (32bit systems, the delta is 88 on 64bit machines).

      :type: int

   .. attribute:: width

      The width of the region in pixels. For compatibility reasons, ``w`` is also supported.

      :type: int

   .. attribute:: height

      The height of the region in pixels. For compatibility reasons, ``h`` is also supported.

      :type: int

   .. attribute:: x

      X-coordinate of top-left corner

      :type: int

   .. attribute:: y

      Y-coordinate of top-left corner

      :type: int

   .. attribute:: n

      Number of components per pixel. This number depends on colorspace and alpha. In most cases, ``Pixmap.n - Pixmap.aslpha == pixmap.colorspace.n`` is true, except for pixmaps without a colorspace (stencil masks).

      :type: int

   .. attribute:: xres

      Horizontal resolution in dpi (dots per inch).

      :type: int

   .. attribute:: yres

      Vertical resolution in dpi.

      :type: int

   .. attribute:: interpolate

      An information-only boolean flag set to ``True`` if the image will be drawn using "linear interpolation". If ``False`` "nearest neighbour sampling" will be used.

      :type: bool

.. _ImageFiles:

Supported Image Types for Pixmap Construction
-----------------------------------------------
The following file types are supported as input to construct pixmaps: **BMP, JPEG, GIF, SVG, TIFF, JXR,** and **PNG**. This support is two-fold:

1. Directly create a pixmap with ``Pixmap(filename)`` or ``Pixmap(byterray)``. The pixmap will then have properties as determined by the image.

2. Open such files with ``fitz.open(...)``. The result will then appear as a document containing one single page. Creating a pixmap of this page offers all options available in this context: apply a matrix, choose colorspace and alpha, confine the pixmap to a clip area, etc.

Details on Saving Images with ``writeImage()``
-----------------------------------------------

.. |wimgopt| image:: writeimage.png

The following table shows possible combinations of file extensions, output formats and colorspaces of method ``writeImage()``:

|wimgopt|

.. note:: Not all image file types are available, or at least common on all platforms, e.g. PAM is mostly unknown on Windows. Especially pertaining to CMYK colorspaces, you can always convert a CMYK pixmap to an RGB pixmap with ``rgb_pix = fitz.Pixmap(fitz.csRGB, cmyk_pix)`` and then save that as a PNG.

Pixmap Example Code Snippets
-----------------------------

**Example 1**

This shows how pixmaps can be used for purely graphical, non-PDF purposes. The script reads a PNG picture and creates a new PNG file which consist of 3 * 4 tiles of the original one:
::
 import fitz
 # create a pixmap of a picture
 pix0 = fitz.Pixmap("editra.png")

 # set target colorspace and pixmap dimensions and create it
 tar_width  = pix0.width * 3              # 3 tiles per row
 tar_height = pix0.height * 4             # 4 tiles per column
 tar_irect  = fitz.IRect(0, 0, tar_width, tar_height)
 # create empty target pixmap
 tar_pix    = fitz.Pixmap(fitz.csRGB, tar_irect, pix0.alpha)
 # clear target with a very lively stone-gray (thanks and R.I.P., Loriot)
 tar_pix.clearWith(90)

 # now fill target with 3 * 4 tiles of input picture
 for i in range(4):
     pix0.y = i * pix0.height                     # modify input's y coord
     for j in range(3):
         pix0.x = j * pix0.width                  # modify input's x coord
         tar_pix.copyPixmap(pix0, pix0.irect)     # copy input to new loc
         # save all intermediate images to show what is happening
         fn = "target-%i-%i.png" % (i, j)
         tar_pix.writePNG(fn) 


.. |editra| image:: editra.png

This is the input picture ``editra.png`` (taken from the wxPython directory ``/tools/Editra/pixmaps``):

|editra|

.. |target| image:: target.png

Here is the output, showing some intermediate picture and the final result:

|target|

**Example 2**

This shows how to create a PNG file from a numpy array (several times faster than most other methods):
::
 import numpy as np
 import fitz
 #==============================================================================
 # create a fun-colored width * height PNG with fitz and numpy
 #==============================================================================
 height = 150
 width  = 100
 bild = np.ndarray((height, width, 3), dtype=np.uint8)

 for i in range(height):
     for j in range(width):
         # one pixel (some fun coloring)
         bild[i, j] = [(i+j)%256, i%256, j%256]

 samples = bytearray(bild.tostring())    # get plain pixel data from numpy array
 pix = fitz.Pixmap(fitz.csRGB, width, height, samples, alpha=False)
 pix.writePNG("test.png")

**Example 3**

This shows how to interface with ``PIL / Pillow`` (the Python Imaging Library), thereby extending the reach of image files that can be processed:

>>> import fitz
>>> from PIL import Image
>>> pix = fitz.Pixmap(...)
>>> ...
>>> # create and save a PIL image
>>> img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
>>> img.save(filename, 'jpeg')
>>> ...
>>> # opposite direction:
>>> # create a pixmap from any PIL-supported image file "some_image.xxx"
>>> img = Image.open("some_image.xxx").convert("RGB")
>>> samples = img.tobytes()
>>> pix = fitz.Pixmap(fitz.csRGB, img.size[0], img.size[1], samples, alpha=False)
