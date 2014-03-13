#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# @author: Bartosz Nowak sztosz@gmail.com

from django.core.urlresolvers import reverse

from . import views
from . import models


class SReturns(views.Returns):
    queryset = models.Return.objects.filter(completed=False).order_by('-start_date')
    template_name = 'returns/scanner/return_form.html'


class SCreateReturn(views.CreateReturn):

    def get_success_url(self):
        return reverse(None)


class SDetails(views.Details):
    pass
