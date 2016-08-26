'''Views page for the analytics Caprende module.'''

from django.shortcuts import render

from .models import SubCategoryDataSet

# Create your views here.
def dashboard(request):
    '''Returns the view of the dashboard.'''
    subcategory_datasets = SubCategoryDataSet.objects.sort_by_user(request.user)
    context = {
        "subcats" : subcategory_datasets,
        "dashboard" : True,
    }
    return render(request, "analytics/dashboard.html", context)
