'''Models page for the billing Caprende module.'''
# pylint: disable=no-member, too-many-arguments, bare-except

from __future__ import unicode_literals

import datetime
import random

from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone

# Create your models here.
from .signals import membership_dates_update
from .utils import update_braintree_membership

def user_logged_in_receiver(sender, user, **kwargs):
    '''User logged in receiver that updates status on login.'''
    try:
        update_braintree_membership(user)
    except:
        pass

user_logged_in.connect(user_logged_in_receiver)

class UserMerchantId(models.Model):
    '''Braintree UserMerchant ID module.'''

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    customer_id = models.CharField(max_length=120)
    subscription_id = models.CharField(max_length=120, null=True, blank=True)
    plan_id = models.CharField(max_length=120, null=True, blank=True)
    merchant_name = models.CharField(max_length=120, default="Braintree")

    def __unicode__(self):
        return self.customer_id

class Membership(models.Model):
    '''Membership class for a user.'''

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_ended = models.DateTimeField(default=timezone.now())
    date_start = models.DateTimeField(default=timezone.now())

    def __unicode__(self):
        return str(self.user.username)

    def update_status(self):
        '''Update the is_member boolean value based on the date.'''

        if self.date_ended > timezone.now():
            self.user.is_member = True
            self.user.save()
        else:
            self.user.is_member = False
            self.user.save()

def update_membership_status(sender, instance, created, **kwargs):
    '''Update the membership is_member boolean whenever the profile is saved.'''

    if created:
        pass
    else:
        instance.update_status()

post_save.connect(update_membership_status, sender=Membership)

def update_membership_dates(sender, new_date_start, **kwargs):
    '''Update the member dates for the user.'''

    membership = sender
    current_date_end = membership.date_ended
    #If the current end date is later than the new date start the new end date is current end date + 30 days
    if current_date_end >= new_date_start:
        membership.date_ended = current_date_end + datetime.timedelta(days=30, hours=10)
        membership.save()
    #If the current end date has passed prior to the new date start then the membership goes from the new date to new date + 30 days
    else:
        membership.date_start = new_date_start
        membership.date_ended = new_date_start + datetime.timedelta(days=30, hours=10)
        membership.save()
    membership.update_status()

membership_dates_update.connect(update_membership_dates)


class TransactionManager(models.Manager):
    '''Model manager for the Transaction class.'''

    def create_new(self, user, transaction_id, amount, card_type, \
        success=None, transaction_status=None, last_four=None):
        '''Create a new transaction class from given information for Caprende records.'''

        if not user:
            raise ValueError("Must be a user.")
        if not transaction_id:
            raise ValueError("Must complete a transaction to add new.")

        #Create a randomly generated order id
        new_order_id = "%s%s%s" % (transaction_id[:2], random.randint(1, 129), transaction_id[2:])
        #Create the transaction object
        new_trans = self.model(
            user=user,
            transaction_id=transaction_id,
            order_id=new_order_id,
            amount=amount,
            card_type=card_type
        )
        new_trans.save(using=self._db)
        if success is not None:
            new_trans.success = success
            new_trans.transaction_status = transaction_status
            new_trans.save(using=self._db)
        if last_four is not None:
            new_trans.last_four = last_four
            new_trans.save(using=self._db)
        return new_trans

    def get_recent_for_user(self, user, num):
        '''Get recent transactions for a user.'''
        return super(TransactionManager, self).filter(user=user)[:num]

class Transaction(models.Model):
    '''Transaction model for the billing app for Caprende.'''

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    transaction_id = models.CharField(max_length=120)
    order_id = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    success = models.BooleanField(default=True)
    transaction_status = models.CharField(max_length=220, null=True, blank=True)
    card_type = models.CharField(max_length=120)
    last_four = models.PositiveIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    objects = TransactionManager()

    def __unicode__(self):
        return self.order_id

    class Meta:
        '''Meta class invocation for the Transaction model.'''
        ordering = ['-timestamp']

