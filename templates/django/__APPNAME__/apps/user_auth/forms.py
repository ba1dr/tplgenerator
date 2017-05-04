# -*- coding: utf-8 -*-

from django import forms

from .models import Account


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

        if email != self.user.email and Account.objects.get(email=email):
            raise forms.ValidationError('That email already exists.')

        return email

    def save(self):
        for field, value in self.cleaned_data.items():
            if field in self.base_fields:
                setattr(self.user, field, value)

        self.user.save()
        return self.user
