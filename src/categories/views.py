'''Views page for the categories Caprende module.'''

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Category, SubCategory

# Create your views here.

@login_required
def category_detail(request, slug):
    '''Returns the view of a category in detail.'''

    category = Category.objects.get(slug=slug)
    context = {
        "category" : category,
    }
    return render(request, "categories/category_detail.html", context)

@login_required
def subcategory_detail(request, slug):
    '''Returns the view of a subcategory in detail.'''

    subcategory = SubCategory.objects.get(slug=slug)
    context = {
        "subcategory" : subcategory,
    }
    return render(request, "categories/subcategory_detail.html", context)
