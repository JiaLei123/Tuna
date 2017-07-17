# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.test import Client
from accounts.models import UserInfo
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

        user = UserInfo.objects.create_user(email='lei.jia@nuance.com', username='jeff_jia',password='Motorola123!')
        user.save()
        login_data = {}
        login_data['email'] = 'lei.jia@nuance.com'
        login_data['password'] = 'Motorola123!'
        response_login = c.post("/accounts/login/", login_data)
        cookis_tocken = response_login.cookies

        response = c.post("/annotation_review/unit_test/", data, cookis_tocken)
        self.assertEqual(response.status_code, 400)
