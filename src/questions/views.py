'''Views page for the questions Caprende module.'''

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect


from .forms import QuestionResponseForm
from .models import Question, QuestionResponse

# Create your views here.

@login_required
def question_detail(request, course, question_id):
    '''Return to the view of the question.'''

    question = get_object_or_404(Question, id=question_id)

    #If a response exists, redirect to the review page
    response = QuestionResponse.objects.get_queryset().get_response(user=request.user, question=question)
    if response != None:
        return HttpResponseRedirect(reverse('question_review', kwargs={
            'course' : course,
            'question_id' : question_id,
            'response' : response.attempt,
        }))

    #First user attempt at this question
    else:
        form = QuestionResponseForm(request.POST or None)
        if form.is_valid():
            answer = form.cleaned_data.get("answer")
            response = QuestionResponse.objects.create_response(
                user=request.user,
                question=question,
                attempt=answer,
            )
            response.save()
            if not response.correct:
                messages.error(request, question.answer_explanation)
            else:
                messages.success(request, question.answer_explanation)
            return HttpResponseRedirect(reverse('question_review', kwargs={
                'course' : course,
                'question_id' : question_id,
                'response' : answer
            }))
        context = {
            "question" : question,
            "form" : form
        }
        return render(request, "questions/question_detail.html", context)

@login_required
def question_review(request, course, question_id, response):
    '''Return to the view of the question.'''
    question = get_object_or_404(Question, id=question_id)
    context = {
        "question" : question,
        "response" : response,
    }
    return render(request, "questions/question_review.html", context)

