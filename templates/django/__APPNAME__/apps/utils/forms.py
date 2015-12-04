
from django import forms
from django.template.loader import render_to_string
from django.forms.extras.widgets import SelectDateWidget

from utils.widgets import CheckboxToggleWidget, BTSInputWidget, BTSNumInputWidget


class ImprovedForm(object):

    def __init__(self, *args, **kwargs):
        super(ImprovedForm, self).__init__(*args, **kwargs)
        self.reinit_widgets()

    def add_class(self, field_name, newclass):
        # get css class from the given widget and returns the string with new class
        classes = list(c for c in self.fields[field_name].widget.attrs.get('class', '').split(' ') if c)
        return ' '.join(set(classes + newclass.split(' ')))

    def set_widget_class(self, field_name, newclass):
        # adds CSS class for the field's widget
        self.fields[field_name].widget.attrs['class'] = self.add_class(field_name, newclass)

    def reinit_widgets(self):
        super(ImprovedForm, self).__init__(*args, **kwargs)
        for fname in self.fields:
            if isinstance(self.fields[fname].widget, forms.HiddenInput):
                continue
            prev_widget_args = self.fields[fname].widget.attrs
            widget_args = {'attrs': prev_widget_args}
            if isinstance(self.fields[fname], forms.fields.BooleanField):
                widget_args.update({
                    #
                })
                self.fields[fname].required = False  # to allow False values to be accepted
                self.fields[fname].widget = CheckboxToggleWidget(**widget_args)
            elif isinstance(self.fields[fname], (forms.fields.CharField, forms.fields.IntegerField, )):
                placeholder = "This field is required" if self.fields[fname].required else self.fields[fname].help_text
                css_class = ""
                widget_args.update({
                    'placeholder': placeholder, 'css_class': css_class,
                    'error_messages': placeholder
                })
                if isinstance(self.fields[fname], forms.fields.IntegerField):
                    # widget_args['attrs'].update({'type': 'number'})
                    widget_args['attrs'].update({'class': self.add_class(fname, 'number-field')})
                    self.fields[fname].widget = BTSNumInputWidget(**widget_args)
                elif isinstance(self.fields[fname], forms.fields.CharField):
                    widget_args['max_length'] = self.fields[fname].max_length
                    self.fields[fname].widget = BTSInputWidget(**widget_args)
                    self.fields[fname].widget = BTSInputWidget(**widget_args)

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
