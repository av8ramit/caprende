'''Views page for the comments Caprende module.'''
# pylint: disable=no-member

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect

from questions.models import Question

from .forms import CommentForm
from .models import Comment

# Create your views here.

@login_required
def comment_thread(request, comment_id):
    '''View a comment thread on it's own page.'''

    comment_parent = Comment.objects.get(comment_id)
    form = CommentForm()
    context = {
        "comment" : comment_parent,
        "form" : form,
    }

    return render(request, "comments/comment_thread.html", context)

def comment_create_view(request):
    '''Method that is called when a user creates or replies to a comment.'''

    if request.method == "POST" and request.user.is_authenticated():
        parent_id = request.POST.get('parent_id')
        question_id = request.POST.get('question_id')

        try:
            question = Question.objects.get(id=question_id)
        except Question.model.DoesNotExist:
            question = None

        if parent_id is not None:
            try:
                parent_comment = Comment.objects.get(id=parent_id)
            except Comment.model.DoesNotExist:
                parent_comment = None
        else:
            parent_comment = None

        form = CommentForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data.get('comment')

            #Reply Comment
            if parent_comment is not None:
                new_comment = Comment.objects.create_comment(
                    user=request.user,
                    text=comment_text,
                    question=question,
                    parent=parent_comment
                    )
                messages.success(request, "Thank you for your response.")
                return HttpResponseRedirect(parent_comment.get_absolute_url())
            #New Comment
            else:
                new_comment = Comment.objects.create_comment(
                    user=request.user,
                    text=comment_text,
                    question=question
                    )
                messages.success(request, "Thank you for your comment.")
                return HttpResponseRedirect(new_comment.get_absolute_url())

        else:
            messages.error(request, "There was an error posting your comment. Please try again.")
            return HttpResponseRedirect(question.get_absolute_url())


