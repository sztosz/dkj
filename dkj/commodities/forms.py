#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# @author: Bartosz Nowak sztosz@gmail.com


from django import forms

from . import models


class CommodityImportSingleForm(forms.ModelForm):
    class Meta:
        model = models.Commodity
        fields = ('ean', 'sku', 'name',)


class CommodityImportBatchForm(forms.Form):
    file = forms.FileField(label="Wybierz plik z danymi...")

