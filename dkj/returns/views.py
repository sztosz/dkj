#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# @author: Bartosz Nowak sztosz@gmail.com

from django.views.generic import ListView, DetailView, CreateView
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import Http404

from dkj.common import LoggedInMixin
from . import models, forms


class Returns(LoggedInMixin, ListView):
    queryset = models.Return.objects.order_by('-start_date')
    context_object_name = 'returns'


class CreateReturn(LoggedInMixin, CreateView):
    model = models.Return
    form_class = forms.CreateReturnForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('returns:detail', args=(self.object.pk,))


class Details(LoggedInMixin, DetailView):
    model = models.Return
    template_name = None  # TODO template for Returns
    context_object_name = 'return'

    def get_context_data(self, **kwargs):
        context = super(Details, self).get_context_data(**kwargs)
        waybills = models.Waybill.objects.filter(return_id=self.object)
        for waybill in waybills:
            waybill.documents = models.Document.objects.filter(waybill=waybill.pk)
        context['waybills'] = waybills
        # context['documents'] = models.Document.objects.filter(return_id=self.object)
        context['commodities'] = models.CommodityInDocument.objects.filter(return_id=self.object)
        return context


class CreateWaybill(LoggedInMixin, CreateView):
    model = models.Waybill
    template_name = None  # TODO Create AddReturn template
    form_class = forms.CreateWaybillForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.return_id = get_object_or_404(models.Return, pk=self.kwargs['return_pk'])
        obj.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('returns:detail', args=(self.kwargs['return_pk'],))

# class Waybill(LoggedInMixin, DetailView):
#     model = models.Waybill
#     template_name = None  # TODO template for Returns
#     context_object_name = 'waybill'
#
#     def get_context_data(self, **kwargs):
#         context = super(Waybill, self).get_context_data(**kwargs)
#         context['documents'] = models.Document.objects.filter(waybill=self.object)
#         context['commodities'] = models.CommodityInDocument.objects.filter(waybill=self.object)
#         return context


class CreateDocument(LoggedInMixin, CreateView):
    model = models.Document
    template_name = None  # TODO Create AddReturn template
    form_class = forms.CreateDocumentForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.return_id = get_object_or_404(models.Return, pk=self.kwargs['return_pk'])
        obj.waybill = get_object_or_404(models.Waybill, pk=self.kwargs['waybill_pk'])
        if obj.waybill.return_id != obj.return_id:
            raise Http404
        obj.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('returns:detail', args=(self.kwargs['return_pk'],))


# class Document(LoggedInMixin, DetailView):
#     model = models.Waybill
#     template_name = None  # TODO template for Returns
#     context_object_name = 'document'
#
#     def get_context_data(self, **kwargs):
#         context = super(Document, self).get_context_data(**kwargs)
#         context['commodities'] = models.CommodityInDocument.objects.filter(document=self.object)
#         return context



