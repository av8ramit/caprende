'''Views page for the analytics Caprende module.'''

from django.shortcuts import render

from .models import CategoryDataSet #, SubCategoryDataSet

# Create your views here.
def dashboard(request):
    '''Returns the view of the dashboard.'''
    category_datasets = CategoryDataSet.objects.sort_by_user(request.user)
    print category_datasets
    context = {
        "category_datasets" : category_datasets,
    }
    return render(request, "analytics/dashboard.html", context)
