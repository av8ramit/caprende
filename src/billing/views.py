'''Views page for the billing Caprende module.'''
# pylint: disable=no-member, bare-except, too-many-return-statements, too-many-statements

import braintree

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import  Membership, Transaction, UserMerchantId
from .signals import membership_dates_update


braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id=settings.BRAINTREE_MERCHANT_ID,
                                  public_key=settings.BRAINTREE_PUBLIC_KEY,
                                  private_key=settings.BRAINTREE_PRIVATE_KEY)

# Create your views here.

PLAN_ID = "monthly_plan" #Set by the admin before deployment

def get_or_create_model_transaction(user, braintree_transaction):
    '''Create a transaction from a braintree transaction.'''

    trans_id = braintree_transaction.id
    try:
        Transaction.objects.get(user=user, transaction_id=trans_id)
        created = False
    except Transaction.DoesNotExist:
        created = True
        payment_type = braintree_transaction.payment_instrument_type
        amount = braintree_transaction.amount
        #Paypal transaction
        if payment_type == braintree.PaymentInstrumentType.PayPalAccount:
            trans = Transaction.objects.create_new(user, trans_id, amount, "PayPal")
        #Credit Card transaction
        elif payment_type == braintree.PaymentInstrumentType.CreditCard:
            credit_card_details = braintree_transaction.credit_card_details
            card_type = credit_card_details.card_type
            last_4 = credit_card_details.last_4
            trans = Transaction.objects.create_new(user, trans_id, amount, card_type, last_four=last_4)
        #Do not create the transaction as that payment type is not supported
        else:
            created = False
            trans = None
    return trans, created

def update_transactions(user):
    '''Update transactions for a given user.'''

    bt_transactions = braintree.Transaction.search(
        braintree.TransactionSearch.customer_id == user.usermerchantid.customer_id
    )
    try:
        django_transactions = user.transaction_set.all()
    except:
        django_transactions = None
    if bt_transactions is not None and django_transactions is not None:
        if bt_transactions.maximum_size <= django_transactions.count():
            pass
        #Update the local transactions with the braintree ones
        else:
            for bt_tran in bt_transactions.items:
                get_or_create_model_transaction(user, bt_tran)

@login_required
def history(request):
    '''Return a list of all true transactions for a user.'''

    update_transactions(request.user)
    transaction_set = Transaction.objects.filter(user=request.user).filter(success=True)
    return render(request, "billing/history.html", {"queryset": transaction_set})

@login_required
def upgrade(request):
    '''Upgrade the membership of a user.'''

    if request.user.is_authenticated():

        #Retrieve merchant object for user
        try:
            merchant_obj = UserMerchantId.objects.get(user=request.user)
        except:
            messages.error(request, "There was an error with your account. Please contact us.")
            return redirect("contact_us")

        merchant_customer_id = merchant_obj.customer_id
        client_token = braintree.ClientToken.generate({
            "customer_id": merchant_customer_id
        })

        if request.method == "POST":
            nonce = request.POST.get("payment_method_nonce", None)
            if nonce is None:
                messages.error(request, "Unable to get authentication with braintree, please try again later.")
                return redirect("upgrade")
            else:
                #Run the braintree create method with this payment information
                payment_method_result = braintree.PaymentMethod.create({
                    "customer_id": merchant_customer_id,
                    "payment_method_nonce": nonce,
                    "options": {
                        "make_default": True
                    }
                })

                #If the payment transaction was successful
                if not payment_method_result.is_success:
                    messages.error(request, "An error occured while processing your payment: %s" % payment_method_result.message)
                    return redirect("upgrade")

                the_token = payment_method_result.payment_method.token
                current_sub_id = merchant_obj.subscription_id
                did_create_sub = False
                did_update_sub = False
                trans_timestamp = None

                #Find the subscription if it exists
                try:
                    current_subscription = braintree.Subscription.find(current_sub_id)
                    sub_status = current_subscription.status
                except:
                    current_subscription = None
                    sub_status = None

                #If the subscription is active, update the payment method
                if current_subscription and sub_status == "Active":
                    braintree.Subscription.update(current_sub_id, {
                        "payment_method_token": the_token,
                    })
                    did_update_sub = True
                #If the subscription doesn't exist or isn't active, create it
                else:
                    create_sub = braintree.Subscription.create({
                        "payment_method_token": the_token,
                        "plan_id": PLAN_ID
                    })
                    did_create_sub = True

                #If the subscription was created, create a membership object
                if did_create_sub or did_update_sub:
                    membership_instance, created = Membership.objects.get_or_create(user=request.user)

                #If the subscription was updated, update the dates
                if did_update_sub and not did_create_sub:
                    messages.success(request, "Your plan has been updated")
                    membership_dates_update.send(membership_instance, new_date_start=timezone.now())
                    return redirect("billing_history")
                #If the subscription was created, update the dates and create a transaction
                elif did_create_sub and not did_update_sub:
                    #Update the merchant_obj attributes
                    merchant_obj.subscription_id = create_sub.subscription.id
                    merchant_obj.plan_id = PLAN_ID
                    merchant_obj.save()

                    bt_tran = create_sub.subscription.transactions[0]
                    new_tran, created = get_or_create_model_transaction(request.user, bt_tran)
                    trans_timestamp = None
                    if created:
                        trans_timestamp = new_tran.timestamp
                    membership_dates_update.send(membership_instance, new_date_start=trans_timestamp)

                    messages.success(request, "Thank your for signing up with Caprende. Welcome!")
                    return redirect("billing_history")
                else:
                    messages.error(request, "An error occurred, please try again later.")
                    return redirect("upgrade")

        #Provide the HTML file with the client_token
        context = {"client_token" : client_token}

        return render(request, "billing/upgrade.html", context)

@login_required
def cancel_subscription(request):
    '''Cancel the subscription of a user.'''

    sub_id = request.user.usermerchantid.subscription_id
    if sub_id is not None:
        result = braintree.Subscription.cancel(sub_id)
        if result.is_success:
            request.user.usermerchantid.subscription_id = None
            request.user.usermerchantid.save()
            messages.success(request, "Youre account has been successfully cancelled.")
        else:
            messages.error(request, "There was an error with your account. Please contact us for further instruction.")
            return redirect("contact_us")
    else:
        messages.error(request, "You do not have an active account.")
    return redirect("billing_history")
