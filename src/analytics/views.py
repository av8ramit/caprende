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

def peer_analytics(request):
    '''Returns the view of the peer analytics page.'''

    context = {
        "peer_analytics" : True,
    }
    return render(request, "analytics/peer_analytics.html", context)

def in_depth(request):
    '''Returns the view of the in depth anaytics page regarding your performance among all the subcategories.'''

    context = {
        "in_depth" : True,
    }
    return render(request, "analytics/in_depth.html", context)
