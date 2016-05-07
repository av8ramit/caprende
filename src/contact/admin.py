'''Admin page for the contact Caprende module.'''

from django.contrib import admin

from .models import ContactRequest

# Register your models here.
class ContactRequestAdmin(admin.ModelAdmin):
    '''Apps page for the contact Caprende module.'''

    list_display = ['timestamp', 'email', '__unicode__']
    class Meta:
        '''Meta class invocation for ContactRequest.'''
        model = ContactRequest

admin.site.register(ContactRequest, ContactRequestAdmin)
