'''Views page for the default Caprende module.'''

from django.shortcuts import redirect, render

def home(request):
    '''Return the view to the home page.'''
    context = {}
    if request.user.is_authenticated():
        return redirect("dashboard")
    else:
        return render(request, "home_visitor.html", context)
