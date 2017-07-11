#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include
import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),

    # ex: /annotation_review/5/
    url(r'^(?P<annotation_review_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /annotation_review/5/vote/
    url(r'^(?P<annotation_review_id>[0-9]+)/vote/$', views.vote, name='vote'),
    # ex: /annotation_review/5/skip/
    url(r'^(?P<annotation_review_id>[0-9]+)/skip/$', views.skip, name='skip'),
]