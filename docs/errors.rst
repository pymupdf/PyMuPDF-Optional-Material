Error Messages
====================

This a list of exception messages raised by PyMuPDF together with an explanation and possible solution.

In addition, the underlying C library MuPDF also raises exceptions on the Python level. We have included a few of those as well and may extend this in future.


**annot has no /AP**
    * Bad specification - no changes possible for this annotation.

**arg 1 not bytes or bytearray**
    * Specify parameter as type ``bytes`` or ``bytearray``.

**bad PDF: Contents is no stream object**
    * The ``/Contents`` object(s) of a page must be streams. Repair PDF.

**bad PDF: file has no stream**
    * An embedded / attached file is not a stream. Repair PDF.

**buffer too large to deflate**
    * Internal error - report an issue.

**cannot deflate buffer**
    * Internal error - report an issue.

**cannot open <path>: No such file or directory**
    * Specify a valid file name / path.

**cannot recognize archive**
    * Trying to open an invalid CBZ document.

**cannot recognize zip archive**
    * Trying to open an invalid XPS document.

**color components must be in range 0 to 1**
    * Color components must be floats in interval [0, 1].

**could not create UTF16 for '<name>'**
    * Internal error - report an issue.

**could not get string of '<name>'**
    * Internal error - report an issue.

**could not get UTF16 string of '<name>'**
    * Internal error - report an issue.

**could not load root object**
    * Root object of PDF not found. Repair PDF.

**encrypted file - save to new**
    * Trying incremental save for a decrypted file. Use ``doc.save()`` to a new file.

**exactly one of filename, pixmap must be given**
    * You either specified both parameters or none.

**expected a sequence**
    * Parameter type must be ``list``, ``tuple``, etc.

**filename must be a string**
    * Specify a valid file path / name.

**filename must be string or None**
    * Specify a valid file path / name or omit parameter.

**filename must end with '.png'**
    * ``writePNG()`` requires file extension ``.png``.

**filetype missing with stream specified**
    * Document open from memory needs its type as a string.

**fontname must be supplied**
    * A new font file requires some (arbitrary) **new** reference name.

**found code point nnn: increase charlimit**
    * Trying to get a glyph width beyond the current table size limit.

**incremental excludes garbage**
    * Garbage collection cannot occur during incremental saves.

**incremental excludes linear**
    * Linearization cannot occur during incremental saves.

**incremental save needs original file**
    * Incremental save is only possible to the original file.

**info not a dict**
    * Specify correct Python parameter type.

**invalid font - FontDescriptor missing**
    * Specify correct XREF to read font.

**invalid font descriptor subtype**
    * Bad font description in PDF. Repair file.

**unhandled font type** / **unhandled font type '<type>'**
    * MuPDF does not yet handle this font type. Requesting method cannot be used, unfortunately. Report an issue.

**invalid key in info dict**
    * Dictionary key misspelled.

**invalid page range**
    * Page numbers must be in range ``[0, pageCount - 1]``.

**invalid stream**
    * Stream object updates need type ``bytes`` or ``bytearray``.

**len(samples) invalid**
    * Length of samples must equal ``width * height * n`` (where ``n`` is the number of components per pixel).

**line endpoints must be within page rect**
    * The ``Page.rect`` must contain the points.

**name already exists**
    * The name is in use by some other embedded file.

**name not valid**
    * Specify a name of non-zero length.

**need 3 color components**
    * Only RGB colors are supported, which need three components.

**no embedded files**
    * PDF has no embedded files.

**no objects found**
    * Trying to open an invalid PDF, FB2, or EPUB document.

**not a file attachment annot**
    * Accessed an annotation with the wrong type.

**not a PDF**
    * Using some method or attribute only valid for PDF document type.

**nothing to change**
    * No data supplied for embedded file metadata change.

**operation illegal for closed doc**
    * Trying to use methods / properties after close of document.

**orphaned object: parent is None**
    * Accessing an object whose parent no longer exists (e.g. an annotation of an unavailable page).

**page number out of range**
    * Page numbers must always be ``< pageCount``, but also non-negative for some methods.

**page numbers must be integers**
    * Specify valid page numbers (``select()`` method).

**rect must be contained in page rect**
    * Image insertion requires a target rectangle contained in ``page.rect``.

**rect must be finite and not empty**
    * Top-left corner must be "northeast" of bottom-right one, and rectangle area must be positive.

**repaired file - save to new**
    * Trying incremental save for file repaired during open. Use ``doc.save()`` to a new file.

**save to original requires incremental**
    * Using original filename in ``doc.save()`` without also specifying option ``incremental``. Consider using ``doc.saveIncr()``.

**sequence length must be <n>**
    * Creating Point, Rect, Irect, Matrix with wrong length sequences.

**some text is needed**
    * Specify text with a positive length.

**source and target too close**
    * Target number of moved page ``pno`` must be ``> pno`` or ``< pno - 1``.

**source must not equal target PDF**
    * Method ``doc.insertPDF()`` requires two distinct document objects (which may point to the same file, however).

**source not a PDF**
    * Method ``doc.insertPDF()`` only works with PDF documents.

**source page out of range**
    * Specify a valid page number.

**target not a PDF**
    * Method ``doc.insertPDF()`` only works with PDF documents.

**text position outside page height range**
    * If text starts at :ref:`Point` ``point``, ``fontsize <= point.y <= (page height - fontsize * 1.2)`` must be true.

**type(ap) invalid**
    * Internal error - report an issue.

**type(imagedata) invalid**
    * Use type ``bytearray``.

**type(samples) invalid**
    * Use type ``bytes`` or ``bytearray``.

**unknown PDF Base 14 font**
    * Use a valid PDF standard font name.

**xref entry is not an image**
    * Trying to create a pixmap from a non-image PDF object.

**xref invalid**
    * Internal error - report an issue.

**xref is not a stream**
    * Trying to access the stream part of a non-stream object.

**xref out of range**
    * PDF xref numbers must be ``1 <= xref <= doc._getXrefLength()``.

