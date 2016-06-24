'''Admin page for the questions Caprende module.'''

from django.contrib import admin

from .models import Question, QuestionResponse

# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    '''Admin interface for Question.'''

    list_display = ["__unicode__", 'course']
    exclude = ['index']

    class Meta:
        '''Meta class invocation for Question class.'''
        model = Question

admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionResponse)
