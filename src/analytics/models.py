'''Models page for the analytics Caprende module.'''
# pylint: disable=no-member

from __future__ import unicode_literals

from django.db import models

from categories.models import Category, SubCategory
from users.models import MyUser

# Create your models here.

class CategoryDataSetQueryset(models.query.QuerySet):
    '''QuerySet for the CategoryDataSet class.'''

    def sort_by_user(self, user):
        '''Sort for datasets by user.'''
        return self.filter(user=user)

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
