# -*- coding: utf-8 -*-

import os

from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, DetailView, FormView
from django.views.decorators.csrf import csrf_exempt

from utils.decorators import authenticated_redirect

from .forms import ProfileForm
from .models import User


@login_required
def view_profile(request, username):
    """View Profile"""
    selected_user = User.objects.get(username=username)

    context = {
        'selected_user': selected_user
    }

    return render(request, 'view_profile.html', context)


@login_required
def edit_profile(request):
    """Edit Profile"""
    user = request.user
    form = ProfileForm(request.POST or None, user=user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard')

    context = {
        'user': user,
        'form': form
    }

    return render(request, 'edit_profile.html', context)


@login_required
def edit_avatar(request):
    """Edit User Avatar"""
    user = request.user
    form = AvatarForm(request.POST or None, request.FILES or None, user=user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('edit-avatar')

    context = {
        'user': user,
        'form': form
    }

    return render(request, 'avatar.html', context)


@login_required
def remove_avatar(request):
    """Remove User Avatar"""
    file_path = request.user.avatar.path

    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)

    request.user.avatar = None
    request.user.save()

    return redirect('edit-avatar')


@authenticated_redirect
def auth_login(request):
    """Login Page"""
    error = None

    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'),
                            password=request.POST.get('password'))

        if user and user.is_active:
            login(request, user)
            redirect_to = request.POST.get(REDIRECT_FIELD_NAME,
                                           request.GET.get(REDIRECT_FIELD_NAME, '/'))
            return HttpResponseRedirect(redirect_to)

        error = 'Could not authenticate user'

    context = {
        'error': error,
        'redirect_field_name': REDIRECT_FIELD_NAME,
        'nextpage': request.GET.get(REDIRECT_FIELD_NAME, request.POST.get(REDIRECT_FIELD_NAME, '/'))
    }

    return render(request, 'user_auth/login.html', context)


@csrf_exempt
@login_required
def auth_logout(request):
    """Logout"""
    logout(request)
    return redirect('home')
