#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# @author: Bartosz Nowak sztosz@gmail.com

from django.db import models


class Commodity(models.Model):
    sku = models.CharField(max_length=25, verbose_name='Index towaru (SKU)')
    ean = models.CharField(max_length=13, verbose_name='EAN')
    name = models.CharField(max_length=100, verbose_name='Nazwa towaru')

    def __str__(self):
        if self.name == 'BRAK_TOWARU_W_BAZIE':
            return self.ean
        else:
            return self.name
