'''Forms page for the users Caprende module.'''
# pylint: disable=no-self-use

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import MyUser, UserProfile

class UserCreationForm(forms.ModelForm):
    '''A form for creating new users. Includes all the required fields, plus a repeated password.'''
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        '''Meta class invocation for MyUser.'''
        model = MyUser
        fields = ('email', 'username')

    def clean_password2(self):
        '''Check that the two password entries match.'''
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def signup(self, request, user):
        '''Signup method called by allauth.'''
        user.save()


class UserChangeForm(forms.ModelForm):
    '''A form for updating users. Includes all the fields on the user, but replaces
    the password field with admin's password hash display field.'''
    password = ReadOnlyPasswordHashField()

    class Meta:
        '''Meta class invocation for MyUser.'''
        model = MyUser
        fields = ('email', 'password', 'username', 'is_active', 'is_admin', "is_member")

    def clean_password(self):
        '''Regardless of what the user provides, return the initial value. This is done here, rather
        than on the field, because the field does not have access to the initial value.'''
        return self.initial["password"]


class EditProfileForm(forms.ModelForm):
    '''A form for updating the user profile for a user.'''

    class Meta:
        '''Meta class invocation for UserProfile.'''
        model = UserProfile
        fields = ('first_name', 'last_name', 'profile_image', 'course', 'motivational_image', 'university', 'major', 'state')

class UserCategoryEnableForm(forms.Form):
    '''A form for a user to update the questions enabled.'''
    choices = forms.MultipleChoiceField(choices=(), widget=forms.CheckboxSelectMultiple())

    def __init__(self, *args, **kwargs):
        categories = kwargs.pop('categories', None)
        super(UserCategoryEnableForm, self).__init__(*args, **kwargs)
        self.fields['choices'].choices = categories


