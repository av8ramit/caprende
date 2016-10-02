'''Views page for the users Caprende module.'''

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from billing.models import Transaction
from notifications.models import Notification

from .models import UserCategoryEnable
from .forms import EditProfileForm, UserCategoryEnableForm

# Create your views here.
@login_required
def user_account(request):
    '''Return the view to the user account page.'''
    notifications = Notification.objects.get_recent_for_user(request.user, 6)
    transactions = Transaction.objects.get_recent_for_user(request.user, 3)
    context = {
        "notifications": notifications,
        "transactions": transactions
    }

    return render(request, "users/user_account.html", context)

def edit_profile(request):
    '''Return the view to the edit profile page.'''


    profile = request.user.profile
    form = EditProfileForm(request.POST or None, request.FILES or None, initial={
        "first_name" : profile.first_name,
        "last_name" : profile.last_name,
        "profile_image" : profile.profile_image,
        "course" : profile.course,
        "motivational_image" : profile.motivational_image,
        "university" : profile.university,
        "major" : profile.major,
        "state" : profile.state,
    })
    if form.is_valid():
        profile.update(
            first_name=form.cleaned_data.get("first_name"),
            last_name=form.cleaned_data.get("last_name"),
            profile_image=form.cleaned_data.get("profile_image"),
            course=form.cleaned_data.get("course"),
            motivational_image=form.cleaned_data.get("motivational_image"),
            university=form.cleaned_data.get("university"),
            major=form.cleaned_data.get("major"),
            state=form.cleaned_data.get("state")
        )
        messages.success(request, "Your profile has been updated.")
        return redirect("edit_profile")
    return render(request, "users/edit_profile.html", {'form':form})


def category_filter(request):
    '''Filter the categories that a user wants to answer questions for.'''

    categoryenables = UserCategoryEnable.objects.all().by_profile(request.user.profile)

    zip_cat = []
    initial = []
    for cat in categoryenables:
        zip_cat.append(cat.category.name + " (" + cat.category.section.name + ")")
        if cat.enabled:
            initial.append(cat)
    form = UserCategoryEnableForm(request.POST or None, categories=zip(categoryenables, zip_cat), initial={"choices" : initial})
    if form.is_valid():
        #Update Logic
        for category_enable in categoryenables:
            if unicode(category_enable) in form.cleaned_data.get("choices"):
                category_enable.enable()
            else:
                category_enable.disable()
        return redirect("category_filter")

    context = {
        'form' : form,
        "cat_filt" : True,
    }
    return render(request, "users/category_filter.html", context)



