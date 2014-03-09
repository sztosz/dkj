#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# @author: Bartosz Nowak sztosz@gmail.com


from __future__ import unicode_literals

from django.contrib import admin
from .models import Commodity


class CommodityAdmin(admin.ModelAdmin):
    list_display = ('ean', 'sku', '__str__',)


admin.site.register(Commodity, CommodityAdmin)
