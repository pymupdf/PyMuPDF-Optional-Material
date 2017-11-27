
.. _cooperation:

===============================================================
Working together: DisplayList, TextPage and TextSheet
===============================================================
Here are some instructions on how to use these classes together.

In some situations, performance improvements may be achievable when you fall back to the detail level explained here.

This may be possible when several different things need to be done with the same page.

Create a DisplayList
---------------------
A :ref:`DisplayList` represents an interpreted page. Methods for pixmap creation, text extraction and text search are  - behind the curtain - all using the page's display list to perform their tasks. Therefore, some overhead can be saved, if a display list is only created once per page.

An example may be, that a page image must re-displayed multiple times in a GUI because the user is zooming (i.e. change of image resolution and clip area).

>>> dl = page.getDisplayList()              # create the display list

You can also create display lists for many pages "on stack" (in a list), may be during document open, or you store it when a page is visited for the first time.

Note, that for everything what follows, only the display list is needed - the corresponding :ref:`Page` object could have been deleted.

Generate Pixmap
------------------
The following creates a Pixmap from a :ref:`DisplayList`. Parameters are the same as for :meth:`Page.getPixMap`.

>>> pix = dl.getPixmap()                    # create the page's pixmap

The execution time of this statement may be up to 50% smaller than that of :meth:`Page.getPixMap`.

Perform Text Search
---------------------
With the display list from above, we can also search for text.

For this we need to create :ref:`TextSheet` and :ref:`TextPage` objects.

>>> ts = fitz.TextSheet()                    # see remark (*)
>>> tp = dl.getTextPage(ts)                  # display list from above
>>> rlist = tp.search("needle")              # look up "needle" locations
>>> for r in rlist:                          # work with found locations:
        pix.invertIRect(r.irect)             # e.g. invert colors in rectangle

(*) The text sheet could actually have been re-used, it does not need to be new as indicated here. You may create one when you open the document and use it for all text operations.

Extract Text
----------------
With the :ref:`TextPage` object from above, we can immediately use one or all of the 4 text extraction methods:

>>> txt  = tp.extractText()                  # plain text format
>>> json = tp.extractJSON()                  # json format
>>> html = tp.extractHTML()                  # HTML format
>>> xml  = tp.extractXML()                   # XML format
