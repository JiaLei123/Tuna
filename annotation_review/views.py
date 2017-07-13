# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from .models import ReviewSentence, WorkSet
# from accounts.permission import permission_verify
from accounts.models import UserInfo
from django.views.decorators.csrf import csrf_exempt

@login_required()
# @permission_verify()
def index(request):
    return render(request, 'annotation_review/index.html', locals())

@login_required()
def detail(request, annotation_review_id):
    try:
        # annotation_review_item = AnnotationReviewItem.objects.get(pk=annotation_review_id)
        review_sentence= ReviewSentence()
        review_sentence.review_sentence_index=1
        review_sentence.review_sentence_text="This is just example"
        review_sentence.work_set_count = 200
        review_sentence.id = 1
        review_sentence.language = "zh-cn"

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
def continue_work(request):
    iUser = UserInfo.objects.get(username=request.user)




@csrf_exempt
def valid_ticket_number(request):
    ticket = request.POST['ticket_number']
    return HttpResponse('{"valid":true}')
