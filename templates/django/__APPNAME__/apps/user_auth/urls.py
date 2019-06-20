
from django.conf.urls import include, url
from django.views.generic.base import TemplateView
from django.contrib.auth import views as djauth_v
from django.contrib.auth.decorators import login_required

from registration.backends.default.views import RegistrationView, ActivationView
from registration.forms import RegistrationFormUniqueEmail

from utils.decorators import authenticated_redirect
from . import views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogOutView.as_view(), name='logout'),
    url(r'^profile/$', login_required(views.UserProfileView.as_view(mode='view')), name='view-profile'),
    url(r'^profile/edit/$', views.UserProfileView.as_view(mode='edit'), name='edit-profile'),
    url(r'^settings/$', login_required(views.UserSettingsView.as_view()), name='settings'),

    url(
        r'^reset/$',
        djauth_v.PasswordResetView.as_view(**{
            'template_name': 'user_auth/passwordreset/reset.html',
            'email_template_name': 'user_auth/passwordreset/email.html',
            'subject_template_name': 'user_auth/passwordreset/subject.txt',
        }),
        name='password_reset'
    ),
    url(
        r'^reset/sent/$',
        djauth_v.PasswordResetDoneView.as_view(**{
            'template_name': 'user_auth/passwordreset/sent.html',
        }),
        name='password_reset_done'
    ),
    url(
        r'^reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        djauth_v.PasswordResetConfirmView.as_view(**{
            'template_name': 'user_auth/passwordreset/confirm.html',
        }),
        name='password_reset_confirm'
    ),
    url(
        r'^reset/done/$',
        djauth_v.PasswordResetCompleteView.as_view(**{
            'template_name': 'user_auth/passwordreset/done.html',
        }),
        name='password_reset_complete'
    ),
    url(
        r'^profile/password/$',
        views.PasswordChangeView.as_view(**{
            'template_name': 'user_auth/change_password.html',
            # 'post_change_redirect': 'dashboard',
        }),
        name='change_password'
    ),
    url(r'profile/password/done', djauth_v.PasswordChangeDoneView.as_view(), name='password_change_done'),
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
