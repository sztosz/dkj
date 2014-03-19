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
    number = forms.CharField(max_length=11, label='List Przewozowy', help_text='Podaj 10 cyfr')

    class Meta:
        model = models.Waybill
        exclude = ('return_id',)

    def clean_number(self):
        number = self.cleaned_data['number']
        number = ''.join([d for d in number if d.isdigit()])
        if len(number) != 10:
            raise forms.ValidationError('List musi się składać z dokładnie 10 cyfr')
        return number


class CreateDocumentForm(forms.ModelForm):
    DOCUMENT_KINDS = (
        ('FS', 'FS'),
        ('MMW', 'MMW'),
    )
    kind = forms.ChoiceField(choices=DOCUMENT_KINDS, label='Rodzaj')
    discriminant = forms.CharField(max_length=3, label='Wyróżnik')
    number = forms.CharField(max_length=8, label='Numer')
    year = forms.CharField(max_length=4, label='rok')

    class Meta:
        model = models.Document
        exclude = ('waybill', 'return_id', 'number')

    def clean_number(self):
        number = self.cleaned_data['number']
        try:
            number = int(number)
            return str(number)
        except ValueError:
            raise forms.ValidationError('Numer musi się składać z samych cyfr')

    def clean_year(self):
        year = self.cleaned_data['year']

        try:
            year = int(year)
            return str(year)
        except ValueError:
            raise forms.ValidationError('Rok musi się składać z samych cyfr')

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['number'] = "{1}-{2}/{3}/{4}".format(cleaned_data['kind'], cleaned_data['discriminant'],
                                                          cleaned_data['number'], cleaned_data['year'])


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
