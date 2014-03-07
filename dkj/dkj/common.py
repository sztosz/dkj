#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# @author: Bartosz Nowak sztosz@gmail.com

from django.shortcuts import redirect


class LoggedInMixin(object):
    """ A mixin requiring a user to be logged in. """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/login/?next={0}'.format(request.path))
        return super(LoggedInMixin, self).dispatch(request, *args, **kwargs)
