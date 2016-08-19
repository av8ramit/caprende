'''Views page for the billing Caprende module.'''
# pylint: disable=too-many-instance-attributes

import braintree

from django.test import TestCase

from users.models import MyUser

# Create your tests here.

class BillingTests(TestCase):
    '''Tests related to the actual Billing functionality.'''

    def setUp(self):
        '''Set up the billing infrastructure.'''

        #User creation
        self.user = MyUser.objects.create_user(
            username="test",
            email="test@yahoo.com",
            password="password1!",
        )

    def test_user_merchant_id(self):
        '''Testing to see if the user was automatically created.'''
        self.assertTrue(self.user.usermerchantid != None)

    def tearDown(self):
        '''Tear down the infrastructure.'''
        braintree.Customer.delete(self.user.usermerchantid.customer_id)
