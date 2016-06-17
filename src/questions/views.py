'''Views page for the questions Caprende module.'''

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect

from analytics.models import CategoryDataSet, SubCategoryDataSet
from comments.forms import CommentForm

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

            #Create or retrieve the data set for the user
            cat_data_set = CategoryDataSet.objects.get_or_create(
                user=request.user,
                category=question.category,
            )[0]
            subcat_data_set = SubCategoryDataSet.objects.get_or_create(
                user=request.user,
                subcategory=question.subcategory,
            )[0]

            #Update the dataset and messages based on correctness
            if not response.correct:
                cat_data_set.add_miss()
                subcat_data_set.add_miss()
                messages.error(request, question.answer_explanation)
            else:
                cat_data_set.add_correct()
                subcat_data_set.add_correct()
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
    comments = question.comment_set.all()
    comment_form = CommentForm()

    for c in comments:
        c.get_children()

    context = {
        "question" : question,
        "response" : response,
        "comments" : comments,
        "comment_form": comment_form
    }
    return render(request, "questions/question_review.html", context)

