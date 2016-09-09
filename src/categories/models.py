'''Models page for the categories Caprende module.'''
# pylint: disable=no-member

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify

from course.models import CourseSection

# Create your models here.

class CategoryQuerySet(models.query.QuerySet):
    '''Category Query Set'''

    def by_section(self, section):
        '''Return the categories associated with a section from a course.'''
        return self.filter(section=section)

class CategoryManager(models.Manager):
    '''Category Model Manager'''

    def get_queryset(self):
        '''Get the queryset of Category.'''
        return CategoryQuerySet(self.model, using=self._db)

    def all(self):
        '''Return all the categories.'''
        return self.get_queryset()

    def by_section(self, section):
        '''Return all the categories by section.'''
        return self.all().by_section(section=section)

class Category(models.Model):
    '''Base model for a Category for a Course for Caprende.'''

    name = models.CharField(
        max_length=120,
    )
    slug = models.SlugField(
        default='default-slug',
        unique=True,
    )
    description = models.TextField(
        max_length=2000,
        default="",
        null=True,
    )
    section = models.ForeignKey(CourseSection)

    objects = CategoryManager()

    class Meta:
        '''Meta class invocation for Category class.'''
        unique_together = ('section', 'name')

    @property
    def course(self):
        '''Return the course the Category belongs to.'''
        return self.section.course

    def __unicode__(self):
        return self.course.name + " | " + self.section.name + " | " + self.name

    def get_absolute_url(self):
        '''Return the URL to the category.'''
        return reverse("category_detail", kwargs={"slug": self.slug})

    def get_all_sections(self):
        '''Return all the subcategories by category.'''
        return self.subcategory_set.all()

def set_category_slug_receiver(sender, instance, created, *args, **kwargs):
    '''Receiver function for assigning a slug to a category.'''

    if created:
        instance.slug = slugify(instance.name + " " + instance.section.course.name)
        instance.save()

post_save.connect(set_category_slug_receiver, sender=Category)

class SubCategoryQuerySet(models.query.QuerySet):
    '''SubCategory Query Set'''

    def by_category(self, category):
        '''Return the subcategories associated with a category.'''
        return self.filter(category=category)

class SubCategoryManager(models.Manager):
    '''SubCategory Model Manager'''

    def get_queryset(self):
        '''Get the queryset of SubCategory.'''
        return SubCategoryQuerySet(self.model, using=self._db)

    def all(self):
        '''Return all the subcategories.'''
        return self.get_queryset()

    def by_category(self, category):
        '''Return all the subcategories by category.'''
        return self.all().by_category(category=category)

class SubCategory(models.Model):
    '''Base mode for a SubCategory for a Category for Caprende.'''

    name = models.CharField(
        max_length=250,
    )
    slug = models.SlugField(
        default='default-slug',
        unique=True,
    )
    description = models.TextField(
        max_length=2000,
        default="",
        null=True,
    )
    category = models.ForeignKey(Category)

    objects = SubCategoryManager()

    class Meta:
        '''Meta class invocation for SubCategory class.'''
        unique_together = ('category', 'name')

    @property
    def section(self):
        '''Return the section of the course the SubCategory belongs to.'''
        return self.category.section

    @property
    def course(self):
        '''Return the course the SubCategory belongs to.'''
        return self.section.course

    def get_absolute_url(self):
        '''Return the URL to the subcategory.'''
        return reverse("subcategory_detail", kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.course.name + " | " + self.section.name + " | " + self.category.name + " | " + self.name

def set_subcategory_slug_receiver(sender, instance, created, *args, **kwargs):
    '''Receiver function for assigning a slug to a subcategory.'''

    if created:
        instance.slug = slugify(instance.name + " " + instance.category.name + " " + instance.category.section.course.name)
        instance.save()

post_save.connect(set_subcategory_slug_receiver, sender=SubCategory)


