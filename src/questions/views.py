'''Views page for the questions Caprende module.'''

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect

from analytics.models import CategoryDataSet, SubCategoryDataSet
from comments.forms import CommentForm
from course.models import Course

from .forms import QuestionResponseForm
from .models import Question, QuestionResponse

# Create your views here.

@login_required
def user_question_detail(request):
    '''Return the view of the next question the user has to answer.'''

    return HttpResponseRedirect(reverse('question_detail', kwargs={
        'course_slug' : request.user.profile.course.slug,
        'question_index' : request.user.profile.next_question_index,
    }))

@login_required
def question_detail(request, course_slug, question_index):
    '''Return to the view of the question.'''

    course = Course.objects.all().get(slug=course_slug)
    question = get_object_or_404(Question, course=course, index=question_index)

    #If a response exists, redirect to the review page
    response = QuestionResponse.objects.get_queryset().get_response(user=request.user, question=question)
    if response != None:
        return HttpResponseRedirect(reverse('question_review', kwargs={
            'course_slug' : course.slug,
            'question_index' : question_index,
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

            #Increase the question index for the user.
            request.user.profile.increase_question_index()

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
                'course_slug' : course.slug,
                'question_index' : question_index,
                'response' : answer
            }))
        context = {
            "question" : question,
            "form" : form,
            "practice" : True
        }
        return render(request, "questions/question_detail.html", context)

@login_required
def question_review(request, course_slug, question_index, response):
    '''Return to the view of the question.'''

    question = get_object_or_404(Question, course=Course.objects.all().get(slug=course_slug), index=question_index)
    comments = question.comment_set.all()
    comment_form = CommentForm()

    if question.get_next_url() is None:
        messages.info(request, "Congratulations, you've completed all the questions we offer. Check again soon for more.")

    for c in comments:
        c.get_children()

    context = {
        "question" : question,
        "response" : response,
        "comments" : comments,
        "comment_form": comment_form
    }
    return render(request, "questions/question_review.html", context)
