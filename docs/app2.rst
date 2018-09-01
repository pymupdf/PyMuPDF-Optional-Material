.. _Appendix2:

======================================
Appendix 2: Details on Text Extraction
======================================
This chapter provides background on the text extraction methods of PyMuPDF.

Information of interest are

* what do they provide?
* what do they imply (processing time / data sizes)?

General structure of a TextPage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`TextPage` is one of PyMuPDF's classes. It is normally created behind the curtain, when :ref:`Page` text extraction methods are used, but it is also available directly. In any case, an intermediate class, :ref:`DisplayList` must be created first (display lists contain interpreted pages, they also provide the input for :ref:`Pixmap` creation). Information contained in a :ref:`TextPage` has the following hierarchy. Other than its name suggests, images may optionally also be part of a text page::

 <page>
     <text block>
         <line>
             <span>
                 <char>
     <image block>
         <img>

A **text page** consists of blocks (= roughly paragraphs).

A **block** consists of either lines and their characters, or an image.

A **line** consists of spans.

A **span** consists of font information and characters that share a common baseline.

Plain Text
~~~~~~~~~~

This function extracts a page's plain **text in original order** as specified by the creator of the document (which may not equal a natural reading order).

An example output::

 PyMuPDF Documentation
 Release 1.12.0
 Jorj X. McKie
 Dec 04, 2017

HTML
~~~~

HTML output fully reflects the structure of the page's ``TextPage`` -- much like DICT or JSON below. This includes images, font information and text positions. If wrapped in HTML header and trailer code, it can readily be displayed be an internate browser. Our above example::

 <div style="width:595pt;height:841pt">
 <img style="top:88pt;left:327pt;width:195pt;height:86pt" src="data:image/jpeg;base64,
 /9j/4AAQSkZJRgABAQEAYABgAAD/4Q (... omitted image data ...) ">
 <p style="top:189pt;left:195pt;"><b><span style="font-family:SFSX2488,serif;font-size:24.7871pt;">PyMuPDF Documentation</span></b></p>
 <p style="top:223pt;left:404pt;"><b><i><span style="font-family:SFSO1728,serif;font-size:17.2154pt;">Release 1.12.0</span></i></b></p>
 <p style="top:371pt;left:400pt;"><b><span style="font-family:SFSX1728,serif;font-size:17.2154pt;">Jorj X. McKie</span></b></p>
 <p style="top:637pt;left:448pt;"><b><span style="font-family:SFSX1200,serif;font-size:11.9552pt;">Dec 04, 2017</span></b></p>
 </div>

.. _HTMLQuality:

Controlling Quality of HTML Output
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Though HTML output has improved a lot in MuPDF v1.12.0, it currently is not yet bug-free: we have found problems in the areas **font support** and **image positioning**.

* HTML text contains references to the fonts used of the original document. If these are not known to the browser (a fat chance!), it will replace them with his assumptions, which probably will let the result look awkward. This issue varies greatly by browser -- on my Windows machine, MS Edge worked just fine, whereas Firefox looked horrible.

* For PDFs with a complex structure, images may not be positioned and / or sized correctly. This seems to be the case for rotated pages and pages, where the various possible page bbox variants do not coincide (e.g. ``MediaBox != CropBox``). We do not know yet, how to address this -- we filed a bug at MuPDF's site.

To address the font issue, you can use a simple utility script to scan through the HTML file and replace font references. Here is a little example that replaces all fonts with one of the :ref:`Base-14-Fonts`: serifed fonts will become "Times", non-serifed "Helvetica" and monospaced will become "Courier". Their respective variations for "bold", "italic", etc. are hopefully done correctly by your browser::

 import sys
 filename = sys.argv[1]
 otext = open(filename).read()                 # original html text string
 pos1 = 0                                      # search start poition
 font_serif = "font-family:Times"              # enter ...
 font_sans  = "font-family:Helvetica"          # ... your choices ...
 font_mono  = "font-family:Courier"            # ... here
 found_one  = False                            # true if search successfull

 while True:
     pos0 = otext.find("font-family:", pos1)   # start of a font spec
     if pos0 < 0:                              # none found - we are done
         break
     pos1 = otext.find(";", pos0)              # end of font spec
     test = otext[pos0 : pos1]                 # complete font spec string
     testn = ""                                # the new font spec string
     if test.endswith(",serif"):               # font with serifs?
         testn = font_serif                    # use Times instead
     elif test.endswith(",sans-serif"):        # sans serifs font?
         testn = font_sans                     # use Helvetica
     elif test.endswith(",monospace"):         # monospaced font?
         testn = font_mono                     # becomes Courier
 
     if testn != "":                           # any of the above found?
         otext = otext.replace(test, testn)    # change the source
         found_one = True
         pos1 = 0                              # start over
 
 if found_one:
     ofile = open(filename + ".html", "w")
     ofile.write(otext)
     ofile.close()
 else:
     print("Warning: could not find any font specs!")



DICT (or JSON)
~~~~~~~~~~~~~~~~

DICT (JSON) output fully reflects the structure of a ``TextPage`` and provides image content and position details (``bbox`` -- boundary boxes in pixel units) for every block and line. This information can be used to present text in another reading order if required (e.g. from top-left to bottom-right). Have a look at `PDF2textJS.py <https://github.com/rk700/PyMuPDF/blob/master/examples/PDF2textJS.py>`_. Images are stored as ``bytes`` (``bytearray`` in Python 2) for DICT output and base64 encoded strings for JSON output. Here is how this looks like::

 In [2]: doc = fitz.open("pymupdf.pdf")
 In [3]: page = doc[0]
 In [4]: d = page.getText("dict")
 In [5]: d
 Out[5]: 
 {'width': 612.0,
 'height': 792.0,
 'blocks': [{'type': 1,
   'bbox': [344.25, 88.93597412109375, 540.0, 175.18597412109375],
   'width': 261,
   'height': 115,
   'ext': 'jpeg',
   'image': b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01 ... <more data> ...'},
  {'type': 0,
   'lines': [{'wmode': 0,
     'dir': (1.0, 0.0),
     'spans': [{'font': 'ClearSans-Bold',
       'size': 24.787099838256836,
       'flags': 20,
       'text': 'PyMuPDF Documentation'}],
     'bbox': (251.24600219726562,
      184.3526153564453,
      539.9661254882812,
      218.6648406982422)}],
   'bbox': (251.24600219726562,
    184.3526153564453,
    539.9661254882812,
    218.6648406982422)},
  {'type': 0,
   'lines': [{'wmode': 0,
     'dir': (1.0, 0.0),
     'spans': [{'font': 'ClearSans-BoldItalic',
       'size': 17.21540069580078,
       'flags': 22,
       'text': 'Release 1.13.18'}],
     'bbox': (412.5299987792969,
      220.4202880859375,
      540.0100708007812,
      244.234375)}],
   'bbox': (412.5299987792969,
    220.4202880859375,
    540.0100708007812,
    244.234375)},
  {'type': 0,
   'lines': [{'wmode': 0,
     'dir': (1.0, 0.0),
     'spans': [{'font': 'ClearSans-Bold',
       'size': 17.21540069580078,
       'flags': 20,
       'text': 'Jorj X. McKie'}],
     'bbox': (432.9129943847656,
      355.5234680175781,
      534.0018310546875,
      379.3543701171875)}],
   'bbox': (432.9129943847656,
    355.5234680175781,
    534.0018310546875,
    379.3543701171875)},
  {'type': 0,
   'lines': [{'wmode': 0,
     'dir': (1.0, 0.0),
     'spans': [{'font': 'ClearSans-Bold',
       'size': 11.9552001953125,
       'flags': 20,
       'text': 'Aug 23, 2018'}],
     'bbox': (465.7779846191406,
      597.5914916992188,
      539.995849609375,
      614.1408081054688)}],
   'bbox': (465.7779846191406,
    597.5914916992188,
    539.995849609375,
    614.1408081054688)}]}
 In [6]: 

RAWDICT
~~~~~~~~~~~~~~~~
This dictionary is an **information superset of DICT** and takes the detail level one step deeper. It looks exactly like the above, except that the ``"text"`` items (*string*) are replaced by ``"chars"`` items (*list*). Each ``"chars"`` entry is a character *dict*. For example, here is what you would see in place of item ``'text': 'PyMuPDF Documentation'`` above::

       'chars': [{'c': 'P',
         'origin': (251.24600219726562, 211.052001953125),
         'bbox': (251.24600219726562,
          184.3526153564453,
          266.2421875,
          218.6648406982422)},
        {'c': 'y',
         'origin': (266.2421875, 211.052001953125),
         'bbox': (266.2421875,
          184.3526153564453,
          279.3793640136719,
          218.6648406982422)},
        {'c': 'M',
         'origin': (279.3793640136719, 211.052001953125),
         'bbox': (279.3793640136719,
          184.3526153564453,
          299.5560607910156,
          218.6648406982422)},
        ... <more character dicts> ...  
        {'c': 'o',
         'origin': (510.84130859375, 211.052001953125),
         'bbox': (510.84130859375,
          184.3526153564453,
          525.2426147460938,
          218.6648406982422)},
        {'c': 'n',
         'origin': (525.2426147460938, 211.052001953125),
         'bbox': (525.2426147460938,
          184.3526153564453,
          539.9661254882812,
          218.6648406982422)}]}]


XML
~~~

The XML version extracts text (no images) with the detail level of RAWDICT::
 
 <page width="595.276" height="841.89">
 <image bbox="327.526 88.936038 523.276 175.18604" />
 <block bbox="195.483 189.04106 523.2428 218.90952">
 <line bbox="195.483 189.04106 523.2428 218.90952" wmode="0" dir="1 0">
 <font name="SFSX2488" size="24.7871">
 <char bbox="195.483 189.04106 214.19727 218.90952" x="195.483" y="211.052" c="P"/>
 <char bbox="214.19727 189.04106 227.75582 218.90952" x="214.19727" y="211.052" c="y"/>
 <char bbox="227.75582 189.04106 253.18738 218.90952" x="227.75582" y="211.052" c="M"/>
 <char bbox="253.18738 189.04106 268.3571 218.90952" x="253.18738" y="211.052" c="u"/>
 (... omitted data ...)
 </font>
 </line>
 </block>
 <block bbox="404.002 223.5048 523.30477 244.49039">
 <line bbox="404.002 223.5048 523.30477 244.49039" wmode="0" dir="1 0">
 <font name="SFSO1728" size="17.2154">
 <char bbox="404.002 223.5048 416.91358 244.49039" x="404.002" y="238.94702" c="R"/>
 (... omitted data ...)
 <char bbox="513.33706 223.5048 523.30477 244.49039" x="513.33706" y="238.94702" c="0"/>
 </font>
 </line>
 </block>
 (... omitted data ...)
 </page>

.. note:: We have successfully tested `lxml <https://pypi.org/project/lxml/>`_ to interpret this output.

XHTML
~~~~~
A variation of TEXT but in HTML format, containing the bare text and images ("semantic" output)::

 <div>
 <p><img width="195" height="86" src="data:image/jpeg;base64,
 /9j/4AAQSkZJRgABAQEAYABgAAD/4Q (... omitted image data ...)"/></p>
 <p><b>PyMuPDF Documentation</b></p>
 <p><b><i>Release 1.12.0</i></b></p>
 <p><b>Jorj X. McKie</b></p>
 <p><b>Dec 13, 2017</b></p>
 </div>


Further Remarks
~~~~~~~~~~~~~~~~~

1. We have modified MuPDF's **plain text** extraction: The original prints out every line followed by a newline character. This leads to a rather ragged, space-wasting look. We have combined all lines of a text block into one, separating lines by space characters. We also do not add extra newline characters at the end of blocks.

2. The extraction methods each have its own default behavior concerning images: "TEXT" and "XML" do not extract images, while the others do. On occasion it may make sense to **switch off images** for them, too. See chapter :ref:`cooperation` on how to achieve this. To **exclude images**, use an argument of ``3`` when you create the :ref:`TextPage`.

3. Apart from the above "standard" ones, we offer additional extraction methods :meth:`Page.getTextBlocks` and :meth:`Page.getTextWords` for performance reasons. They return lists of a page's text blocks, resp. words. Each list item contains text accompanied by its rectangle ("bbox", location on the page). This should help to resolve extraction issues around multi-column or boxed text.

4. For uttermost detail, down to the level of one character, use RAWDICT extraction.


Performance
~~~~~~~~~~~~
The text extraction methods differ significantly: in terms of information they supply, and in terms of resource requirements. Generally, more information of course means that more processing is required and a higher data volume is generated.

To begin with, all methods are **very fast** in relation to other products out there in the market. In terms of processing speed, we couldn't find a faster (free) tool. Even the most detailed method, RAWDICT, processes all 1'310 pages of the :ref:`AdobeManual` in less than 9 seconds (simple text needs less than 2 seconds here).

Relative to each other, **"RAWDICT"** is about 4.6 times slower than **"TEXT"**, the others range between them. The following table shows **relative runtimes** with **"TEXT"** set to 1, measured across ca. 1550 text-heavy and 250 image-heavy pages.

======= ====== =====================================================================
Method  Time   Comments
======= ====== =====================================================================
TEXT     1.00  no images, plain text, line breaks
WORDS    1.07  no images, word level text with bboxes
BLOCKS   1.10  image bboxes (only), block level text with bboxes
XML      2.30  no images, char level text, layout and font details
DICT     2.68  **binary** images, span level text, layout and font details
XHTML    3.51  **base64** images, span level text, no layout info
HTML     3.60  **base64** images, span level text, layout and font details
RAWDICT  4.61  **binary** images, char level text, layout and font details
======= ====== =====================================================================

In versions prior to v1.13.1, JSON was a standalone extraction method. Since we have added the DICT extraction, JSON output is now created from it, using the **json** module contained in Python for serialization. We believe, DICT output is more handy for the programmer's purpose, because all of its information is directly usable -- including images. Previously, for JSON, you had to bsae64-decode images before you could use them. We also have replaced the old "imgtype" dictionary key (an integer bit code) with the key "ext", which contains the appropriate extension string for the image.

Look into the previous chapter **Appendix 1** for more performance information.
