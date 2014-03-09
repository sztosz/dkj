#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# @author: Bartosz Nowak sztosz@gmail.com
from django import forms

from . import models


class CreateReturnForm(forms.ModelForm):
    class Meta:
        model = models.Return
        exclude = ('user', 'completed',)
