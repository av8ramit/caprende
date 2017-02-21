'''Views page for the questions Caprende module.'''

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect

from analytics.models import CategoryDataSet, SubCategoryDataSet
from comments.forms import CommentForm
from course.models import Course

from .forms import QuestionResponseForm
from .models import Question, QuestionResponse
from .utils import next_question_url, prev_question_url

# Create your views here.

@login_required
def user_question_detail(request):
    '''Return the view of the next question the user has to answer.'''

    if request.user.profile.course is None:
        messages.error(request, "Please select a course prior to completing questions.")
        return redirect("edit_profile")

    return HttpResponseRedirect(reverse('question_detail', kwargs={
        'course_slug' : request.user.profile.course.slug,
        'question_index' : request.user.profile.next_question_index,
    }))

@login_required
def question_detail(request, course_slug, question_index):
    '''Return to the view of the question.'''

    course = Course.objects.all().get(slug=course_slug)
    question = get_object_or_404(Question, course=course, index=question_index)
    category_data_set = CategoryDataSet.objects.sort_by_user(request.user).filter(category=question.category)

    if len(category_data_set) == 0:
        total = 0
        correct = 0
    else:
        correct = category_data_set[0].correct
        total = correct + category_data_set[0].missed

    prev_url = prev_question_url(question, request.user.profile)
    next_url = next_question_url(question, request.user.profile)

    #If a response exists, redirect to the review page
    response = QuestionResponse.objects.get_queryset().get_response(user=request.user, question=question)
    if response != None:
        return HttpResponseRedirect(reverse('question_review', kwargs={
            'course_slug' : course.slug,
            'question_index' : question_index,
            'response' : response.attempt
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
                messages.error(request, "You answered incorrectly. Please check the answer and explanation for help.")
            else:
                cat_data_set.add_correct()
                subcat_data_set.add_correct()
                messages.success(request, "Congratulations! You answered correctly.")

            return HttpResponseRedirect(reverse('question_review', kwargs={
                'course_slug' : course.slug,
                'question_index' : question_index,
                'response' : answer
            }))
        context = {
            "question" : question,
            "form" : form,
            "practice" : True,
            "correct" : correct,
            "total" : total,
            "prev_url" : prev_url,
            "next_url" : next_url,
        }
        return render(request, "questions/question_detail.html", context)

@login_required
def question_review(request, course_slug, question_index, response):
    '''Return to the view of the question.'''

    question = get_object_or_404(Question, course=Course.objects.all().get(slug=course_slug), index=question_index)
    category_data_set = CategoryDataSet.objects.sort_by_user(request.user).filter(category=question.category)
    correct = category_data_set[0].correct
    total = correct + category_data_set[0].missed

    comments = question.comment_set.all()
    comment_form = CommentForm()

    prev_url = prev_question_url(question, request.user.profile)
    next_url = next_question_url(question, request.user.profile)
    if next_url is None:
        messages.info(request, "Congratulations, you've completed all the questions we offer. Check again soon for more.")

    for c in comments:
        c.get_children()

    context = {
        "question" : question,
        "response" : response,
        "comments" : comments,
        "practice" : True,
        "comment_form": comment_form,
        "correct" : correct,
        "total" : total,
        "prev_url" : prev_url,
        "next_url" : next_url,
    }
    return render(request, "questions/question_review.html", context)
