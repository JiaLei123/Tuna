#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include
import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    # ex: /annotation_review/5/
    url(r'^(?P<annotation_review_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /annotation_review/5/vote/
    url(r'^(?P<annotation_review_id>[0-9]+)/vote/$', views.vote, name='vote'),
    # ex: /annotation_review/5/skip/
    url(r'^(?P<annotation_review_id>[0-9]+)/skip/$', views.skip, name='skip'),
    # ex: /annotation_review/continue/
    url(r'^continue_work/$', views.continue_work, name='continue_work'),

    url(r'^start_work/$', views.start_work, name='start_work'),

    # ajax data valid function
    url(r'^valid_file_name/$', views.valid_file_name, name='valid_file_name'),
    url(r'^valid_ticket_number/$', views.valid_ticket_number, name='valid_file_name'),

]
