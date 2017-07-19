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

    url(r'^(?P<work_set_id>[0-9]+)/previous_work/$', views.previous_work, name='previous_work'),

    url(r'^start_work/$', views.start_work, name='start_work'),

    url(r'^submit_work/$', views.submit_work, name='submit_work'),

    url(r'^(?P<work_set_id>[0-9]+)/finish_work/$', views.finish_work, name='finish_work'),

    url(r'^(?P<work_set_id>[0-9]+)/show_summary/$', views.show_summary, name='show_summary'),

    url(r'^(?P<work_set_id>[0-9]+)/query_review_sentence_table/$', views.query_review_sentence_table,
        name='query_review_sentence_table'),
    # ajax data valid function
    url(r'^valid_file_name/$', views.valid_file_name, name='valid_file_name'),
    url(r'^valid_ticket_number/$', views.valid_ticket_number, name='valid_file_name'),

    url(r'^unit_test/$', views.unit_test, name='unit_test'),

]
