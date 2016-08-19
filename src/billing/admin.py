'''Admin page for the billing Caprende module.'''

from django.contrib import admin

from .models import Membership, Transaction, UserMerchantId

# Register your models here.
admin.site.register(UserMerchantId)
admin.site.register(Membership)
admin.site.register(Transaction)
