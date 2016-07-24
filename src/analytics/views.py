'''Views page for the analytics Caprende module.'''

from django.shortcuts import render

from .models import CategoryDataSet #, SubCategoryDataSet

# Create your views here.
def dashboard(request):
    '''Returns the view of the dashboard.'''
    category_datasets = CategoryDataSet.objects.sort_by_user(request.user)
    weakest_cats = category_datasets[:3]
    print weakest_cats
    context = {
        "weakest_cats" : weakest_cats,
        "dashboard" : True,
    }
    return render(request, "analytics/dashboard.html", context)
