# -*- coding: utf-8 -*-

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.generic.list import ListView
from django.views.generic.edit import ModelFormMixin, ProcessFormView
from django.views.generic.detail import DetailView, SingleObjectTemplateResponseMixin, BaseDetailView
from django.shortcuts import redirect, render_to_response
from django.urls import reverse
from django.http import Http404


class ViewMixin:
    page_title = ''

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = self.page_title
        return context


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


class BaseCreateUpdateView(ObjectBaseView, ModelFormMixin, ProcessFormView):
    template_name = None
    form_class = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.form_class and not self.model:
            self.model = self.form_class._meta.model

    def get_object(self, queryset=None):
        try:
            obj = super().get_object(queryset)
            if not obj:
                obj = self.model()
            return obj
        except Http404:
            raise
        return self.model()


class ObjectListBaseView(ListView):
    template_name = 'utils/list.html'
    content_template_name = 'utils/list_content.html'
    model = None
    FILTER_FIELDS = [('name', 'Name'), ]

    def filter_value(self, qset, fname, fdname, fvalue):
        if fdname.endswith('?'):
            fvalue = True if fvalue == 'True' else False
            fd = {"%s" % fname: fvalue}
            qset = qset.filter(**fd)
        else:
            fd = {"%s__iexact" % fname: fvalue}
            qset = qset.filter(**fd)
        return qset

    def get_pagination_page(self, page=1, maxitems=50, filters=None, sortfield=None, sortasc='1'):
        self.object_list = items = self.get_queryset()
        if filters:
            for ff in filters:
                ffs = ff.split('*', 1)
                if len(ffs) > 1:
                    fname, fvalue = ffs
                    for ffield, ffname in self.FILTER_FIELDS:
                        if ffield == fname:
                            items = self.filter_value(items, fname, ffname, fvalue)
        if sortfield:
            if sortasc == '0':
                items = items.order_by("-%s" % sortfield)
            else:
                items = items.order_by("%s" % sortfield)
        paginator = Paginator(items, maxitems)
        try:
            page = int(page)
        except ValueError:
            page = 1

        try:
            items = paginator.page(page)
        except (EmptyPage, InvalidPage):
            items = paginator.page(paginator.num_pages)

        return items

    def get_context_data(self, **kwargs):
        context = {}
        # context = super().get_context_data()
        context['enable_list_reload_btn'] = True
        page = kwargs.pop('page', 1)
        maxitems = kwargs.pop('maxitems', 50)
        filters = kwargs.pop('filters', [])
        sortfield = kwargs.pop('sortfield', None)
        sortasc = kwargs.pop('sortasc', None)
        context['auto_refresh'] = self.request.GET.get('arefresh') == 'true'
        if not self.request.is_ajax():
            lfilter = self.get_filter_vals()
            context['filters'] = lfilter
        context['items'] = self.get_pagination_page(page, maxitems, filters=filters,
                                                    sortfield=sortfield, sortasc=sortasc)
        context['prelast'] = context['items'].paginator.num_pages - 1
        context['sortfield'] = sortfield
        return context

    def get_queryset(self):
        return self.model.objects.all()

    def get_filter_vals(self):
        def get_val(vv):
            if vv is None:
                return ''
            return str(vv)

        retval = []
        for fld, fname in self.FILTER_FIELDS:
            retval.append((fname, fld, sorted(get_val(v)
                                              for v in set(self.get_queryset().values_list(fld, flat=True)))))
        return retval

    def get(self, request):
        if not request.is_ajax():
            return super().get(request)
        page = request.GET.get('page', 1)
        filters = request.GET.getlist('filters[]', [])
        maxitems = request.GET.get('maxitems', 50)
        sortfield = request.GET.get('sort', 'id')
        sortasc = str(request.GET.get('sortasc', '1'))
        context = self.get_context_data(page=page, maxitems=maxitems,
                                        filters=filters, sortfield=sortfield, sortasc=sortasc)
        self.template_name = self.content_template_name
        return self.render_to_response(context)
