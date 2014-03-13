#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# @author: Bartosz Nowak sztosz@gmail.com
from django import forms

from dkj.common import EanValidator
from . import models


class CreateReturnForm(forms.ModelForm):
    class Meta:
        model = models.Return
        exclude = ('user', 'completed',)


class CreateWaybillForm(forms.ModelForm):
    class Meta:
        model = models.Waybill
        exclude = ('return_id',)


class CreateDocumentForm(forms.ModelForm):
    class Meta:
        model = models.Document
        exclude = ('waybill', 'return_id',)


class AddCommodityTroughEANForm(forms.ModelForm):
    ean = forms.CharField(max_length=13, label='EAN', help_text='13 cyfr')

    class Meta:
        model = models.CommodityInDocument
        exclude = ('return_id', 'waybill', 'document', 'commodity',)

    def clean_ean(self):
        ean = self.cleaned_data['ean']
        validator = EanValidator()
        if not validator.ean_valid(ean):
            raise forms.ValidationError(validator.error)
        return ean
