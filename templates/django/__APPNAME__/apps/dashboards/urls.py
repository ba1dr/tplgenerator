# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^dashboard$', login_required(views.DashboardView.as_view()), name='dashboard'),
]
