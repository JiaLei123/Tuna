# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.test import Client
import json

# Create your tests here.

class AnnotationReviewTestCase(TestCase):
    def setUp(self):
        pass

    def test_start_work(self):
        c = Client()
        data = {}
        data['language_name'] = 10
        data['task_type_name'] = 1
        data['file_name'] = r'H:\Chinese_translation_Util\News.grm'
        data['ticket_number'] = 'PTNLU_2276'

        response = c.post("/start_work/", json.dumps(data))
