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
    # url(r'^waybill/(?P<pk>\d+)/$', Details.as_view(), name='waybill_detail'),

    # url(r'^print/(?P<pk>\d+)/$', ReturnPrint.as_view(),
    #     name='print'),
    # url(r'^export/(?P<pk>\d+)/$', ReturnExport.as_view(),
    #     name='export'),
    # url(r'^update/(?P<pk>\d+)/$', CommercialReturnUpdate.as_view(),
    #     name='update'),
    # url(r'^close/(?P<pk>\d+)/$', CommercialReturnClose.as_view(),
    #     name='close'),
    # url(r'^item/add/(?P<pk>\d+)/$', CommercialReturnItemAdd.as_view(),
    #     name='item_add'),
    # url(r'^item/update/(?P<pk>\d+)/$', CommercialReturnItemUpdate.as_view(),
    #     name='item_update'),
    # url(r'^item/delete/(?P<pk>\d+)/$', CommercialReturnItemDelete.as_view(),
    #     name='item_delete'),
)

