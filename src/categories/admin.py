'''Admin page for the categories Caprende module.'''

from django.contrib import admin

from .models import Category, SubCategory

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    '''Admin interface for Category.'''

    list_display = ["__unicode__", "course"]

    class Meta:
        '''Meta class invocation for Category class.'''
        model = Category

class SubCategoryAdmin(admin.ModelAdmin):
    '''Admin interface for SubCategory'''

    list_display = ["__unicode__", "course"]

    class Meta:
        '''Meta class invocation for SubCategory class.'''
        model = SubCategory

admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
