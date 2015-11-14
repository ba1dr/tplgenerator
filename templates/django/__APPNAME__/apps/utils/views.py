# -*- coding: utf-8 -*-

from django.views.generic.detail import DetailView, SingleObjectTemplateResponseMixin, BaseDetailView
from django.core.urlresolvers import reverse


class ObjectBaseView(SingleObjectTemplateResponseMixin):
    model = None  # redefine this!
    success_url_name = None
    basetemplate = 'base.html'
    baseajaxtemplate = 'partials/popupform.html'

    def get_object(self, queryset=None):
        try:
            retval = super().get_object(queryset)
            return retval
        except AttributeError:
            return None

    def dispatch(self, request, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        #
        return super().post(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['basetemplate'] = self.basetemplate
        context['ajax'] = False
        if self.request.is_ajax():
            context['ajax'] = True
            context['basetemplate'] = self.baseajaxtemplate
        return context

    def get_success_url(self):
        return reverse(self.success_url_name)
