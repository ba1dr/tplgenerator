# -*- coding: utf-8 -*-

from django.forms import CheckboxInput, TextInput


class CheckboxToggleWidget(CheckboxInput):

    def __init__(self, *args,
                 size='small', on_color='success', off_color='danger', on_text='Yes', off_text='No',
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs['class'] = 'toggle-chkbox'
        self.attrs['data-size'] = size
        self.attrs['data-on-color'] = on_color
        self.attrs['data-off-color'] = off_color
        self.attrs['data-on-text'] = on_text
        self.attrs['data-off-text'] = off_text


class BTSInputWidget(TextInput):

    def __init__(self, *args, **kwargs):
        maxlength = kwargs.pop('max_length', None)
        placeholder = kwargs.pop('placeholder', None)
        css_class = kwargs.pop('css_class', '')
        error_messages = kwargs.pop('error_messages', '')
        super().__init__(*args, **kwargs)
        self.attrs['class'] = self.attrs.get('class', '') + ' form-control ' + css_class
        self.attrs['maxlength'] = maxlength
        self.attrs['placeholder'] = placeholder
        self.attrs['error_messages'] = error_messages
        self.attrs['data-content'] = error_messages
