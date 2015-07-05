from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('landings.views',
    url(r'^$', 'home', name='home'),
    url(r'^dashboard$', 'dashboard', name='dashboard'),
)
