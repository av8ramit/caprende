'''Views page for the course Caprende module.'''

from django.shortcuts import render

from .models import Course

# Create your views here.

def course_detail(request, slug):
    '''Returns the view to the course page.'''

    course = Course.objects.get(slug=slug)
    context = {
        "course" : course,
    }
    return render(request, "course/course_detail.html", context)

def course_list(request):
    '''Returns the view to the course list page.'''

    course_array = Course.objects.all()
    context = {
        "queryset" : course_array
    }
    return render(request, "course/course_list.html", context)
