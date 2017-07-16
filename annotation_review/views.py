# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from .models import ReviewSentence, Language, TaskType, WorkSet
# from accounts.permission import permission_verify
from accounts.models import UserInfo
from django.views.decorators.csrf import csrf_exempt
from lib import file_accessor1
import os


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
def detail(request, annotation_review_id):
    try:
        review_sentence = ReviewSentence.objects.get(pk=annotation_review_id)
        # review_sentence = ReviewSentence()
        # review_sentence.review_sentence_index = 1
        # review_sentence.review_sentence_text = "This is just example"
        # review_sentence.work_set_count = 200
        # review_sentence.id = 1
        # review_sentence.language = "zh-cn"

    except ReviewSentence.DoesNotExist:
        raise Http404("Annotation Review Item does not exist")
    return render(request, 'annotation_review/detail.html', {'review_sentence': review_sentence})


@login_required()
def vote(request, annotation_review_id):
    result = request.POST['optionsRadios']
    p = get_object_or_404(ReviewSentence, pk=annotation_review_id)
    try:
        result = request.POST['optionsRadios']
        p.annotation_review_result = result
    except:
        # Redisplay the question voting form.
        return render(request, 'annotation_review/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        p.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('annotation_review:detail', args=(p.id + 1,)))


@login_required()
def skip(request, annotation_review_id):
    return HttpResponseRedirect(reverse('annotation_review:detail', args=(1,)))


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
    work_set = WorkSet(work_set_name=work_set_name, is_complete=False, ticket_number=ticket_number, task_type=task_type,
                       user=user)
    work_set.save()
    accessor = file_accessor1.FileAccessor(file_path)
    sentence_list = accessor.read_file()
    if sentence_list:
        i = 1
        for sentence in sentence_list:
            review_sentence = ReviewSentence(review_sentence_index=i, review_sentence_result=0,
                                             review_sentence_text=sentence, sentence_text="", language=language.id,
                                             work_set_count=len(sentence_list), work_set=work_set)
            review_sentence.save()
            i = i + 1
    return HttpResponseRedirect(reverse('annotation_review:detail', args=(1,)))


@login_required()
def continue_work(request):
    work_set_id = request.POST['work_set_id']
    work_set = WorkSet.objects.get(id=work_set_id)
    sentence_review_list = work_set.reviewsentence_set.filter(review_sentence_result=0).order_by(
        "review_sentence_index")
    return HttpResponseRedirect(
        reverse('annotation_review:detail', args=(sentence_review_list[0].review_sentence_index,)))


@csrf_exempt
def valid_file_name(request):
    file_name = request.POST['file_name']
    accessor = file_accessor1.FileAccessor(file_name)
    valid = accessor.file_exit_valid()
    response = '{"valid":%s}' % valid
    return HttpResponse(response.lower())


@csrf_exempt
def valid_ticket_number(request):
    ticket = request.POST['ticket_number']
    return HttpResponse('{"valid":true}')


def unit_test(request):
    user = UserInfo.objects.get(email=request.user)
    language_name = request.POST['language_name']
    if language_name and language_name < 10:
        raise Http404("Annotation Review Item does not exist")
    return HttpResponse('Good')
