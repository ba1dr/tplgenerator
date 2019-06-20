
from django.contrib.auth import get_user_model, authenticate, login, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.views import (
    LoginView as BaseLoginView, LogoutView as BaseLogoutView,
    PasswordChangeView as BasePasswordChangeView
)
from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, DetailView, FormView

from utils.views import ViewMixin
from .forms import UserProfileForm

User = get_user_model()


class LoginView(BaseLoginView):
    template_name = 'login.html'


class LogOutView(BaseLogoutView):
    def get(self, *args, **kwargs):
        return redirect('home')


class PasswordChangeView(ViewMixin, BasePasswordChangeView):
    page_title = 'Change Password'


class UserProfileView(TemplateView):
    template_name = 'user_auth/view_profile.html'
    mode = 'view'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.mode == 'view':
            context['page_title'] = 'View Profile'
            self.template_name = 'user_auth/view_profile.html'
        elif self.mode == 'edit':
            context['page_title'] = 'Edit Profile'
            self.template_name = 'user_auth/edit_profile.html'
        return context

    def post(self, *args, **kwargs):
        form = UserProfileForm(self.request.POST or None, instance=self.request.user)
        if form.is_valid():
            form.save()
            return redirect('view-profile')
        context = self.get_context_data(*args, **kwargs)
        context['form'] = form
        return render(self.request, self.template_name, context)


class UserSettingsView(ViewMixin, TemplateView):
    template_name = 'settings.html'
    page_title = 'User Settings'

    def post(self, *args, **kwargs):
        return redirect('settings')
        context = self.get_context_data(*args, **kwargs)
        return render(self.request, self.template_name, context)
