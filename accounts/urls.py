#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from accounts import user
from accounts import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordResetForm

urlpatterns = [
    url(r'^login/$', user.login, name='login'),
    url(r'^logout/$', user.logout, name='logout'),
    url(r'^password_reset/$', user.PasswordResetView.as_view(), name='password_reset'),
    url(r'^change_password/$', user.change_password, name='change_password'),
]
