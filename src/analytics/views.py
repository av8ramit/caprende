'''Views page for the analytics Caprende module.'''

from django.shortcuts import render

from .models import CategoryDataSet, SubCategoryDataSet

#ToDo: Put @login_required decorator

# Create your views here.
def dashboard(request):
    '''Returns the view of the dashboard.'''
    subcategory_datasets = SubCategoryDataSet.objects.sort_by_user(request.user)
    context = {
        "subcats" : subcategory_datasets[:4],
        "dashboard" : True,
    }
    return render(request, "analytics/dashboard.html", context)

def peer_analytics(request):
    '''Returns the view of the peer analytics page.'''

    #Weakest category by state
    categories = request.user.profile.course.get_all_categories()
    weakest_category_by_state = None
    weakest_category_strength_by_state = 100000 #Ridiculously large number

    for category in categories:
        correct, total = CategoryDataSet.objects.stats_by_state(category=category, state=request.user.profile.state)
        if total == 0 or total == correct:
            continue
        category_strength = float(correct) / total / (total - correct)

        if category_strength <= weakest_category_strength_by_state:
            weakest_category_by_state = category
            weakest_category_strength_by_state = category_strength

    #Weakest category by major
    weakest_category_by_major = None
    weakest_category_strength_by_major = 100000

    for category in categories:
        correct, total = CategoryDataSet.objects.stats_by_major(category=category, major=request.user.profile.major)
        if total == 0 or total == correct:
            continue
        category_strength = float(correct) / total / (total - correct)

        if category_strength <= weakest_category_strength_by_major:
            weakest_category_by_major = category
            weakest_category_strength_by_major = category_strength

    #Weakest category by university
    weakest_category_by_university = None
    weakest_category_strength_by_university = 100000

    for category in categories:
        correct, total = CategoryDataSet.objects.stats_by_university(category=category, university=request.user.profile.university)
        if total == 0 or total == correct:
            continue
        category_strength = float(correct) / total / (total - correct)

        if category_strength <= weakest_category_strength_by_university:
            weakest_category_by_university = category
            weakest_category_strength_by_university = category_strength


    context = {
        "peer_analytics" : True,
        "weakest_category_by_university" : weakest_category_by_university,
        "weakest_category_by_major" : weakest_category_by_major,
        "weakest_category_by_state" : weakest_category_by_state
    }
    return render(request, "analytics/peer_analytics.html", context)

def in_depth(request):
    '''Returns the view of the in depth anaytics page regarding your performance among all the subcategories.'''

    context = {
        "in_depth" : True,
    }
    return render(request, "analytics/in_depth.html", context)
