#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import render, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from forms import LoginUserForm
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

# Create your views here.
def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'Get' and request.GET.has_key('next'):
        next_page = request.GET['next']
    else:
        next_page = '/'
    if next_page == '/accounts/logout/':
        next_page = '/'
    if request.method == 'POST':
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            return HttpResponseRedirect(request.POST['next'])
    else:
        form = LoginUserForm(request)
    kwargs = {
        'request': request,
        'form': form,
        'next': next_page,
    }

    return render(request, 'accounts/login.html', kwargs)

@login_required()
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))