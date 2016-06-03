'''Forms page for the questions Caprende module.'''

from django import forms

class QuestionResponseForm(forms.Form):
    '''A form for answering practice questions.'''
    answer = forms.CharField(max_length=1)
