# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from accounts.models import UserInfo
import django.utils.timezone as timezone


# Create your models here.


class WorkSet(models.Model):
    work_set_name = models.CharField('work set name, it equal to the task file name', max_length=255)
    is_complete = models.BooleanField('identify if work set is completely', default=False)
    created_at = models.DateTimeField('work set create datetime', default=timezone.now)
    update_at = models.DateTimeField('work set last modify datetime', auto_now=True)

    user_id = models.ForeignKey(UserInfo)


class ReviewSentence(models.Model):
    review_sentence_index = models.IntegerField('review sentence index for the work set')
    review_sentence_result = models.IntegerField('review sentence result, it should be 1, 2, 3')
    review_sentence_text = models.CharField('review sentence text with annotation info', max_length=1000)
    sentence_text = models.CharField('review sentence origin text without annotation info', max_length=1000)
    language = models.CharField('the language this sentence belong to', max_length=20)
    work_set_count = models.IntegerField('the total number of sentence in work set')
    created_at = models.DateTimeField('review sentence create datetime', default=timezone.now)
    update_at = models.DateTimeField('review sentence last modify datetime', auto_now=True)

    work_set = models.ForeignKey(WorkSet)


class Language(models.Model):
    name = models.CharField('sentence language name', max_length=10)
    created_at = models.DateTimeField('language create datetime', default=timezone.now)
    update_at = models.DateTimeField('language last modify datetime', auto_now=True)


class TaskType(models.Model):
    name = models.CharField('task type name', max_length=50)
    created_at = models.DateTimeField('task type create datetime', default=timezone.now)
    update_at = models.DateTimeField('task type last modify datetime', auto_now=True)
