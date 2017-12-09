# -*- coding: utf-8 -*-

import os

from django import forms

from .models import User


def get_theme_list():
    themes = [('default', 'Default')]
    themes_dir = os.path.join(CUR_DIR, '../..', 'public/css/themes')
    if os.path.exists(themes_dir):
        for fname in os.listdir(themes_dir):
            tname = fname[:-8]
            themes.append((tname, tname.title()))
    return themes


class ProfileForm(forms.Form):
    """User Profile Form"""
    email = forms.EmailField()
    first_name = forms.CharField(max_length=40, required=False)
    last_name = forms.CharField(max_length=40, required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self._build_initial()
        super(ProfileForm, self).__init__(*args, **kwargs)

    def _build_initial(self):
        for field in self.base_fields:
            if field in dir(self.user):
                self.base_fields[field].initial = getattr(self.user, field)

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email != self.user.email and User.objects.get(email=email):
            raise forms.ValidationError('That email already exists.')

        return email

    def save(self):
        for field, value in self.cleaned_data.items():
            if field in self.base_fields:
                setattr(self.user, field, value)

        self.user.save()
        return self.user


class UserSettingsForm(forms.Form):
    theme = forms.ChoiceField(choices=get_theme_list(), initial='default', required=False)
