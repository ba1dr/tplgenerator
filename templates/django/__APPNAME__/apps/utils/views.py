# -*- coding: utf-8 -*-

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView, SingleObjectTemplateResponseMixin, BaseDetailView
from django.shortcuts import redirect, render_to_response
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


class ObjectListBaseView(ListView):
    template_name = 'utils/list.html'
    content_template_name = 'utils/list_content.html'
    model = None
    FILTER_FIELDS = ['name', ]

    def filter_value(self, qset, fname, fvalue):
        if fname in self.FILTER_FIELDS:
            fd = {fname: fvalue}
            qset = qset.filter(**fd)
        return qset

    def get_pagination_page(self, page=1, maxitems=50, filters=None, sortfield=None, sortasc='1'):
        items = self.get_queryset()
        if filters:
            for ff in filters:
                ffs = ff.split('*', 1)
                if len(ffs) > 1:
                    fname, fvalue = ffs
                    items = self.filter_value(items, fname, fvalue)
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
        page = kwargs.pop('page', 1)
        maxitems = kwargs.pop('maxitems', 50)
        filters = kwargs.pop('filters', [])
        sortfield = kwargs.pop('sortfield', None)
        sortasc = kwargs.pop('sortasc', None)
        if not self.request.is_ajax():
            lfilter = self.get_filter_vals()
            context['filters'] = lfilter
        context['items'] = self.get_pagination_page(page, maxitems)
        context['prelast'] = context['items'].paginator.num_pages - 1
        context['sortfield'] = sortfield
        return context

    def get_queryset(self):
        return self.model.objects.all()

    def get_filter_vals(self):
        retval = []
        for fld in self.FILTER_FIELDS:
            retval.append((fld, sorted(list(self.get_queryset().values_list(fld, flat=True).distinct()))))
        return retval

    def get(self, request):
        if not request.is_ajax():
            return super().get(request)
        page = request.GET.get('page', 1)
        filters = request.GET.getlist('filters[]', [])
        maxitems = request.GET.get('maxitems', 50)
        sortfield = request.GET.get('sort', 'id')
        sortasc = str(request.GET.get('asc', '1'))
        context = self.get_context_data(page=page, maxitems=maxitems,
                                        filters=filters, sortfield=sortfield, sortasc=sortasc)
        return render_to_response(self.content_template_name, context)
