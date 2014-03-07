#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# @author: Bartosz Nowak sztosz@gmail.com


from __future__ import unicode_literals

from django.contrib import admin
from .models import ReturnCarrier, Return, Waybill, Document, CommodityInDocument


class CommercialReturnCarrierAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


class CommercialReturnAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'carrier', 'carrier_comment', 'completed', 'driver_name', 'user',)


class WaybillAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'return_id',)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'waybill', 'return_id',)


class CommodityInDocumentAdmin(admin.ModelAdmin):
    list_display = ('commodity', 'document', 'waybill', 'return_id')

admin.site.register(ReturnCarrier, CommercialReturnCarrierAdmin)
admin.site.register(Return, CommercialReturnAdmin)
admin.site.register(Waybill, WaybillAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(CommodityInDocument, CommodityInDocumentAdmin)
