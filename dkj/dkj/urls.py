#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# @author: Bartosz Nowak sztosz@gmail.com
from django.conf.urls import patterns, include, url
from django.contrib import admin

from .views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dkj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^returns/', include('returns.urls', namespace='Returns')),
    url(r'^commodities/', include('commodities.urls', namespace='Commodities')),

    url(r'^$', Index.as_view(), name='index'),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'dkj/login.html'},
        name='login'),
    url(r'^Slogin/$', 'django.contrib.auth.views.login', {'template_name': 'dkj/s_login.html'},
        name='Slogin'),
    url(r'^img/svg_barcode/(?P<ean>\d+)/$', 'dkj.common.sgv_ean_barcode', name='svg_barcode'),

)
