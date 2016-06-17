'''Admin page for the questions Caprende module.'''

from django.contrib import admin

from .models import Question, QuestionResponse

# Register your models here.

admin.site.register(Question)
admin.site.register(QuestionResponse)
