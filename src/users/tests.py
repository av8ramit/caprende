'''Tests page for the users Caprende module.'''
# pylint: disable=no-self-use, no-member

from __future__ import absolute_import

import json
import uuid
from datetime import timedelta

import braintree

from django.conf import settings
from django.contrib.auth.models import AnonymousUser, AbstractUser
from django.core import mail
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.timezone import now
from django.test.utils import override_settings
from django.test.client import Client, RequestFactory
from django.test import TestCase

from allauth.account import app_settings
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress, EmailConfirmation
from allauth.account.auth_backends import AuthenticationBackend
from allauth.utils import get_user_model, get_current_site
from allauth.account.utils import user_pk_to_url_str

from course.models import Course

from .models import MyUser, UserProfile


braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id=settings.BRAINTREE_MERCHANT_ID,
                                  public_key=settings.BRAINTREE_PUBLIC_KEY,
                                  private_key=settings.BRAINTREE_PRIVATE_KEY)

@override_settings(
    ACCOUNT_DEFAULT_HTTP_PROTOCOL='https',
    ACCOUNT_EMAIL_VERIFICATION=app_settings.EmailVerificationMethod.MANDATORY,
    ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.USERNAME,
    ACCOUNT_SIGNUP_FORM_CLASS=None,
    ACCOUNT_EMAIL_SUBJECT_PREFIX=None,
    LOGIN_REDIRECT_URL='/accounts/profile/',
    ACCOUNT_ADAPTER='allauth.account.adapter.DefaultAccountAdapter',
    ACCOUNT_USERNAME_REQUIRED=True)
class AccountTests(TestCase):
    '''Tests related to the actual Account functionality.'''

    def test_username_containing_at(self):
        '''Testing a username containing @.'''

        user = get_user_model().objects.create(username='@raymond.penners')
        user.set_password('psst')
        user.save()
        braintree.Customer.delete(user.usermerchantid.customer_id)
        EmailAddress.objects.create(user=user,
                                    email='raymond.penners@gmail.com',
                                    primary=True,
                                    verified=True)
        resp = self.client.post(reverse('account_login'),
                                {'login': '@raymond.penners',
                                 'password': 'psst'})
        self.assertRedirects(resp,
                             'http://testserver' + settings.LOGIN_REDIRECT_URL,
                             fetch_redirect_response=False)

    def test_signup_same_email_verified_externally(self):
        '''Testing signup of the same email verified externally.'''

        user = self._test_signup_email_verified_externally('john@doe.com',
                                                           'john@doe.com')
        self.assertEqual(EmailAddress.objects.filter(user=user).count(),
                         1)
        EmailAddress.objects.get(verified=True,
                                 email='john@doe.com',
                                 user=user,
                                 primary=True)

    def test_signup_other_email_verified_externally(self):
        '''
        John is invited on john@work.com, but signs up via john@home.com.
        E-mail verification is by-passed, their home e-mail address is
        used as a secondary.
        '''

        user = self._test_signup_email_verified_externally('john@home.com',
                                                           'john@work.com')
        self.assertEqual(EmailAddress.objects.filter(user=user).count(),
                         2)
        EmailAddress.objects.get(verified=False,
                                 email='john@home.com',
                                 user=user,
                                 primary=False)
        EmailAddress.objects.get(verified=True,
                                 email='john@work.com',
                                 user=user,
                                 primary=True)

    def _test_signup_email_verified_externally(self, signup_email, verified_email):
        username = 'johndoe'
        request = RequestFactory().post(reverse('account_signup'),
                                        {'username': username,
                                         'email': signup_email,
                                         'password1': 'johndoe',
                                         'password2': 'johndoe'})
        # Fake stash_verified_email
        from django.contrib.messages.middleware import MessageMiddleware
        from django.contrib.sessions.middleware import SessionMiddleware
        SessionMiddleware().process_request(request)
        MessageMiddleware().process_request(request)
        request.user = AnonymousUser()
        request.session['account_verified_email'] = verified_email
        from allauth.account.views import signup
        resp = signup(request)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['location'],
                         get_adapter().get_login_redirect_url(request))
        self.assertEqual(len(mail.outbox), 0)
        user = get_user_model().objects.get(username=username)
        braintree.Customer.delete(user.usermerchantid.customer_id)
        return user

    def _create_user(self):
        user = get_user_model().objects.create(username='john', is_active=True)
        user.set_password('doe')
        user.save()
        braintree.Customer.delete(user.usermerchantid.customer_id)
        return user

    def _create_user_and_login(self):
        user = self._create_user()
        self.client.login(username='john', password='doe')
        return user

    def test_redirect_when_authenticated(self):
        '''Test redirect when authenticated.'''

        self._create_user_and_login()
        c = self.client
        resp = c.get(reverse('account_login'))
        self.assertRedirects(resp, 'http://testserver/accounts/profile/',
                             fetch_redirect_response=False)

    def test_password_reset_get(self):
        '''Test password reset.'''

        resp = self.client.get(reverse('account_reset_password'))
        self.assertTemplateUsed(resp, 'account/password_reset.html')

    def test_password_set_redirect(self):
        '''Test password set redirect.'''

        resp = self._password_set_or_reset_redirect('account_set_password',
                                                    True)
        self.assertEqual(resp.status_code, 302)

    def test_password_reset_no_redirect(self):
        '''Test password reset no redirect.'''

        resp = self._password_set_or_reset_redirect('account_change_password',
                                                    True)
        self.assertEqual(resp.status_code, 200)

    def test_password_reset_redirect(self):
        '''Test password reset redirect.'''

        resp = self._password_set_or_reset_redirect('account_change_password',
                                                    False)
        self.assertEqual(resp.status_code, 302)

    def _password_set_or_reset_redirect(self, urlname, usable_password):
        user = self._create_user_and_login()
        c = self.client
        if not usable_password:
            user.set_unusable_password()
            user.save()
        resp = c.get(reverse(urlname))
        return resp

    def _request_new_password(self):
        user = get_user_model().objects.create(
            username='john', email='john@doe.org', is_active=True)
        user.set_password('doe')
        user.save()
        braintree.Customer.delete(user.usermerchantid.customer_id)
        self.client.post(
            reverse('account_reset_password'),
            data={'email': 'john@doe.org'})
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['john@doe.org'])
        return user

    @override_settings(ACCOUNT_EMAIL_CONFIRMATION_HMAC=False)
    def test_email_verification_mandatory(self):
        '''Test email verification when it's mandatory.'''

        c = Client()
        # Signup
        resp = c.post(reverse('account_signup'),
                      {'username': 'johndoe',
                       'email': 'john@doe.com',
                       'password1': 'johndoe',
                       'password2': 'johndoe'},
                      follow=True)
        user = get_user_model().objects.filter(
            username='johndoe', is_active=True)[0]
        braintree.Customer.delete(user.usermerchantid.customer_id)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(mail.outbox[0].to, ['john@doe.com'])
        self.assertGreater(mail.outbox[0].body.find('https://'), 0)
        self.assertEqual(len(mail.outbox), 1)
        self.assertTemplateUsed(
            resp,
            'account/verification_sent.%s' % app_settings.TEMPLATE_EXTENSION)
        # Attempt to login, unverified
        for attempt in [1, 2]:
            resp = c.post(reverse('account_login'),
                          {'login': 'johndoe',
                           'password': 'johndoe'},
                          follow=True)
            # is_active is controlled by the admin to manually disable
            # users. I don't want this flag to flip automatically whenever
            # users verify their email adresses.
            self.assertTrue(get_user_model().objects.filter(
                username='johndoe', is_active=True).exists())

            self.assertTemplateUsed(
                resp,
                'account/verification_sent.' + app_settings.TEMPLATE_EXTENSION)
            # Attempt 1: no mail is sent due to cool-down ,
            # but there was already a mail in the outbox.
            self.assertEqual(len(mail.outbox), attempt)
            self.assertEqual(
                EmailConfirmation.objects.filter(
                    email_address__email='john@doe.com').count(),
                attempt)
            # Wait for cooldown
            EmailConfirmation.objects.update(sent=now() - timedelta(days=1))
        # Verify, and re-attempt to login.
        confirmation = EmailConfirmation \
            .objects \
            .filter(email_address__user__username='johndoe')[:1] \
            .get()
        resp = c.get(reverse('account_confirm_email',
                             args=[confirmation.key]))
        self.assertTemplateUsed(
            resp,
            'account/email_confirm.%s' % app_settings.TEMPLATE_EXTENSION)
        c.post(reverse('account_confirm_email',
                       args=[confirmation.key]))
        resp = c.post(reverse('account_login'),
                      {'login': 'johndoe',
                       'password': 'johndoe'})
        self.assertRedirects(resp,
                             'http://testserver'+settings.LOGIN_REDIRECT_URL,
                             fetch_redirect_response=False)

    def test_email_escaping(self):
        '''Test email escaping.'''

        site = get_current_site()
        site.name = '<enc&"test>'
        site.save()
        u = get_user_model().objects.create(
            username='test',
            email='foo@bar.com')
        braintree.Customer.delete(u.usermerchantid.customer_id)
        request = RequestFactory().get('/')
        EmailAddress.objects.add_email(request, u, u.email, confirm=True)
        self.assertTrue(mail.outbox[0].subject[1:].startswith(site.name))

    @override_settings(
        ACCOUNT_EMAIL_VERIFICATION=app_settings.EmailVerificationMethod
        .OPTIONAL)
    def test_login_unverified_account_optional(self):
        '''Tests login behavior when email verification is optional.'''

        user = get_user_model().objects.create(username='john')
        user.set_password('doe')
        user.save()
        braintree.Customer.delete(user.usermerchantid.customer_id)
        EmailAddress.objects.create(user=user,
                                    email='john@example.com',
                                    primary=True,
                                    verified=False)
        resp = self.client.post(reverse('account_login'),
                                {'login': 'john',
                                 'password': 'doe'})
        self.assertRedirects(resp,
                             'http://testserver'+settings.LOGIN_REDIRECT_URL,
                             fetch_redirect_response=False)

    @override_settings(
        ACCOUNT_EMAIL_VERIFICATION=app_settings.EmailVerificationMethod
        .OPTIONAL,
        ACCOUNT_LOGIN_ATTEMPTS_LIMIT=3)
    def test_login_failed_attempts_exceeded(self):
        '''Test login failed attempts exceeded.'''

        user = get_user_model().objects.create(username='john')
        user.set_password('doe')
        user.save()
        braintree.Customer.delete(user.usermerchantid.customer_id)
        EmailAddress.objects.create(user=user,
                                    email='john@example.com',
                                    primary=True,
                                    verified=False)
        for i in range(5):
            is_valid_attempt = (i == 4)
            is_locked = (i >= 3)
            resp = self.client.post(
                reverse('account_login'),
                {'login': 'john',
                 'password': (
                     'doe' if is_valid_attempt
                     else 'wrong')})
            self.assertFormError(
                resp,
                'form',
                None,
                'Too many failed login attempts. Try again later.'
                if is_locked
                else
                'The username and/or password you specified are not correct.')

    def test_login_unverified_account_mandatory(self):
        '''Tests login behavior when email verification is mandatory.'''

        user = get_user_model().objects.create(username='john')
        user.set_password('doe')
        user.save()
        braintree.Customer.delete(user.usermerchantid.customer_id)
        EmailAddress.objects.create(user=user,
                                    email='john@example.com',
                                    primary=True,
                                    verified=False)
        resp = self.client.post(reverse('account_login'),
                                {'login': 'john',
                                 'password': 'doe'})
        self.assertRedirects(resp, reverse('account_email_verification_sent'))


    def test_ajax_password_reset(self):
        '''Test ajax password reset.'''

        user = get_user_model().objects.create(
            username='john', email='john@doe.org', is_active=True)
        user.save()
        braintree.Customer.delete(user.usermerchantid.customer_id)
        resp = self.client.post(
            reverse('account_reset_password'),
            data={'email': 'john@doe.org'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['john@doe.org'])
        self.assertEqual(resp['content-type'], 'application/json')

    @override_settings(
        ACCOUNT_EMAIL_VERIFICATION=app_settings.EmailVerificationMethod
        .OPTIONAL)
    def test_ajax_login_success(self):
        '''Test ajax login success.'''

        user = get_user_model().objects.create(username='john', is_active=True)
        user.set_password('doe')
        user.save()
        braintree.Customer.delete(user.usermerchantid.customer_id)
        resp = self.client.post(reverse('account_login'),
                                {'login': 'john',
                                 'password': 'doe'},
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content.decode('utf8'))
        self.assertEqual(data['location'], '/accounts/profile/')

    @override_settings(ACCOUNT_LOGOUT_ON_GET=False)
    def test_logout_view_on_post(self):
        '''Test logout view on post.'''

        c, resp = self._logout_view('get')
        self.assertTemplateUsed(
            resp,
            'account/logout.%s' % app_settings.TEMPLATE_EXTENSION)
        resp = c.post(reverse('account_logout'))
        self.assertTemplateUsed(resp, 'account/messages/logged_out.txt')

    def _logout_view(self, method):
        c = Client()
        user = get_user_model().objects.create(username='john', is_active=True)
        user.set_password('doe')
        user.save()
        braintree.Customer.delete(user.usermerchantid.customer_id)
        c = Client()
        c.login(username='john', password='doe')
        return c, getattr(c, method)(reverse('account_logout'))

    @override_settings(ACCOUNT_EMAIL_VERIFICATION=app_settings
                       .EmailVerificationMethod.OPTIONAL)
    def test_optional_email_verification(self):
        '''Test optional email verification.'''

        c = Client()
        # Signup
        c.get(reverse('account_signup'))
        resp = c.post(reverse('account_signup'),
                      {'username': 'johndoe',
                       'email': 'john@doe.com',
                       'password1': 'johndoe',
                       'password2': 'johndoe'})
        user = get_user_model().objects.filter(
            username='johndoe', is_active=True)[0]
        braintree.Customer.delete(user.usermerchantid.customer_id)
        # Logged in
        self.assertRedirects(resp,
                             settings.LOGIN_REDIRECT_URL,
                             fetch_redirect_response=False)
        self.assertEqual(mail.outbox[0].to, ['john@doe.com'])
        self.assertEqual(len(mail.outbox), 1)
        # Logout & login again
        c.logout()
        # Wait for cooldown
        EmailConfirmation.objects.update(sent=now() - timedelta(days=1))
        # Signup
        resp = c.post(reverse('account_login'),
                      {'login': 'johndoe',
                       'password': 'johndoe'})
        self.assertRedirects(resp,
                             settings.LOGIN_REDIRECT_URL,
                             fetch_redirect_response=False)
        self.assertEqual(mail.outbox[0].to, ['john@doe.com'])
        # There was an issue that we sent out email confirmation mails
        # on each login in case of optional verification. Make sure
        # this is not the case:
        self.assertEqual(len(mail.outbox), 1)

    @override_settings(ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS=False)
    def test_account_authenticated_login_redirects_is_false(self):
        '''Test account authenticated login redirects.'''

        self._create_user_and_login()
        resp = self.client.get(reverse('account_login'))
        self.assertEqual(resp.status_code, 200)

    @override_settings(ACCOUNT_EMAIL_CONFIRMATION_HMAC=True)
    def test_email_confirmation_hmac_falls_back(self):
        '''Test email confirmation hmac falls back.'''

        user = self._create_user()
        email = EmailAddress.objects.create(
            user=user,
            email='a@b.com',
            verified=False,
            primary=True)
        confirmation = EmailConfirmation.create(email)
        confirmation.sent = now()
        confirmation.save()
        self.client.post(
            reverse('account_confirm_email',
                    args=[confirmation.key]))
        email = EmailAddress.objects.get(pk=email.pk)
        self.assertTrue(email.verified)


class EmailFormTests(TestCase):
    '''Tests related to the actual EmailForm functionality.'''

    def setUp(self):
        '''Set up method for the tests. Instantiate the user.'''
        User = get_user_model()
        self.user = User.objects.create(username='john',
                                        email='john1@doe.org')
        self.user.set_password('doe')
        self.user.save()
        braintree.Customer.delete(self.user.usermerchantid.customer_id)
        self.email_address = EmailAddress.objects.create(
            user=self.user,
            email=self.user.email,
            verified=True,
            primary=True)
        self.email_address2 = EmailAddress.objects.create(
            user=self.user,
            email='john2@doe.org',
            verified=False,
            primary=False)
        self.client.login(username='john', password='doe')

    def test_add(self):
        '''Test adding an email.'''

        resp = self.client.post(
            reverse('account_email'),
            {'action_add': '',
             'email': 'john3@doe.org'})
        EmailAddress.objects.get(
            email='john3@doe.org',
            user=self.user,
            verified=False,
            primary=False)
        self.assertTemplateUsed(resp,
                                'account/messages/email_confirmation_sent.txt')

    def test_ajax_add(self):
        '''Test ajax adding an email.'''

        resp = self.client.post(
            reverse('account_email'),
            {'action_add': '',
             'email': 'john3@doe.org'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data = json.loads(resp.content.decode('utf8'))
        self.assertEqual(data['location'],
                         reverse('account_email'))

    def test_ajax_add_invalid(self):
        '''Test ajax adding invalid email.'''

        resp = self.client.post(
            reverse('account_email'),
            {'action_add': '',
             'email': 'john3#doe.org'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data = json.loads(resp.content.decode('utf8'))
        self.assertTrue('form_errors' in data)
        self.assertTrue('email' in data['form_errors'])

    def test_remove_primary(self):
        '''Test removing primary email.'''

        resp = self.client.post(
            reverse('account_email'),
            {'action_remove': '',
             'email': self.email_address.email})
        EmailAddress.objects.get(pk=self.email_address.pk)
        self.assertTemplateUsed(
            resp,
            'account/messages/cannot_delete_primary_email.txt')

    def test_ajax_remove_primary(self):
        '''Test removing primary email via ajax.'''

        resp = self.client.post(
            reverse('account_email'),
            {'action_remove': '',
             'email': self.email_address.email},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTemplateUsed(
            resp,
            'account/messages/cannot_delete_primary_email.txt')
        data = json.loads(resp.content.decode('utf8'))
        self.assertEqual(data['location'],
                         reverse('account_email'))

    def test_remove_secondary(self):
        '''Test removing secondary email.'''

        resp = self.client.post(
            reverse('account_email'),
            {'action_remove': '',
             'email': self.email_address2.email})
        self.assertRaises(EmailAddress.DoesNotExist,
                          lambda: EmailAddress.objects.get(
                              pk=self.email_address2.pk))
        self.assertTemplateUsed(
            resp,
            'account/messages/email_deleted.txt')

    def test_set_primary_unverified(self):
        '''Test set primary unverified email.'''

        resp = self.client.post(
            reverse('account_email'),
            {'action_primary': '',
             'email': self.email_address2.email})
        email_address = EmailAddress.objects.get(pk=self.email_address.pk)
        email_address2 = EmailAddress.objects.get(pk=self.email_address2.pk)
        self.assertFalse(email_address2.primary)
        self.assertTrue(email_address.primary)
        self.assertTemplateUsed(
            resp,
            'account/messages/unverified_primary_email.txt')

    def test_set_primary(self):
        '''Test set primary email.'''

        email_address2 = EmailAddress.objects.get(pk=self.email_address2.pk)
        email_address2.verified = True
        email_address2.save()
        resp = self.client.post(
            reverse('account_email'),
            {'action_primary': '',
             'email': self.email_address2.email})
        email_address = EmailAddress.objects.get(pk=self.email_address.pk)
        email_address2 = EmailAddress.objects.get(pk=self.email_address2.pk)
        self.assertFalse(email_address.primary)
        self.assertTrue(email_address2.primary)
        self.assertTemplateUsed(
            resp,
            'account/messages/primary_email_set.txt')

    def test_verify(self):
        '''Test verify email.'''

        resp = self.client.post(
            reverse('account_email'),
            {'action_send': '',
             'email': self.email_address2.email})
        self.assertTemplateUsed(
            resp,
            'account/messages/email_confirmation_sent.txt')


class AuthenticationBackendTests(TestCase):
    '''Tests related to the actual Authentication backend modules.'''

    def setUp(self):
        '''Set up method. Instantiate a user.'''
        user = get_user_model().objects.create(
            is_active=True,
            email='john@doe.com',
            username='john')
        user.set_password(user.username)
        user.save()
        braintree.Customer.delete(user.usermerchantid.customer_id)
        self.user = user

    @override_settings(
        ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.USERNAME)  # noqa
    def test_auth_by_username(self):
        '''Test authentication with username.'''

        user = self.user
        backend = AuthenticationBackend()
        self.assertEqual(
            backend.authenticate(
                username=user.username,
                password=user.username).pk,
            user.pk)
        self.assertEqual(
            backend.authenticate(
                username=user.email,
                password=user.username),
            None)

    @override_settings(
        ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.EMAIL)  # noqa
    def test_auth_by_email(self):
        '''Test authentication with email.'''

        user = self.user
        backend = AuthenticationBackend()
        self.assertEqual(
            backend.authenticate(
                username=user.email,
                password=user.username).pk,
            user.pk)
        self.assertEqual(
            backend.authenticate(
                username=user.username,
                password=user.username),
            None)

    @override_settings(
        ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.USERNAME_EMAIL)  # noqa
    def test_auth_by_username_or_email(self):
        '''Test authentication with username or email.'''

        user = self.user
        backend = AuthenticationBackend()
        self.assertEqual(
            backend.authenticate(
                username=user.email,
                password=user.username).pk,
            user.pk)
        self.assertEqual(
            backend.authenticate(
                username=user.username,
                password=user.username).pk,
            user.pk)


class UtilsTests(TestCase):
    '''Tests related to the utils module.'''

    def setUp(self):
        '''Set up method. Create the user bits.'''

        if hasattr(models, 'UUIDField'):
            self.user_id = uuid.uuid4().hex

            class UUIDUser(AbstractUser):
                '''Class instantiation of UUIDUser.'''
                id = models.UUIDField(primary_key=True,
                                      default=uuid.uuid4,
                                      editable=False)

                class Meta(AbstractUser.Meta):
                    '''Meta class instantiation of the UUIDUser class.'''
                    swappable = 'AUTH_USER_MODEL'
        else:
            UUIDUser = get_user_model()
        self.UUIDUser = UUIDUser

    def test_pk_to_url_string_identifies_UUID_as_stringlike(self):
        '''Test pk to url string identifies UUID as a string.'''

        user = self.UUIDUser(
            is_active=True,
            email='john@doe.com',
            username='john')
        self.assertEquals(user_pk_to_url_str(user), str(user.pk))

class UserProfileTests(TestCase):
    '''Tests related to the actual UserProfile and Model manager functionality.'''

    def setUp(self):
        '''Set up the user infrastructure.'''

        #User creation
        self.user = MyUser.objects.create_test_user(
            username="test",
            email="test@yahoo.com",
            password="password1!",
        )

        #User2 creation
        self.user2 = MyUser.objects.create_test_user(
            username="test2",
            email="test2@yahoo.com",
            password="password1!",
        )

        #User3 creation
        self.user3 = MyUser.objects.create_test_user(
            username="test3",
            email="test3@yahoo.com",
            password="password1!",
        )

        #Course Instantiation
        self.course = Course(
            name="testing course",
            slug="testing-course"
        )
        self.course.save()

    def test_user_profile_creation(self):
        '''Test the user profile automatic creation.'''
        assert len(UserProfile.objects.all()) == 3

    def test_user_profile_querysets(self):
        '''Test the user profile querysets.'''

        self.user.profile.update(course=self.course)
        self.user2.profile.update(course=self.course)
        self.user3.profile.update(course=self.course)

        self.user.profile.update(state="California")
        self.user2.profile.update(state="California")
        self.user3.profile.update(state="Nevada")

        self.user.profile.update(major="Engineering")
        self.user2.profile.update(major="Engineering")

        assert len(UserProfile.objects.get_profiles_by_course(course=self.course)) == 3
        assert len(UserProfile.objects.get_profiles_by_major(course=self.course, major="Engineering")) == 2
        assert len(UserProfile.objects.get_profiles_by_state(course=self.course, state="California")) == 2
