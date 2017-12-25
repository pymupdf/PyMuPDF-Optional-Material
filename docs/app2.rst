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
Information contained in a :ref:`TextPage` has the following hierarchy:
::
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

HTML output fully reflects the structure of the page's ``TextPage`` - much like JSON below. This includes images, font information and text positions. If wrapped in HTML header and trailer code, it can readily be displayed be a browser. Our above example::

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

* HTML text contains references to the fonts used of the original document. If these are not known to the browser (a fat chance!), it will replace them with his assumptions, which probably will let the result look awkward. This issue varies greatly by browser - on my Windows machine, MS Edge worked just fine, whereas Firefox looked horrible.

* For PDFs with a complex structure, images may not be positioned and / or sized correctly. This seems to be the case for rotated pages and pages, where the various possible page bbox variants do not coincide (e.g. ``MediaBox != CropBox``). We do not know yet, how to address this - we filed a bug at MuPDF's site.

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



JSON
~~~~

JSON output fully reflects the structure of a ``TextPage`` and provides image content and position details (``bbox`` - boundary boxes in pixel units) for every block and line. This information can be used to present text in another reading order if required (e.g. from top-left to bottom-right). Have a look at `PDF2textJS.py <https://github.com/rk700/PyMuPDF/blob/master/examples/PDF2textJS.py>`_. Images are stored base64 encoded. Here is how this looks like::

 {"width": 595.276, "height": 841.89,
  "blocks": [
   {"type": 1, "bbox": [327.526, 88.936, 523.276, 175.186],
    "imgtype": 8, "width": 261, "height": 115, "image":
 "/9j/4AAQSkZJRgABAQEAYABgAAD/4QBmRXhpZgA (... omitted image data ...) "
   },
   {"type": 0, "bbox": [195.483, 189.041, 523.243, 218.91],
    "lines": [
     {"bbox": [195.483, 189.041, 523.243, 218.91], "wmode": 0, "dir": [1, 0],
      "spans": [
       {"font": "SFSX2488", "size": 24.7871, "flags": 20, "text": "PyMuPDF Documentation"} 
      ]
     }
    ]
   },
   {"type": 0, "bbox": [404.002, 223.505, 523.305, 244.49],
    "lines": [
     {"bbox": [404.002, 223.505, 523.305, 244.49], "wmode": 0, "dir": [1, 0],
      "spans": [
       {"font": "SFSO1728", "size": 17.2154, "flags": 22, "text": "Release 1.12.0"} 
      ]
     }
    ]
   },
   {"type": 0, "bbox": [400.529, 371.31, 517.284, 392.312],
    "lines": [
     {"bbox": [400.529, 371.31, 517.284, 392.312], "wmode": 0, "dir": [1, 0],
      "spans": [
       {"font": "SFSX1728", "size": 17.2154, "flags": 20, "text": "Jorj X. McKie"} 
      ]
     }
    ]
   },
   {"type": 0, "bbox": [448.484, 637.531, 523.252, 652.403],
    "lines": [
     {"bbox": [448.484, 637.531, 523.252, 652.403], "wmode": 0, "dir": [1, 0],
      "spans": [
       {"font": "SFSX1200", "size": 11.9552, "flags": 20, "text": "Dec 13, 2017"} 
      ]
     }
    ]
   }
  ]
 }

XML
~~~

The XML version takes the level of detail even a lot deeper: every single character is provided with its position detail, and every span also contains font information::
 
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

We have successfully tested ``lxml`` to interpret this output.

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

1. We have modified MuPDF's **plain text** extraction: The original prints out every line followed by a newline character. This leads to a rather ragged, space-wasting look. So we have combined all lines of a text block into one, separating lines by space characters (but only if a line does not end with "-"). We also do not add extra newline characters at the end of blocks.

2. The 5 extraction methods each have a default behavior concerning images: "TEXT" and "XML" do not extract images, while the other three do. On occasion it may make sense to switch off images for "HTML", "XHTML" or "JSON", too. See chapter :ref:`cooperation` on how to achieve this. Use an argument of ``3`` when you create the :ref:`TextPage`.

3. Apart from the 5 standard ones, we offer additional extraction methods :meth:`Page.getTextBlocks` and :meth:`Page.getTextWords`. They return lists of a page's text blocks, resp. words. Each list item contains text accompanied by its rectangle ("bbox", location on the page). This should help to resolve extraction issues around multi-column or boxed text.

4. If you need even more detailed positioning information, you can use XML extraction.


Performance
~~~~~~~~~~~~
The text extraction methods differ significantly: in terms of information they supply (see above), and in terms of resource requirements. More information of course means that more processing is required and a higher data volume is generated.

To begin with, all methods are **very** fast in relation to what is out there on the market. In terms of processing speed, we couldn't find a faster (free) tool. Even the most detailed method, XML, processes all 1'310 pages of the :ref:`AdobeManual` in less than 8 seconds.

Relative to each other, **"XML"** is about 2 times slower than **"TEXT"**, the others range between them. E.g. **"JSON", "HTML", "XHTML"**  need about 20% more time than **"TEXT"** (heavily depending on the size of images contained in the document), whereas :meth:`Page.getTextBlocks` and :meth:`Page.getTextWords` are only 1% resp. 3% slower.

Look into the previous chapter **Appendix 1** for more performance information.
