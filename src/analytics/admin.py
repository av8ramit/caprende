'''Admin page for the analytics Caprende module.'''

from django.contrib import admin

from .models import CategoryDataSet, SubCategoryDataSet

# Register your models here.

admin.site.register(CategoryDataSet)
admin.site.register(SubCategoryDataSet)
