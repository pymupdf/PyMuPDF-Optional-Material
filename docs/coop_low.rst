
.. _cooperation:

===============================================================
Working together: DisplayList, TextPage and TextSheet
===============================================================
Here are some instructions on how to use these classes together.

In some situations, performance improvements may be achievable when you fall back to this detail. This is possible when several different things need to be done with the same page - as is demonstrated in the following overview.

Generate Pixmap
------------------
The following creates a Pixmap from a document's ``page`` (this happens behind the curtain when you use method ``page.getPixmap()``):
::
 dl = page.getDisplayList()                 # (1) create display list for the page
 pix = dl.getPixmap(matrix = fitz.Identity, # (2) create a pixmap showing defaults
                    colorspace = fitz.csRGB,
                    alpha = 0, clip = None)

To create another pixmap, just re-execute line (2). This may be desireable when you want to change resolution or colorspace, or restrict the pixmap to certain page areas, etc. Adjust the matrix, colorspace or clip parameters.

The execution times of statements (1) and (2) are of a similar order of magnitude. The proportion typically ranges from about 1:1 for text-oriented pages, to 1:5 or more for complex ones.

You can exploit this fact by e.g. creating display lists for pages "on stack" (perhaps during document open). When a page needs to be (re-) rendered, just create the pixmap of the corresponding display list.

Perform Text Search
---------------------
With the existing objects from above, create a new text page object to search for a text string on the page. The ``page`` object itself is no longer needed (it could have been set to ``None``).

For this we need to create TextPage and TextSheet objects:
::
 ts = fitz.TextSheet()                       # new or reuse from other pages
 tp = dl.getTextPage(ts)
 rlist = tp.search("needle")                 # look up "needle" locations
 for r in rlist:                             # work with found locations:
     pix.invertIRect(r.irect)                # e.g. invert colors in rectangles

Extract Text
----------------
Again with the existing objects, we can immediately use one or all of the 4 text extraction methods:
::
 txt  = tp.extractText()                     # plain text format
 json = tp.extractJSON()                     # json format
 html = tp.extractHTML()                     # HTML format
 xml  = tp.extractXML()                      # XML format
