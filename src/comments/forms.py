'''Forms page for the comments Caprende module.'''

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class CommentForm(forms.Form):
    '''A form for commenting.'''

    comment = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Your comment/reply.", 'rows': 2})
        )

    def __init__(self, data=None, files=None, **kwargs):
        super(CommentForm, self).__init__(data, files, kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.add_input(Submit('submit', 'Add comment', css_class='btn btn-primary',))
