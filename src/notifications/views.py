'''Views page for the notifications Caprende module.'''
# pylint: disable=redefined-builtin

import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, Http404, HttpResponseRedirect, redirect, get_object_or_404


from .models import Notification

# Create your views here.

@login_required
def all(request):
    '''Return the view with all the notifications.'''

    notifications = Notification.objects.all_for_user(request.user)
    context = {
        "notifications" : notifications,
    }
    return render(request, "notifications/notifications_all.html", context)


@login_required
def read(request, id):
    '''Returns the one hop function "view" that checks the notification read status as read.'''

    notification = get_object_or_404(Notification, id=id)
    try:
        next = request.GET.get('next', None)
        if notification.recipient == request.user:
            notification.read = True
            notification.save()
            if next is not None:
                return HttpResponseRedirect(next)
            else:
                return redirect("notifications_all")
        else:
            raise Http404
    except:
        raise redirect("notifications_all")


@login_required
def get_notifications_ajax(request):
    '''Return the notifications ajax view for the dropdown icon link.'''

    if request.is_ajax() and request.method == "POST":
        notifications = Notification.objects.all_for_user(request.user).recent()
        count = notifications.count()
        notes = []
        for note in notifications:
            notes.append(str(note.get_link))
        data = {
            "notifications": notes,
            "count": count,
        }
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type='application/json')
    else:
        raise Http404


