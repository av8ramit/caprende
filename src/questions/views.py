'''Views page for the questions Caprende module.'''

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .models import Question

# Create your views here.

@login_required
def question_detail(request, test, question_id):
    '''Return to the view of the question.'''
    question = get_object_or_404(Question, test=test, id=question_id)
    context = {
        "question" : question
    }
    return render(request, "questions/question_detail.html", context)

