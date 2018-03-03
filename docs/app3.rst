================================================
Appendix 3: Considerations on Embedded Files
================================================
This chapter provides some background on embedded files support in PyMuPDF.

General
----------
Starting with version 1.4, PDF supports embedding arbitrary files as part ("Embedded File Streams") of a PDF document file (see chapter 3.10.3, pp. 184 of the :ref:`AdobeManual`).

In many aspects, this is comparable to concepts also found in ZIP files or the OLE technique in MS Windows. PDF embedded files do, however, *not* support directory structures as does the ZIP format. An embedded file can in turn contain embedded files itself.

Advantages of this concept are that embedded files are under the PDF umbrella, benefitting from its permissions / password protection and integrity aspects: all files a PDF may reference or even be dependent on can be bundled into it and so form a single, consistent unit of information.

In addition to embedded files, PDF 1.7 adds *collections* to its support range. This is an advanced way of storing and presenting meta information (i.e. arbitrary and extensible properties) of embedded files.

MuPDF Support
-----------------
MuPDF v1.11 added initial support for embedded files and collections (also called *portfolios*).

The library contains functions to add files to the ``EmbeddedFiles`` name tree and display some information of its entries.

Also supported is a full set of functions to maintain collections (advanced metadata maintenance) and their relation to embedded files.

PyMuPDF Support
------------------
Starting with PyMuPDF v1.11.0 we fully reflect MuPDF's support for embedded files and partly go beyond that scope:

* We can add, extract **and** delete embedded files.
* We can display **and** change some meta information (outside collections). Informations available for display are **name**, **filename**, **description**, **length** and compressed **size**. Of these properties, *filename* and *description* can also be changed, after a file has been embedded.

Support of the *collections* feature has been postponed to a later version. We will probably include this ever only on user request.