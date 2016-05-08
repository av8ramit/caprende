'''Views page for the users Caprende module.'''

from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import EditProfileForm

# Create your views here.
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
    })
    if form.is_valid():
        profile.update(
            first_name=form.cleaned_data.get("first_name"),
            last_name=form.cleaned_data.get("last_name"),
            profile_image=form.cleaned_data.get("profile_image"),
            course=form.cleaned_data.get("course"),
            motivational_image=form.cleaned_data.get("motivational_image"),
            university=form.cleaned_data.get("university"),
            major=form.cleaned_data.get("major")
        )
        messages.success(request, "Your profile has been updated.")
        return redirect("edit_profile")
    return render(request, "users/edit_profile.html", {'form':form})
