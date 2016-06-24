'''Admin page for the course Caprende module.'''

from django.contrib import admin

from .models import Course, CourseSection

# Register your models here.

class CourseAdmin(admin.ModelAdmin):
    '''Admin interface for Course.'''

    list_display = ["__unicode__"]
    prepopulated_fields = {
        'slug': ["name"],
    }

    class Meta:
        '''Meta class invocation for Course class.'''
        model = Course

admin.site.register(Course, CourseAdmin)
admin.site.register(CourseSection)
