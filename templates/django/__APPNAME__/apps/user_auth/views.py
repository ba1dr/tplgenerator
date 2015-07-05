import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import TemplateView, DetailView, FormView
from django.views.decorators.csrf import csrf_exempt

from utils.decorators import authenticated_redirect

from .forms import ProfileForm, AvatarForm
from .models import Account


@login_required
def view_profile(request, username):
    """View Profile"""
    selected_user = Account.objects.get(username=username)

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
    except Exception, e:
        print e

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
            return redirect('dashboard')

        error = 'Could not authenticate user'

    context = {
        'error': error
    }

    return render(request, 'user_auth/login.html', context)


@csrf_exempt
@login_required
def auth_logout(request):
    """Logout"""
    logout(request)
    return redirect('home')
