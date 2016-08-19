'''Utils page for the billing Caprende module.'''
# pylint: disable=no-member

import datetime
import braintree

from django.conf import settings
from django.utils import timezone

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id=settings.BRAINTREE_MERCHANT_ID,
                                  public_key=settings.BRAINTREE_PUBLIC_KEY,
                                  private_key=settings.BRAINTREE_PRIVATE_KEY)

from .signals import membership_dates_update

def check_membership_status(subscription_id):
    '''Check braintree for membership status and billing date from the API.'''

    sub = braintree.Subscription.find(subscription_id)
    if sub.status == "Active": #braintree.Subscription.Status.Active
        status = True
        next_billing_date = sub.next_billing_date
    else:
        status = False
        next_billing_date = None
    return status, next_billing_date

def update_braintree_membership(user):
    '''Update the braintree membership status. Updated at login.'''

    membership = user.membership
    now = timezone.now()
    subscription_id = user.usermerchantid.subscription_id

    #If the membership has expired and there is a subscription id
    if membership.date_ended <= now and subscription_id is not None:
        status, next_billing_date = check_membership_status(subscription_id)
        datetime_obj = datetime.datetime.combine(next_billing_date, datetime.time(0, 0, 0, 1))
        datetime_aware = timezone.make_aware(datetime_obj, timezone.get_current_timezone())

        #If the status is active add thirty days to the membership
        if status:
            membership_dates_update.send(membership, new_date_start=datetime_aware)
            #update_status called in the signal
        #Update the status of is_member for the user
        else:
            membership.update_status()
    #Update the status of is_member for the user
    elif subscription_id is None:
        membership.update_status()
    #Membership has not expired
    else:
        pass

