#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib import auth
from models import UserInfo, RoleList, PermissionList

class LoginUserForm(forms.Form):
    email = forms.CharField(label='Email', error_messages={'required': 'email should not be empty'},
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', error_messages={'required': 'password should not be empty'},
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None

        super(LoginUserForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = auth.authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('email and password not matched !!!')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('this account has been forbit')
        return self.cleaned_data

    def get_user(self):
        return self.user_cache
