#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# @author: Bartosz Nowak sztosz@gmail.com

from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns(
    '',
    url(r'^$', SReturnsList.as_view(), name='list'),
    url(r'^create/$', SCreateReturn.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', SReturn.as_view(), name='return'),
    url(r'^(?P<return_pk>\d+)/waybill/create/$', SCreateWaybill.as_view(), name='waybill_create'),
    url(r'^(?P<return_pk>\d+)/waybill/(?P<waybill_pk>\d+)/$', SWaybill.as_view(), name='waybill'),
    url(r'^(?P<return_pk>\d+)/waybill/(?P<waybill_pk>\d+)/document/create/$',
        SCreateDocument.as_view(), name='document_create'),
    url(r'^(?P<return_pk>\d+)/waybill/(?P<waybill_pk>\d+)/document/(?P<document_pk>\d+)/$',
        SDocument.as_view(), name='document'),
    url(r'^(?P<return_pk>\d+)/waybill/(?P<waybill_pk>\d+)/document/(?P<document_pk>\d+)/commodity/add$',
        SAddCommodityTroughEAN.as_view(), name='commodity_add'),
)
