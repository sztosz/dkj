#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# @author: Bartosz Nowak sztosz@gmail.com

from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns(
    '',
    url(r'^$', Returns.as_view(), name='list'),
    url(r'^create/$', CreateReturn.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', Details.as_view(), name='detail'),
    url(r'^(?P<return_pk>\d+)/waybill/create$', CreateWaybill.as_view(), name='waybill_create'),
    url(r'^(?P<return_pk>\d+)/waybill/(?P<waybill_pk>\d+)/document/create$', CreateDocument.as_view(),
        name='document_create'),
    url(r'^(?P<return_pk>\d+)/waybill/(?P<waybill_pk>\d+)/document/(?P<document_pk>\d+)/commodity/add$',
        AddCommodityTroughEAN.as_view(), name='commodity_add'),
    url(r'^(?P<pk>\d+)/csv$', CsvExport.as_view(), name='csv'),
    )
