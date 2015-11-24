# -*- coding: utf-8 -*-

from django.forms import CheckboxInput, TextInput
from django.forms.widgets import Widget
from django.forms.fields import Field
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


class BTSInputWidget(TextInput):

    def __init__(self, *args, **kwargs):
        maxlength = kwargs.pop('max_length', None)
        placeholder = kwargs.pop('placeholder', None)
        css_class = kwargs.pop('css_class', '')
        error_messages = kwargs.pop('error_messages', '')
        super().__init__(*args, **kwargs)
        self.attrs['class'] = self.attrs.get('class', '') + ' form-control ' + css_class
        if maxlength:
            self.attrs['maxlength'] = maxlength
        if placeholder:
            self.attrs['placeholder'] = placeholder
        self.attrs['error_messages'] = error_messages
        self.attrs['data-content'] = error_messages


class PlainTextWidget(Widget):

    def __init__(self, *args, **kwargs):
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

    def __init__(self, tag='span', safe_text=True, html_text=None, *args, **kwargs):
        self.tag = tag
        self.safe_text = safe_text
        self.html_text = html_text  # extended text, maybe with additional formatting, will replace value
        super().__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        widget.tag = self.tag
        widget.safe_text = self.safe_text
        widget.html_text = self.html_text
        return attrs

    def validate(self, value):
        pass
