.. _Widget:

================
Widget
================

This class represents the properties of a PDF Form field, a "widget". Fields are a special case of annotations, which allow users with limited permissions to enter information in a PDF. This is usually used for filling out forms.


**Class API**

.. class:: Widget

    .. attribute:: border_color

       A list of up to 4 floats defining the field's border. Default value is ``None`` which causes border style and border width to be ignored.

    .. attribute:: border_style

       A string defining the line style of the field's border. See :attr:`Annot.border`. Default is "s" ("Solid") - a continuous line.

    .. attribute:: border_width

       A float defining the width of the border line. Default is zero, which rsults in a line width of 1.

    .. attribute:: list_values

       A mandatory Python sequence of strings defining the valid choices of listboxes and comboboxes. Ignored for other field types. Equals :attr:`Annot.widget_choices`. The sequence must contain at least two items.

    .. attribute:: field_name

       A mandatory string defining the field's name. Equals :attr:`Annot.widget_name`. No checking for duplicates takes place.

    .. attribute:: field_value

       The value of the field. Equals :attr:`Annot.widget_value`.

    .. attribute:: field_flags

       An integer defining a large amount of proprties of a field.

    .. attribute:: field_type

       An integer defining the field type. This is a value in the range of 0 to 6.

    .. attribute:: field_type_string

       A string describing the field type.

    .. attribute:: fill_color

       A list of up to 4 floats defining the field's background color.

    .. attribute:: button_caption

       For future use: the caption string of a button-type field.

    .. attribute:: rect

       The rectangle containing the field.

    .. attribute:: text_color

       A list of **3 floats** defining the text color as an RGB value. Default value is black (`[0, 0, 0]`).

    .. attribute:: text_font

       A string defining the font to be used. Default value is ``"Helv"``. For valid font reference names see the table below. If you specify an invalid value, the default ``"Helv"`` will be used.

    .. attribute:: text_fontsize

       A float defining the text fontsize. Default value is zero, which causes PDF viewer software to dynamically choose a size suitable for the annotation's rectangle and text amount.

    .. note:: The attributes :attr:`text_color`, :attr:`text_font` and :attr:`text_fontsize` are only used when adding or updating a field and lose its meaning thereafter. To indicate this, they are set to ``None`` in :attr:`Annot.widget` (which returns all available information of a form field). To see which values are in actual use for a field, look at :attr:`text_da` below.

    .. attribute:: text_maxlen

       An integer defining the maximum number of text characters. PDF viewers will (should) not accept larger text amounts.

    .. attribute:: text_type

       An integer defining acceptable text types (e.g. numeric, date, time, etc.).

    .. attribute:: text_da

       A string defining the field's default appearance. This value cannot be changed directly. It will be generated from information contained in :attr:`text_color`, :attr:`text_font`, and :attr:`text_fontsize` above. It has the general format ``0 0 0 rg /Helv 11 Tf``. Its first three tokens form the RGB text color triple, ``/Helv`` and ``11`` are the font name and size.

Standard Fonts for Widgets
----------------------------------
Widgets use their own resources object ``/DR``. A widget resources object must at least contain a ``/Font`` object. Widget fonts are independent from page fonts. We currently support the 14 PDF base fonts using the following fixed reference names, or any name of an already existing field font. When specifying a text font for new or changed widgets, **either** choose one in the first table column (upper or lower case supported), **or** one of the already existing form fonts. In the latter case, spelling must exactly match.

To find out already existing field fonts, inspect the list :attr:`Document.FormFonts`.

============= =======================
**Reference** **Base14 Fontname**
============= =======================
CoBI          Courier-BoldOblique
CoBo          Courier-Bold
CoIt          Courier-Oblique
Cour          Courier
HeBI          Helvetica-BoldOblique
HeBo          Helvetica-Bold
HeIt          Helvetica-Oblique
Helv          Helvetica **(default)**
Symb          Symbol
TiBI          Times-BoldItalic
TiBo          Times-Bold
TiIt          Times-Italic
TiRo          Times-Roman
ZaDb          ZapfDingbats
============= =======================

You are generally free to use any font for every widget. However, we recommend using ``ZaDb`` ("ZapfDingbats") and fontsize 0 for check boxes: typical viewers will put a correctly sized tickmark in the field's rectangle, when it is clicked.