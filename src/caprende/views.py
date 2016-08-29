'''Views page for the default Caprende module.'''

from django.shortcuts import redirect, render

from allauth.account.forms import LoginForm

def home(request):
    '''Return the view to the home page.'''
    context = {
        "form" : LoginForm
    }
    if request.user.is_authenticated():
        return redirect("dashboard")
    else:
        return render(request, "home_visitor.html", context)

def about_us(request):
    '''Return the view of the about_us page.'''

    context = {}
    return render(request, "about_us.html", context)
