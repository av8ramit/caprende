'''Models page for the analytics Caprende module.'''
# pylint: disable=no-member

from __future__ import unicode_literals

from django.db import models

from categories.models import Category, SubCategory
from users.models import MyUser, UserProfile

# Create your models here.

class CategoryDataSetQueryset(models.query.QuerySet):
    '''QuerySet for the CategoryDataSet class.'''

    def sort_by_user(self, user):
        '''Sort for datasets by user.'''
        return self.filter(user=user)

    def sort_by_category(self, category):
        '''Sort for datasets by category.'''
        return self.filter(category=category)

class CategoryDataSetManager(models.Manager):
    '''ModelManager for the CategoryDataSet class.'''

    def get_queryset(self):
        '''Get the queryset for CategoryDataSets.'''
        return CategoryDataSetQueryset(self.model, using=self._db)

    def all(self):
        '''Return all the CategoryDataSets.'''
        return self.get_queryset()

    def sort_by_user(self, user):
        '''Sort for datasets by user.'''
        return self.get_queryset().sort_by_user(user=user)

    def sort_by_category(self, category):
        '''Sort for datasets by category.'''
        return self.get_queryset().sort_by_category(category=category)

    def get_stats(self, category, similar_users):
        '''When given a QuerySet of similar UserProfiles, return the correct, total.'''
        correct = 0
        total = 0
        for userprofile in similar_users:
            dataset = self.sort_by_user(user=userprofile.user).sort_by_category(category=category)
            assert len(dataset) <= 1
            if dataset:
                correct += dataset[0].correct
                total += dataset[0].correct + dataset[0].missed
        return correct, total

    def stats_by_state(self, category, state):
        '''Return a tuple of correct and total for datasets from a state.'''
        similar_users = UserProfile.objects.get_profiles_by_state(course=category.section.course, state=state)
        return self.get_stats(category=category, similar_users=similar_users)

    def stats_by_major(self, category, major):
        '''Return a tuple of correct and total for datasets for a major.'''
        similar_users = UserProfile.objects.get_profiles_by_major(course=category.section.course, major=major)
        return self.get_stats(category=category, similar_users=similar_users)

    def stats_by_university(self, category, university):
        '''Return a tuple of correct and total for datasets for a university.'''
        similar_users = UserProfile.objects.get_profiles_by_university(course=category.section.course, university=university)
        return self.get_stats(category=category, similar_users=similar_users)

    def create(self, user, category):
        '''Create a CategoryDataSet.'''
        dataset = self.model(
            user=user,
            category=category,
        )
        dataset.save(using=self._db)
        return dataset

class CategoryDataSet(models.Model):
    '''Base model for a CategoryDataSet for Caprende.'''

    user = models.ForeignKey(MyUser)
    category = models.ForeignKey(Category)
    correct = models.PositiveSmallIntegerField(default=0)
    missed = models.PositiveSmallIntegerField(default=0)
    percent = models.PositiveIntegerField(default=0)

    objects = CategoryDataSetManager()

    class Meta:
        '''Meta class invocation for CategoryDataSet.'''
        unique_together = ('user', 'category')

    @property
    def total(self):
        '''Return the total number of questions seen by this user of this Category.'''
        return self.correct + self.missed

    def add_correct(self):
        '''Add a correct answer to a user's CategoryDataSet.'''
        self.correct += 1
        self.percent = (self.correct * 100) / self.total
        self.save()

    def add_miss(self):
        '''Add an incorrect answer to a user's CategoryDataSet.'''
        self.missed += 1
        self.percent = (self.correct * 100) / self.total
        self.save()


    def __unicode__(self):
        return self.user.username + " | " + self.category.name + " | " + str(self.percent)

class SubCategoryDataSetQueryset(models.query.QuerySet):
    '''QuerySet for the SubCategoryDataSet class.'''

    def sort_by_user(self, user):
        '''Sort for datasets by user.'''
        return self.filter(user=user)

    def sort_by_subcategory(self, subcategory):
        '''Sort for datasets by category.'''
        return self.filter(subcategory=subcategory)

class SubCategoryDataSetManager(models.Manager):
    '''ModelManager for the SubCategoryDataSet class.'''

    def get_queryset(self):
        '''Get the queryset for SubCategoryDataSets.'''
        return SubCategoryDataSetQueryset(self.model, using=self._db)

    def all(self):
        '''Return all the SubCategoryDataSets.'''
        return self.get_queryset()

    def sort_by_user(self, user):
        '''Sort for datasets by user.'''
        return self.get_queryset().sort_by_user(user=user)

    def sort_by_subcategory(self, subcategory):
        '''Sort for datasets by category.'''
        return self.get_queryset().sort_by_subcategory(subcategory=subcategory)

    def get_stats(self, subcategory, similar_users):
        '''When given a QuerySet of similar UserProfiles, return the correct, total.'''
        correct = 0
        total = 0
        for userprofile in similar_users:
            dataset = self.sort_by_user(user=userprofile.user).sort_by_subcategory(subcategory=subcategory)
            assert len(dataset) <= 1
            if dataset:
                correct += dataset[0].correct
                total += dataset[0].correct + dataset[0].missed
        return correct, total

    def stats_by_state(self, subcategory, state):
        '''Return a tuple of correct and total for datasets from a state.'''
        similar_users = UserProfile.objects.get_profiles_by_state(course=subcategory.category.section.course, state=state)
        return self.get_stats(subcategory=subcategory, similar_users=similar_users)

    def stats_by_major(self, subcategory, major):
        '''Return a tuple of correct and total for datasets for a major.'''
        similar_users = UserProfile.objects.get_profiles_by_major(course=subcategory.category.section.course, major=major)
        return self.get_stats(subcategory=subcategory, similar_users=similar_users)

    def stats_by_university(self, subcategory, university):
        '''Return a tuple of correct and total for datasets for a university.'''
        similar_users = UserProfile.objects.get_profiles_by_university(course=subcategory.category.section.course, university=university)
        return self.get_stats(subcategory=subcategory, similar_users=similar_users)

    def create(self, user, subcategory):
        '''Create a SubCategoryDataSet.'''
        dataset = self.model(
            user=user,
            subcategory=subcategory,
        )
        dataset.save(using=self._db)
        return dataset

class SubCategoryDataSet(models.Model):
    '''Base model for a SubCategoryDataSet for Caprende.'''

    user = models.ForeignKey(MyUser)
    subcategory = models.ForeignKey(SubCategory)
    correct = models.PositiveSmallIntegerField(default=0)
    missed = models.PositiveSmallIntegerField(default=0)
    percent = models.PositiveIntegerField(default=0)

    objects = SubCategoryDataSetManager()

    class Meta:
        '''Meta class invocation for SubCategoryDataSet.'''
        unique_together = ('user', 'subcategory')

    @property
    def total(self):
        '''Return the total number of questions seen by this user of this Category.'''
        return self.correct + self.missed

    def add_correct(self):
        '''Add a correct answer to a user's SubCategoryDataSet.'''
        self.correct += 1
        self.percent = (self.correct * 100) / self.total
        self.save()

    def add_miss(self):
        '''Add an incorrect answer to a user's SubCategoryDataSet.'''
        self.missed += 1
        self.percent = (self.correct * 100) / self.total
        self.save()

    def __unicode__(self):
        return self.user.username + " | " + self.subcategory.name + " | " + str(self.percent)
