#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# @author: Bartosz Nowak sztosz@gmail.com

from django.views.generic import ListView, DetailView, CreateView
from django.core.urlresolvers import reverse

from dkj.common import LoggedInMixin
from . import models


class Returns(LoggedInMixin, ListView):
    queryset = models.Return.objects.order_by('-start_date')
    template_name = None  # TODO template for Returns


class CreateReturn(LoggedInMixin, CreateView):
    model = models.Return
    template_name = None  # TODO Create AddReturn template
    form_class = None  # TODO Create AddReturn template

    def get_success_url(self):
        return reverse('returns:detail', args=(self.object.pk,))


class Details(LoggedInMixin, DetailView):
    model = models.Return
    template_name = None  # TODO template for Returns
    context_object_name = 'return'

    def get_context_data(self, **kwargs):
        context = super(Details, self).get_context_data(**kwargs)
        context['waybills'] = models.Waybill.objects.filter(return_id=self.object)
        context['commodities'] = models.CommodityInDocument.objects.filter(return_id=self.object)
        return context


class CreateWaybill(LoggedInMixin, CreateView):
    model = models.Waybill
    template_name = None  # TODO Create AddReturn template
    form_class = None  # TODO Create AddReturn template

    def get_success_url(self):
        return reverse('returns:waybill', args=(self.object.pk,))


class Waybill(LoggedInMixin, DetailView):
    model = models.Waybill
    template_name = None  # TODO template for Returns
    context_object_name = 'waybill'

    def get_context_data(self, **kwargs):
        context = super(Waybill, self).get_context_data(**kwargs)
        context['documents'] = models.Document.objects.filter(waybill=self.object)
        context['commodities'] = models.CommodityInDocument.objects.filter(waybill=self.object)
        return context


class CreateDocument(LoggedInMixin, CreateView):
    model = models.Document
    template_name = None  # TODO Create AddReturn template
    form_class = None  # TODO Create AddReturn template

    def get_success_url(self):
        return reverse('returns:document', args=(self.object.pk,))


class Document(LoggedInMixin, DetailView):
    model = models.Waybill
    template_name = None  # TODO template for Returns
    context_object_name = 'document'

    def get_context_data(self, **kwargs):
        context = super(Document, self).get_context_data(**kwargs)
        context['commodities'] = models.CommodityInDocument.objects.filter(document=self.object)
        return context



