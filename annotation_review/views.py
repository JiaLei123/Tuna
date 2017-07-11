# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from .models import AnnotationReviewItem, WorkSet
# from accounts.permission import permission_verify

@login_required()
# @permission_verify()
def index(request):
    return render(request, 'annotation_review/index.html')


def vote(request, annotation_review_id):
    p = get_object_or_404(AnnotationReviewItem, pk=annotation_review_id)
    try:
        result = request.POST['optionsRadios']
        p.annotation_review_result = result
    except:
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        p.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:', args=(p.id,)))

