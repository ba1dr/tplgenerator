
from django import forms
from django.template.loader import render_to_string
from utils.widgets import CheckboxToggleWidget, BTSInputWidget


class ImprovedForm(object):

    def __init__(self, *args, **kwargs):
        super(ImprovedForm, self).__init__(*args, **kwargs)
        for fname in self.fields:
            if isinstance(self.fields[fname], forms.fields.BooleanField):
                self.fields[fname].widget = CheckboxToggleWidget()
            elif isinstance(self.fields[fname], forms.fields.CharField):
                placeholder = "This field is required" if self.fields[fname].required else self.fields[fname].help_text
                css_class = ""
                self.fields[fname].widget = BTSInputWidget(max_length=self.fields[fname].max_length,
                                                           placeholder=placeholder, css_class=css_class,
                                                           error_messages=placeholder)

    def as_div(self):
        form_style = 'inline'
        context = {'form': self, 'style': form_style}
        result = render_to_string('utils/form_div.html', context)
        return result

    def as_table(self):
        form_style = 'table'
        context = {'form': self, 'style': form_style}
        result = render_to_string('utils/form_table.html', context)
        return result
