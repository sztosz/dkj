#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# @author: Bartosz Nowak sztosz@gmail.com

from django.shortcuts import redirect


class LoggedInMixin(object):
    """ A mixin requiring a user to be logged in. """
    redirect_url = '/login/?next={0}'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect(self.redirect_url.format(request.path))
        return super(LoggedInMixin, self).dispatch(request, *args, **kwargs)


class EanValidator():
    EAN13_weights = '1313131313131'
    kinds = ['ean13']
    conditions = {
        'ean13': {
            'weight': '1313131313131',
            'length': 13},
    }

    def __init__(self, kind='ean13'):
        if kind not in self.kinds:
            raise TypeError('Incorrect ean type: {}'.format(kind))
        self.weight = self.conditions[kind]['weight']
        self.correct_length = self.conditions[kind]['length']
        self.error = None
        self.valid = False

    def ean_check(self, ean):
        length = len(ean)
        ean = str(ean).strip(   )
        try:
            int(ean)
        except ValueError:
            self.error = 'Expected only digits, got instead  {0}'.format(ean)
            self.valid = False
            return
        if length != self.correct_length:
            self.error = 'Expected length: {0} got instead  {1}'.format(length, self.correct_length)
            self.valid = False
            return
        checksum = 0
        for i in range(length - 1):
            checksum += int(ean[i]) * int(self.weight[i])
        checksum = 10 - checksum % 10
        if checksum == 10:
            checksum = 0
        if checksum == int(str(ean)[-1]):
            self.valid = True
            return
        else:
            self.error = 'Expected checksum {0}, got instead  {1}'.format(str(ean)[-1], checksum)
            self.valid = False
            return

    def ean_valid(self, ean=None):
        if ean:
            self.ean_check(ean)
        return self.valid


