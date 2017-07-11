# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class WorkSet(models.Model):
    work_set_name = models.CharField(description='work set name', max_length=255)
    work_set_status = models.BooleanField(description='if work set been completely', default=False)


class AnnotationReviewItem(models.Model):
    annotation_review_index = models.IntegerField()
    annotation_review_result = models.IntegerField()
    annotation_review_text = models.CharField(max_length=1000)
    annotation_sentence = models.CharField(max_length=250)
    work_set_count = models.IntegerField()
    work_set = models.ForeignKey(WorkSet)

