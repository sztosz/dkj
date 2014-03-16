#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# @author: Bartosz Nowak sztosz@gmail.com

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from .. import views
from .. import models


class ScannerLoggedInMixin(views.LoggedInMixin):
    redirect_url = '/Slogin/?next={0}'


class SReturnsList(ScannerLoggedInMixin, views.ReturnsList):
    queryset = models.Return.objects.filter(completed=False).order_by('-start_date')
    template_name = 'returns/scanner/return_list.html'


class SCreateReturn(ScannerLoggedInMixin, views.CreateReturn):
    template_name = 'returns/scanner/return_form.html'

    def get_success_url(self):
        return reverse('Returns:SReturns:return', args=(self.object.pk,))


class SReturn(ScannerLoggedInMixin, views.Return):
    template_name = 'returns/scanner/return.html'


class SCreateWaybill(ScannerLoggedInMixin, views.CreateWaybill):
    template_name = 'returns/scanner/waybill_form.html'

    def get_success_url(self):
        return reverse('Returns:SReturns:waybill', args=(self.object.return_id.pk, self.object.pk))


class SWaybill(ScannerLoggedInMixin, views.DetailView):
    model = models.Waybill
    pk_url_kwarg = 'waybill_pk'
    context_object_name = 'waybill'
    template_name = 'returns/scanner/waybill.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['documents'] = models.Document.objects.filter(waybill=self.object)
        context['return'] = get_object_or_404(models.Return, pk=self.object.return_id.pk)
        return context


class SCreateDocument(ScannerLoggedInMixin, views.CreateDocument):
    template_name = 'returns/scanner/document_form.html'

    def get_success_url(self):
        return reverse('Returns:SReturns:document', args=(self.object.return_id.pk, self.object.waybill.pk,
                                                          self.object.pk))


class SDocument(ScannerLoggedInMixin, views.DetailView):
    model = models.Document
    pk_url_kwarg = 'document_pk'
    context_object_name = 'document'
    template_name = 'returns/scanner/document.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['commodities'] = models.CommodityInDocument.objects.filter(document=self.object)
        context['waybill'] = get_object_or_404(models.Waybill, pk=self.object.waybill.pk)
        context['return'] = get_object_or_404(models.Return, pk=self.object.return_id.pk)
        return context


class SAddCommodityTroughEAN(ScannerLoggedInMixin, views.AddCommodityTroughEAN):
    template_name = 'returns/scanner/commodityindocument_form.html'

    def get_success_url(self):
        return reverse('Returns:SReturns:document', args=(self.object.return_id.pk, self.object.waybill.pk,
                                                          self.object.document.pk))
