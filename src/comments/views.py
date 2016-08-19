'''Views page for the comments Caprende module.'''
# pylint: disable=no-member

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect

from notifications.models import Notification
from questions.models import Question

from .forms import CommentForm
from .models import Comment

# Create your views here.

@login_required
def comment_thread(request, comment_id):
    '''View a comment thread on it's own page.'''

    comment_parent = Comment.objects.get(id=comment_id)
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

        if parent_id is not None:
            try:
                parent_comment = Comment.objects.get(id=int(parent_id))
            except Comment.DoesNotExist:
                parent_comment = None
        else:
            parent_comment = None

        try:
            question = Question.objects.get(id=int(question_id))
        except Question.DoesNotExist:
            question = None

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
                #Notification to thread writers
                for user in parent_comment.get_affected_users():
                    #User is the same as commentator
                    if user == request.user:
                        continue
                    else:
                        Notification.objects.create(
                            text=str(request.user) + " has commented on a thread you are following.",
                            recipient=user,
                            link=parent_comment.get_absolute_url()
                        )
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


