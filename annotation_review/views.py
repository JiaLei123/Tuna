#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from .models import ReviewSentence, Language, TaskType, WorkSet, ErrorPattern
# from accounts.permission import permission_verify
from accounts.models import UserInfo
from django.views.decorators.csrf import csrf_exempt
from lib import file_accessor
import os
import json
import sys


result_mapping = {
    0: "Not Reivew",
    1: "Correct",
    2: "Incorrect",
    3: "Ambiguous",
    4: "Skip"
}


# first index page


@login_required()
# @permission_verify()
def index(request):
    language_list = Language.objects.all()
    task_type_list = TaskType.objects.all()
    user = UserInfo.objects.get(email=request.user)
    work_set_list = user.workset_set.filter(is_complete=False)
    context = {
        "language_list": language_list,
        "task_type_list": task_type_list,
        'work_set_list': work_set_list
    }
    return render(request, 'annotation_review/index.html', context)


@login_required()
def start_work(request):
    user = UserInfo.objects.get(email=request.user)

    language_name = request.POST['language_name']
    language = Language.objects.get(id=language_name)

    task_type_name = request.POST['task_type_name']
    task_type = TaskType.objects.get(id=task_type_name)

    file_path = request.POST['file_name']
    ticket_number = request.POST['ticket_number']
    work_set_name = os.path.basename(file_path)

    try:
        work_set_db = WorkSet.objects.get(work_set_name=work_set_name)
    except WorkSet.DoesNotExist:
        pass
    else:
        return HttpResponseRedirect(reverse('annotation_review:error'))

    work_set = WorkSet(work_set_name=work_set_name, is_complete=False, ticket_number=ticket_number, task_type=task_type,
                       user=user)
    work_set.save()
    accessor = file_accessor.FileAccessor(file_path)
    sentence_list = accessor.read_file()
    if sentence_list:
        i = 1
        for sentence in sentence_list:
            review_sentence = ReviewSentence(review_sentence_index=i, review_sentence_result=0,
                                             review_sentence_text=sentence, sentence_text="", language=language.id,
                                             work_set_count=len(sentence_list), work_set=work_set)
            review_sentence.save()
            i = i + 1

    # get the first review sentence for this work set
    review_sentence_start = ReviewSentence.objects.filter(work_set=work_set, review_sentence_index=1).values()

    return HttpResponseRedirect(reverse('annotation_review:detail', args=(review_sentence_start.id,)))


@login_required()
def continue_work(request):
    work_set_id = request.POST['work_set_id']
    work_set = WorkSet.objects.get(id=work_set_id)
    sentence_review_list = work_set.reviewsentence_set.filter(review_sentence_result=0).order_by(
        "review_sentence_index")
    return HttpResponseRedirect(
        reverse('annotation_review:detail', args=(sentence_review_list[0].review_sentence_index,)))


# Second do annotation review page


@login_required()
def detail(request, annotation_review_id):
    """
    after check start work or continue work button, the will redirect to detail page then will invoke this function
    :param request:
    :param annotation_review_id:
    :return:
    """
    try:
        review_sentence = ReviewSentence.objects.get(pk=annotation_review_id)
        language = Language.objects.get(pk=review_sentence.language).name
        process = review_sentence.review_sentence_index/review_sentence.work_set_count
        work_set = WorkSet.objects.get(pk=review_sentence.work_set_id)
        context = {
            "work_set": work_set,
            "review_sentence": review_sentence,
            "language": language,
            'process': process
        }
    except ReviewSentence.DoesNotExist:
        raise Http404("Annotation Review Item does not exist")
    return render(request, 'annotation_review/detail.html', context)


@login_required()
def vote(request, annotation_review_id):
    """
    submit the each annotation sentence review result
    :param request:
    :param annotation_review_id:
    :return:
    """
    review_sentence = get_object_or_404(ReviewSentence, pk=annotation_review_id)
    try:
        result = request.POST['optionsRadios']
        review_sentence.review_sentence_result = int(result)
    except:
        # Redisplay the question voting form.
        return render(request, 'annotation_review/detail.html', {
            'review_sentence': review_sentence,
            'error_message': "You didn't select a choice.",
        })
    else:
        review_sentence.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.

        # TODO: should check if it is the last sentence
        return HttpResponseRedirect(reverse('annotation_review:detail', args=(review_sentence.id + 1,)))


@login_required()
def skip(request, annotation_review_id):
    return HttpResponseRedirect(reverse('annotation_review:detail', args=(1,)))


# Third annotation review summary page


@login_required()
def show_summary(request, work_set_id):
    user = UserInfo.objects.get(email=request.user)
    work_set = WorkSet.objects.get(pk=work_set_id)

    error_pattern_list = ErrorPattern.objects.all()
    if not error_pattern_list or len(error_pattern_list) < 1:
        error_pattern1 = ErrorPattern(error_pattern_text="Test error Pattern 退|<unk> 出|<unk> 地|<app> 图|<app>",
                                      error_pattern_status=0, work_set=work_set)
        error_pattern1.save()
        error_pattern2 = ErrorPattern(error_pattern_text="Test error Pattern 酷|<app> 狗|<app>", error_pattern_status=0,
                                      work_set=work_set)
        error_pattern2.save()

    error_pattern_list = ErrorPattern.objects.all()

    context = {
        "work_set": work_set,
        "error_pattern_list": error_pattern_list
    }

    return render(request, 'annotation_review/result.html', context)


@login_required()
def query_review_sentence_table(request, work_set_id):
    reload(sys)
    sys.setdefaultencoding('utf8')

    user = UserInfo.objects.get(email=request.user)
    work_set = WorkSet.objects.get(pk=work_set_id)
    review_sentence_list = work_set.reviewsentence_set.all()

    json_result_list = dict()

    result_list = list()

    for review_sentence in review_sentence_list:
        review_sentence_split = review_sentence.review_sentence_text.split('\t')
        sentence_json = dict()
        sentence_json["sentence_id"] = review_sentence.review_sentence_index
        sentence_json["review_sentence_parse_type"] = review_sentence_split[0]
        review_sentence_mention = review_sentence_split[1].encode('utf-8')
        review_sentence_mention = review_sentence_mention.replace(u'<', '&lt').replace(u'>', '&gt')
        sentence_json["review_sentence_mentions"] = review_sentence_mention
        sentence_json["result"] = result_mapping[review_sentence.review_sentence_result]
        if review_sentence.correct_sentence_text:
            correct_sentence_split = review_sentence.correct_sentence_text.split('\t')
            sentence_json["correct_sentence_parse_type"] = correct_sentence_split[0]
            correct_sentence_mention = review_sentence_split[1].encode('utf-8')
            correct_sentence_mention = correct_sentence_mention.replace(u'<', '&lt').replace(u'>', '&gt')
            sentence_json["correct_sentence_mentions"] = correct_sentence_mention
        result_list.append(sentence_json)

    json_result_list["total"] = len(review_sentence_list)
    json_result_list["rows"] = result_list

    result = json.dumps(json_result_list)
    return HttpResponse(result)


@login_required()
def previous_work(request, work_set_id):
    work_set = WorkSet.objects.get(id=work_set_id)
    sentence_review_list = work_set.reviewsentence_set.filter(review_sentence_result=0).order_by(
        "review_sentence_index")
    return HttpResponseRedirect(
        reverse('annotation_review:detail', args=(sentence_review_list[0].review_sentence_index,)))


@login_required()
def submit_work(request):
    """
    submit work set to finish the annotation review for currently work set
    To finish the work it need:
    1. Save the error pattern
    2  change the work set status to finish status
    :param request:
    :return:
    """
    work_set_id = request.POST['work_set_id']
    return HttpResponseRedirect(reverse('annotation_review:finish_work', args=(work_set_id,)))


# Forth Finish page
@login_required()
def finish_work(request, work_set_id):
    work_set_id = request.POST['work_set_id']
    work_set = get_object_or_404(WorkSet, pk=work_set_id)
    context = {
        "work_set": work_set,
    }
    return render(request, 'annotation_review/complete.html', context)


# Fifth Edit page


# Sixth Error Page
def error_page(request):
    return render(request, 'annotation_review/error.html')

# Ajax data valid function

@csrf_exempt
def valid_file_name(request):
    file_name = request.POST['file_name']
    accessor = file_accessor.FileAccessor(file_name)
    valid = accessor.file_exit_valid()

    response = '{"valid":%s}' % valid
    return HttpResponse(response.lower())


@csrf_exempt
def valid_ticket_number(request):
    ticket = request.POST['ticket_number']
    return HttpResponse('{"valid":true}')


@csrf_exempt
def review_sentence_check(request):
    work_set_id = request.POST['review_sentence_check']
    work_set = WorkSet.objects.get(pk=work_set_id)
    review_sentence_list = work_set.reviewsentence_set.all()
    valid = True
    for x in review_sentence_list:
        if x.review_sentence_result == 0:
            valid = False
            break
    response = '{"valid":%s}' % valid
    return HttpResponse(response.lower())


@login_required()
def unit_test(request):
    user = UserInfo.objects.get(email=request.user)
    language_name = request.POST['language_name']
    if language_name and language_name < 10:
        raise Http404("Annotation Review Item does not exist")
    return HttpResponse('Good')
