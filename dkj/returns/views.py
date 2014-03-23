#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# @author: Bartosz Nowak sztosz@gmail.com

import csv

from django.views.generic import ListView, DetailView, CreateView
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse

from dkj.common import LoggedInMixin
from . import models, forms


class ReturnsList(LoggedInMixin, ListView):
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
        return reverse('Returns:return', args=(self.object.pk,))


class Return(LoggedInMixin, DetailView):
    model = models.Return
    context_object_name = 'return'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        waybills = models.Waybill.objects.filter(return_id=self.object)
        for waybill in waybills:
            documents = models.Document.objects.filter(waybill=waybill.pk)
            for document in documents:
                document.commodities = models.CommodityInDocument.objects.filter(document=document.pk)
            waybill.documents = documents
        context['waybills'] = waybills
        # context['documents'] = models.Document.objects.filter(return_id=self.object)
        # context['commodities'] = models.CommodityInDocument.objects.filter(return_id=self.object)
        return context


class ReturnPrint(LoggedInMixin, DetailView):
    model = models.Return
    template_name = 'returns/return_print.html'
    context_object_name = 'return'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['commodities'] = models.CommodityInDocument.objects.filter(return_id=self.object)
        return context


class CreateWaybill(LoggedInMixin, CreateView):
    model = models.Waybill
    form_class = forms.CreateWaybillForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.return_id = get_object_or_404(models.Return, pk=self.kwargs['return_pk'])
        obj.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('Returns:return', args=(self.kwargs['return_pk'],))


class CreateDocument(LoggedInMixin, CreateView):
    model = models.Document
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
        return reverse('Returns:return', args=(self.kwargs['return_pk'],))


class AddCommodityTroughEAN(LoggedInMixin, CreateView):
    model = models.CommodityInDocument
    template_name = None
    form_class = forms.AddCommodityTroughEANForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.return_id = get_object_or_404(models.Return, pk=self.kwargs['return_pk'])
        obj.waybill = get_object_or_404(models.Waybill, pk=self.kwargs['waybill_pk'])
        obj.document = get_object_or_404(models.Document, pk=self.kwargs['document_pk'])
        obj.commodity = get_object_or_404(models.Commodity, ean=form.cleaned_data['ean'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('Returns:return', args=(self.kwargs['return_pk'],))


class CsvExport(Return):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="commercial_return.csv.txt"'

        writer = csv.writer(response, delimiter=';')
        try:
            writer.writerow(['Numer: {}'.format(context['return'].return_number())])
            writer.writerow(['Przewoźnik: {}'.format(context['return'].carrier.name)])
            writer.writerow(['Nazwisko kierowcy: {}'.format(context['return'].driver_name)])
            writer.writerow(['Nr rejestracyjny samochodu: {}'.format(context['return'].car_plates)])
            writer.writerow(['Komentarz: {}'.format(context['return'].comment)])
            writer.writerow(['Data zwrotu: {}'.format(context['return'].start_date)])
            writer.writerow(['Kontroler: {} {}'.format(context['return'].user.first_name,
                                                       context['return'].user.last_name)])
            writer.writerow([''])
            writer.writerow(['Ilość', 'Towar', 'ean', 'List przewozowy', 'Dokument'])
            for row in context['commodities']:
                writer.writerow([row.amount, row.commodity, row.commodity.ean, row.waybill, row.document])
        except KeyError:
            writer.writerow(['Nastąpił błąd parsowania danych: brak towarów w liście'])
        return response
