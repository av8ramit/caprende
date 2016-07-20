'''Forms page for the course Caprende module.'''
# pylint: disable=no-self-use

from django import forms

from .models import Course


class CourseUploadForm(forms.ModelForm):
    '''A form for the JSON file to populate sections, categories, and subcategories.'''

    class Meta:
        '''Meta class invocation for MyUser.'''
        model = Course
        fields = ('course_json_file',)

class QuestionUploadForm(forms.ModelForm):
    '''A form for the JSON file to populate questions. '''

    class Meta:
        '''Meta class invocation for MyUser.'''
        model = Course
        fields = ('question_json_file',)
