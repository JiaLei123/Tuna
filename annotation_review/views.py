# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from accounts.permission import permission_verify

@login_required()
# @permission_verify()
def index(request):
    return render(request, 'annotation_review/index.html')
