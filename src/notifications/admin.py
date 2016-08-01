'''Admin page for the notifications Caprende module.'''

from django.contrib import admin

from .models import Notification

# Register your models here.

admin.site.register(Notification)
