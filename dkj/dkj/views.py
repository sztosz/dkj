#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# @author: Bartosz Nowak sztosz@gmail.com

from django.views.generic import TemplateView


class Index(TemplateView):

    template_name = 'dkj/index.html'
