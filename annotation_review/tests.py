# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, RequestFactory
from django.test import Client
from accounts.models import UserInfo
from .views import unit_test
import json

# Create your tests here.

class AnnotationReviewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserInfo.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        pass

    def test_start_work(self):
        c = Client()
        data = {}
        data['language_name'] = 10
        data['task_type_name'] = 1
        data['file_name'] = r'H:\Chinese_translation_Util\News.grm'
        data['ticket_number'] = 'PTNLU_2276'
        # c.login(username='lei.jia@nuance.com', password='Motorola123!')

        # response = c.post("/annotation_review/unit_test/", data)

        request = self.factory.post('/customer/details', data)
        request.user = self.user

        response = unit_test(request)
        self.assertEqual(response.status_code, 400)
