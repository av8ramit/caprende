'''Models page for the users Caprende module.'''
# pylint: disable=no-member,too-many-arguments

from __future__ import unicode_literals

import braintree

from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django.db.models.signals import post_save
from django.http import Http404

from billing.models import UserMerchantId
from course.models import Course

from .utils import upload_location, UNIVERSITY_LIST, MAJOR_LIST

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id=settings.BRAINTREE_MERCHANT_ID,
                                  public_key=settings.BRAINTREE_PUBLIC_KEY,
                                  private_key=settings.BRAINTREE_PRIVATE_KEY)

class MyUserManager(BaseUserManager):
    '''Model manager for the MyUser class.'''

    def create_user(self, username=None, email=None, password=None):
        '''Creates and saves a User with the given username, email and password.'''

        if not username:
            raise ValueError('Must include username')

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_test_user(self, username=None, email=None, password=None):
        '''Creates and saves a User with the given username, email and password.'''

        if not username:
            raise ValueError('Must include username')

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        braintree.Customer.delete(user.usermerchantid.customer_id)
        return user

    def create_superuser(self, username, email, password):
        '''Creates and saves a superuser with the given username, email and password.'''

        user = self.create_user(
            username=username,
            email=email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    '''Base model custom User class for authentication.'''

    username = models.CharField(
        max_length=255,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Email Address',
        max_length=255,
        unique=True,
    )
    is_member = models.BooleanField(
        default=False,
        verbose_name='Is Paid Member'
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __unicode__(self):
        '''Return the username as the string representation.'''
        return self.username

    def has_module_perms(self, app_label):
        '''Does the user have permissions to view the app `app_label`?'''
        return self.is_active

    def has_perm(self, app_label):
        '''Does the user have permissions to view the app `app_label`?'''
        return self.is_active

    @property
    def profile(self):
        '''Return the profile object associated with this user.'''
        return UserProfile.objects.get(user=self)

    @property
    def is_staff(self):
        '''Is the user a member of staff?'''
        return self.is_admin

    def get_short_name(self):
        '''The user is identified by username.'''
        return self.username

    def get_full_name(self):
        '''The user is identified by username.'''
        return self.profile.get_full_name()

class UserProfileManager(models.Manager):
    '''Model manager for the UserProfile class.'''

    def get_profiles_by_course(self, course):
        '''Return all users that belong to a particular class.'''
        return self.filter(course=course)

class UserProfile(models.Model):
    '''Base model custom User class for authentication.'''

    user = models.OneToOneField(MyUser)
    first_name = models.CharField(
        max_length=120,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=120,
        null=True,
        blank=True,
    )
    profile_image = models.FileField(
        upload_to=upload_location,
        null=True,
        blank=True,
    )
    course = models.ForeignKey(Course, null=True)
    motivational_image = models.FileField(
        upload_to=upload_location,
        null=True,
        blank=True,
    )
    university = models.CharField(
        max_length=100,
        choices=UNIVERSITY_LIST,
        null=True,
        blank=True
    )
    major = models.CharField(
        max_length=100,
        choices=MAJOR_LIST,
        null=True,
        blank=True
    )
    completed = models.BooleanField(
        default=True
    )
    next_question_index = models.PositiveIntegerField(
        default=1
    )

    objects = UserProfileManager()

    def update(self,
               first_name=None,
               last_name=None,
               profile_image=None,
               course=None,
               motivational_image=None,
               university=None,
               major=None
              ):
        '''Update the profile with any relevant information.'''

        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if profile_image:
            self.profile_image = profile_image
        if course:
            self.course = course
            print course
        if motivational_image:
            self.motivational_image = motivational_image
        if university:
            self.university = university
        if major:
            self.major = major
        self.save()

    def get_full_name(self):
        '''The user is identified by their email address.'''
        return "%s %s" % (self.first_name, self.last_name)

    def get_short_name(self):
        '''The user is identified by their email address.'''
        if self.first_name:
            return self.first_name
        else:
            return self.username

    def increase_question_index(self):
        '''Increase the question index by 1.'''
        self.next_question_index += 1
        self.save()

    def __unicode__(self):
        return self.user.username


def new_user_receiver(sender, instance, created, *args, **kwargs):
    '''Receiver function for new user creation.'''
    if created:
        UserProfile.objects.create(user=instance)
    try:
        merchant_obj = UserMerchantId.objects.get(user=instance)
    except UserMerchantId.DoesNotExist:
        new_customer_result = braintree.Customer.create({
            "email" : instance.email
        })
        if new_customer_result.is_success:
            merchant_obj, created = UserMerchantId.objects.get_or_create(user=instance)
            merchant_obj.customer_id = new_customer_result.customer.id
            merchant_obj.save()
        else:
            raise Http404("There was an error with your account. Please contact us.")

def new_profile_receiver(sender, instance, created, *args, **kwargs):
    '''Receiver function for new profile creation.'''
    if created:
        instance.completed = False
    else:
        instance.completed = True

post_save.connect(new_user_receiver, sender=MyUser)
post_save.connect(new_profile_receiver, sender=UserProfile)






