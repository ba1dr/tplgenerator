# -*- coding: utf-8 -*-

from django.forms import CheckboxInput, TextInput, PasswordInput
from django.forms.widgets import Widget, NumberInput, Textarea, Select
from django.forms.extras.widgets import SelectDateWidget
from django.forms.fields import Field, CharField
from django.forms.utils import flatatt
from django.utils.html import format_html
from django.utils.encoding import force_text


class CheckboxToggleWidget(CheckboxInput):

    def __init__(self, *args,
                 size=None, on_color=None, off_color=None, on_text=None, off_text=None,
                 **kwargs):
        css_class = kwargs.pop('css_class', '')
        attrs = kwargs.get('attrs', {})
        super().__init__(*args, **kwargs)
        self.attrs['class'] = self.attrs.get('class', '') + ' form-control toggle-chkbox ' + css_class
        self.attrs['data-size'] = size or attrs.get('data-size') or 'small'
        self.attrs['data-on-color'] = on_color or attrs.get('data-on-color') or 'success'
        self.attrs['data-off-color'] = off_color or attrs.get('data-off-color') or 'danger'
        self.attrs['data-on-text'] = on_text or attrs.get('data-on-text') or 'Yes'
        self.attrs['data-off-text'] = off_text or attrs.get('data-off-text') or 'No'


class BTSInputMixin(object):
    def set_class(self, newclass):
        # adds CSS class for the field's widget
        classes = list(c for c in self.attrs.get('class', '').split(' ') if c)
        self.attrs['class'] = ' '.join(set(classes + newclass.split(' ')))

    def unset_class(self, oldclass):
        # adds CSS class for the field's widget
        classes = list(c for c in self.attrs.get('class', '').split(' ') if c)
        if oldclass in classes:
            classes.remove(oldclass)
        self.attrs['class'] = ' '.join(set(classes))

    def has_css_class(self, classname):
        return classname in self.attrs.get('class', '').split(' ')

    def __init__(self, *args, **kwargs):
        input_type = kwargs.pop('input_type', None)
        if input_type:
            self.input_type = input_type
        maxlength = kwargs.pop('max_length', None)
        placeholder = kwargs.pop('placeholder', None)
        css_class = kwargs.pop('css_class', '')
        error_messages = kwargs.pop('error_messages', '')
        self.numtype = kwargs.pop('numtype', '')
        super().__init__(*args, **kwargs)
        self.set_class('form-control')
        if css_class:
            self.set_class(css_class)
        if maxlength:
            self.attrs['maxlength'] = maxlength
        if placeholder:
            self.attrs['placeholder'] = placeholder
        self.attrs['error_messages'] = error_messages
        self.attrs['data-content'] = error_messages

    @property
    def is_hidden(self):
        if super().is_hidden:
            return True
        return self.has_css_class('hidden')


class BTSSelectDateWidget(BTSInputMixin, SelectDateWidget):
    pass


class BTSSelectWidget(BTSInputMixin, Select):
    pass


class BTSTextArea(BTSInputMixin, Textarea):
    pass


class BTSInputWidget(BTSInputMixin, TextInput):
    pass


class BTSPasswordWidget(BTSInputMixin, PasswordInput):
    pass


class BTSNumInputWidget(BTSInputMixin, NumberInput):
    input_type = 'text'

    def value_from_datadict(self, data, files, name):
        """
        Given a dictionary of data and this widget's name, returns the value
        of this widget. Returns None if it's not provided.
        """
        retval = data.get(name, None)
        if retval and isinstance(retval, str):
            retval = retval.replace(',', '')  # we assume it was formatting addon
        return retval

    def _format_value(self, value):
        if self.numtype == 'float':
            value = "%.2f" % value
            return value
        return super()._format_value(value)


class PlainTextWidget(Widget):

    def set_class(self, newclass):
        # adds CSS class for the field's widget
        classes = list(c for c in self.attrs.get('class', '').split(' ') if c)
        self.attrs['class'] = ' '.join(set(classes + newclass.split(' ')))

    def __init__(self, *args, **kwargs):
        self.attrs = {}
        self.tag = kwargs.pop('tag', None)
        self.safe_text = kwargs.pop('safe_text', None)
        # extended text, maybe with additional formatting, will replace value
        self.html_text = kwargs.pop('html_text', None)
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs)
        if value and self.safe_text:
            # if safe_text is False - use value as is, do not escape text
            value = force_text(value)
        if self.html_text:
            value = self.html_text
        return format_html('<%s{}>%s</%s>' % (self.tag, value, self.tag), flatatt(final_attrs))


class PlainTextField(Field):
    widget = PlainTextWidget

    def __init__(self, required=False, tag='span', safe_text=True, html_text=None, *args, **kwargs):
        self.tag = tag
        self.safe_text = safe_text
        self.html_text = html_text  # extended text, maybe with additional formatting, will replace value
        super().__init__(required, *args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        widget.tag = self.tag
        widget.safe_text = self.safe_text
        widget.html_text = self.html_text
        return attrs

    def validate(self, value):
        pass
