'''Views page for the course Caprende module.'''
# pylint: disable=no-member

import json

from django.contrib import messages
from django.shortcuts import redirect, render

from categories.models import Category, SubCategory
from notifications.models import Notification
from questions.models import Question
from users.models import UserProfile

from .forms import CourseUploadForm, QuestionUploadForm
from .models import Course, CourseSection

# Create your views here.

def course_detail(request, slug):
    '''Returns the view to the course page.'''

    course = Course.objects.get(slug=slug)
    context = {
        "course" : course,
    }
    course_form = CourseUploadForm(request.POST or None, request.FILES or None, initial={"course_json_file" : course.course_json_file})
    question_form = QuestionUploadForm(request.POST or None, request.FILES or None, initial={"question_json_file" : course.question_json_file})

    #Add a form if an admin user is logged in
    if str(request.user) != "AnonymousUser" and request.user.is_admin:
        context["course_form"] = course_form
        context["question_form"] = question_form

    # Course form validation
    if course_form.is_valid():
        json_file = course_form.cleaned_data.get("course_json_file")

        # Verify the JSON file and inject any new sections, categories, and subcategories
        if json_file != None:
            if str(json_file)[-5:] != ".json" and str(json_file)[-5:] != ".JSON":
                messages.error(request, "Please specify a appropriate JSON file.")
            else:
                #course.course_json_file = json_file
                #course.save()
                data = json.load(json_file)
                for section in data.keys():
                    coursesection, _ = CourseSection.objects.get_or_create(name=section, course=course)
                    coursesection.save()
                    for category in data[section].keys():
                        cat, _ = Category.objects.get_or_create(name=category, section=coursesection)
                        cat.save()
                        for subcategory in data[section][category]:
                            subcat, _ = SubCategory.objects.get_or_create(name=subcategory, category=cat)
                            subcat.save()
                messages.success(request, "JSON file for courses was successfully uploaded.")

    # Question form validation
    if question_form.is_valid():
        json_file = question_form.cleaned_data.get("question_json_file")

        # Verify the JSON file and inject any new sections, categories, and subcategories
        if json_file != None:
            if str(json_file)[-5:] != ".json" and str(json_file)[-5:] != ".JSON":
                messages.error(request, "Please specify a appropriate JSON file.")
            else:
                #course.question_json_file = json_file
                #course.save()
                data = json.load(json_file)
                for index in data.keys():
                    json_course = Course.objects.get(name=data[index]["course"])
                    if json_course != course:
                        messages.error(request, "The question %s does not belong to this course." % index)
                        continue
                    section = CourseSection.objects.get(name=data[index]["section"], course=course)
                    category = Category.objects.get(name=data[index]["category"], section=section)
                    subcategory = SubCategory.objects.get(name=data[index]["subcategory"], category=category)
                    question, _ = Question.objects.get_or_create(
                        index=int(index),
                        course=course,
                        section=section,
                        category=category,
                        subcategory=subcategory,
                        passage=data[index]["passage"],
                        question_text=data[index]["text"],
                        option_A=data[index]["option_A"],
                        option_B=data[index]["option_B"],
                        option_C=data[index]["option_C"],
                        option_D=data[index]["option_D"],
                        option_E=data[index]["option_E"],
                        answer_letter=data[index]["answer_letter"],
                        answer_explanation=data[index]["answer_explanation"]
                    )
                    question.save()

                #Notify all relevant users new questions have been added
                for profile in UserProfile.objects.get_profiles_by_course(course=course):
                    user = profile.user
                    Notification.objects.create(
                        text="We have added new questions to our %s course. Check them out!" % course.name,
                        recipient=user,
                        link=Question.objects.get(index=user.profile.next_question_index, course=course).get_absolute_url()
                    )

                messages.success(request, "JSON file for questions was successfully uploaded. All %s users have been notified." % course)


        return redirect("course_detail", slug=slug)
    return render(request, "course/course_detail.html", context)

def course_list(request):
    '''Returns the view to the course list page.'''

    course_array = Course.objects.all()
    context = {
        "queryset" : course_array
    }
    return render(request, "course/course_list.html", context)

