# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from accounts.models import UserInfo

# Create your models here.


class WorkSet(models.Model):
    work_set_name = models.CharField(max_length=255)
    is_complete = models.BooleanField(default=False)
    user_id = models.ForeignKey(UserInfo)


class ReviewSentence(models.Model):
    review_sentence_index = models.IntegerField()
    review_sentence_result = models.IntegerField()
    review_sentence_text = models.CharField(max_length=1000)
    sentence_text = models.CharField(max_length=1000)
    language = models.CharField(max_length=20)
    work_set_count = models.IntegerField()
    work_set = models.ForeignKey(WorkSet)

