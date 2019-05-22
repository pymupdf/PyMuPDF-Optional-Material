==============
Glossary
==============

.. data:: contents

        "A **content stream** is a PDF :data:`stream` :data:`object` whose data consists of a sequence of instructions describing the graphical elements to be painted on a page." (:ref:`AdobeManual` p. 151). For an overview of the mini-language used in these streams see chapter "Operator Summary" on page 985 of the :ref:`AdobeManual`. A PDF :data:`page` can have none to many contents objects. If it has none, the page is empty. If it has several, they will be interpreted in sequence as if their instructions had been present in one such object (i.e. like in a concatenated string). It should be noted that there are more stream object types which use the same syntax: e.g. appearance dictionaries associated with annotations and Form XObjects.

.. data:: resources

        A :data:`dictionary` containing any resources required by a PDF :data:`page` (required, inheritable, :ref:`AdobeManual` p. 145) and certain other objects (Form XObjects).

.. data:: dictionary

        A PDF :data:`object` type, which is somewhat comparable to the same-named Python notion: "A dictionary object is an associative table containing pairs of objects, known as the dictionary’s entries. The first element of each entry is the key and the second element is the value. The key must be a name (...). The value can be any kind of object, including another dictionary. A dictionary entry whose value is null (...) is equivalent to an absent entry." (:ref:`AdobeManual` p. 59).
        
        Dictionaries are the most important :data:`object` type in PDF. Here is an example (describing a :data:`page`)::

            <<
            /Contents 40 0 R                  % value: indirect object
            /Type/Page                        % value: name object
            /MediaBox[0 0 595.32 841.92]      % value: array object
            /Rotate 0                         % value: number object
            /Parent 12 0 R
            /Resources<<                      % value: dictionary object
                /ExtGState<</R7 26 0 R>>
                /Font<<
                     /R8 27 0 R/R10 21 0 R/R12 24 0 R/R14 15 0 R
                     /R17 4 0 R/R20 30 0 R/R23 7 0 R /R27 20 0 R
                     >>
                /ProcSet[/PDF/Text]           % value: array of two names
                >>
            /Annots[55 0 R]                   % value: array, one entry (indirect object)
            >>

        ``/Contents``, ``/Type``, ``/MediaBox``, etc. are **keys**, ``40 0 R``, ``/Page``, ``[0 0 595.32 841.92]``, etc. are the respective **values**. The strings ``<<`` and ``>>`` are used to enclose object definitions.
        
        This example also shows the syntax of **nested** dictionary values: ``/Resources`` has an object as its value, which in turn is a dictionary with keys like ``/ExtGState`` (with the value ``<</R7 26 0 R>>``, another dictionary), etc.

.. data:: page

        A PDF page is a :data:`dictionary` object which defines one page in the document, see :ref:`AdobeManual` p. 145.

.. data:: object

        Similar to Python, PDF supports the notion *object*, which can come in eight basic types: boolean values, integer and real numbers, strings, names, arrays, dictionaries, streams, and the null object (:ref:`AdobeManual` p. 51). Objects can be made identifyable by assigning a label. This label is then called *indirect* object. PyMuPDF supports retrieving definitions of indirect objects via their label (the cross reference number) via :meth:`Document._getXrefString`.

.. data:: stream

        A PDF :data:`object` type which is a sequence of bytes, similar to a string. "However, a PDF application can read a stream incrementally, while a string must be read in its entirety. Furthermore, a stream can be of unlimited length, whereas a string is subject to an implementation limit. For this reason, objects with potentially large amounts of data, such as images and page descriptions, are represented as streams." "A stream consists of a :data:`dictionary` followed by zero or more bytes bracketed between the keywords *stream* and *endstream*"::

            dictionary
            stream
            … zero or more bytes …
            endstream

        See :ref:`AdobeManual` p. 60. PyMuPDF supports retrieving stream content via :meth:`Document._getXrefStream`. Use :meth:`Document.isStream` to determine whether an object is of stream type.

.. data:: xref 

        Abbreviation for cross-reference number: this is an integer unique identification for objects in a PDF. There exists a cross-reference table (which may consist of several separate segments) in each PDF, which stores the relative position of each object for quick lookup. The cross-reference table is one entry longer than the number of existing object: item zero is reserved and must not be used in any way. Many PyMuPDF classes have an ``xref`` attribute (which is zero for non-PDFs), and one can find out the total number of objects in a PDF via :meth:`Document._getXrefLength`.