#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response,redirect



def index(request):
    return redirect('/annotation_review/index/')