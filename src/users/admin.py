'''Admin page for the users Caprende module.'''

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from .models import MyUser, UserProfile, UserCategoryEnable
from .forms import UserChangeForm, UserCreationForm

class MyUserAdmin(UserAdmin):
    '''Apps page for the users Caprende module.'''

    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'username', 'is_admin', 'is_member')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_member')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin, MyUser, and UserProfile.
admin.site.register(MyUser, MyUserAdmin)
admin.site.register(UserProfile)
admin.site.register(UserCategoryEnable)
# Now unregister the Group model from admin.
admin.site.unregister(Group)
