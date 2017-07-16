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
        # c.login(username='lei.jia@nuance.com', password='Motorola123!')
        login_data = {}
        login_data['email'] = 'lei.jia@nuance.com'
        login_data['password'] = 'Motorola123'
        response = c.post("/accounts/login/", data)
        response = c.post("/annotation_review/unit_test/", data)
        self.assertEqual(response.status_code, 400)
