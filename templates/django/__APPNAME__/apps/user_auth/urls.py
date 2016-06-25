# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib.auth import views as djauth_v

from registration.backends.default.views import RegistrationView, ActivationView
from registration.forms import RegistrationFormUniqueEmail

from utils.decorators import authenticated_redirect
from . import views


urlpatterns = [
    url(r'^login/$', views.auth_login, name='login'),
    url(r'^logout/$', views.auth_logout, name='logout'),
    url(r'profile/edit/$', views.edit_profile, name='edit-profile'),
    url(r'profile/picture/$', views.edit_avatar, name='edit-avatar'),
    url(r'profile/picture/remove/$', views.remove_avatar, name='remove-avatar'),
    url(r'profile/view/(?P<username>[\w0-9-_]+)/$', views.view_profile, name='view-profile'),
    url(
        r'^reset/$',
        djauth_v.password_reset,
        {
            'template_name': 'user_auth/passwordreset/reset.html',
            'email_template_name': 'user_auth/passwordreset/email.html',
            'subject_template_name': 'user_auth/passwordreset/subject.txt',
        },
        name='password_reset'
    ),
    url(
        r'^reset/sent/$',
        djauth_v.password_reset_done,
        {
            'template_name': 'user_auth/passwordreset/sent.html',
        },
        name='password_reset_done'
    ),
    url(
        r'^reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        djauth_v.password_reset_confirm,
        {
            'template_name': 'user_auth/passwordreset/confirm.html',
        },
        name='password_reset_confirm'
    ),
    url(
        r'^reset/done/$',
        djauth_v.password_reset_complete,
        {
            'template_name': 'user_auth/passwordreset/done.html',
        },
        name='password_reset_complete'
    ),
    url(
        r'^profile/password/$',
        djauth_v.password_change,
        {
            'template_name': 'user_auth/change_password.html',
            'post_change_redirect': 'dashboard',
        },
        name='change_password'
    ),
    url(
        r'^activate/complete/$',
        TemplateView.as_view(
            template_name='user_auth/activation/complete.html'
        ),
        name='registration_activation_complete'
    ),
    url(
        r'^activate/(?P<activation_key>\w+)/$',
        ActivationView.as_view(
            template_name='user_auth/activation/activate.html'
        ),
        name='registration_activate'
    ),
    url(
        r'^register/$',
        authenticated_redirect(
            RegistrationView.as_view(
                form_class=RegistrationFormUniqueEmail,
                template_name='user_auth/registration/form.html'
            )
        ),
        name='register'
    ),
    url(
        r'^register/email_sent/$',
        TemplateView.as_view(
            template_name='user_auth/registration/complete.html'
        ),
        name='registration_complete'
    ),
    url(
        r'^register/not_allowed/$',
        TemplateView.as_view(
            template_name='user_auth/registration/disallowed.html'
        ),
        name='registration_disallowed'
    ),
]
