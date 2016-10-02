'''Models page for the course Caprende module.'''
# pylint: disable=no-member

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify

from .utils import upload_location

# Create your models here.

class CourseQuerySet(models.query.QuerySet):
    '''Course Query Set'''

    def active(self):
        '''Return the activated courses.'''
        return self.filter(active=True)

    def featured(self):
        '''Return the featured courses.'''
        return self.filter(featured=True)

class CourseManager(models.Manager):
    '''Course Model Manager'''

    def get_queryset(self):
        '''Get the queryset of Course.'''
        return CourseQuerySet(self.model, using=self._db)

    def all(self):
        '''Return all the courses.'''
        return self.get_queryset()

class Course(models.Model):
    '''Base model for a Course or a Test for Caprende.'''

    name = models.CharField(
        max_length=120,
        unique=True,
    )
    slug = models.SlugField(
        default='default-slug',
        unique=True,
    )
    description = models.TextField(
        max_length=2000,
        default="",
        null=True
    )
    course_json_file = models.FileField(
        upload_to=upload_location,
        null=True,
        blank=True,
    )
    question_json_file = models.FileField(
        upload_to=upload_location,
        null=True,
        blank=True,
    )
    active = models.BooleanField(
        default=True,
    )
    featured = models.BooleanField(
        default=True,
    )

    objects = CourseManager()

    def __unicode__(self):
        return self.name

    def get_sections(self):
        '''Return a query set of the Sections for a given test.'''
        return self.coursesection_set.all()

    def get_absolute_url(self):
        '''Return the URL for the course_detail for the particular course.'''
        return reverse("course_detail", kwargs={"slug": self.slug})

    def get_all_sections(self):
        '''Return all the sections by course.'''
        return self.coursesection_set.all()

    def get_all_categories(self):
        '''Return all the categories by course.'''
        categories = []
        for section in self.get_all_sections():
            categories += section.get_all_categories()
        return categories

    def get_all_subcategories(self):
        '''Return all the subcategories by course.'''
        subcategories = []
        for category in self.get_all_categories():
            subcategories += category.get_all_subcategories()
        return subcategories

def set_course_slug_receiver(sender, instance, created, *args, **kwargs):
    '''Receiver function for assigning a question the next index.'''

    if created:
        instance.slug = slugify(instance.name)
        instance.save()

post_save.connect(set_course_slug_receiver, sender=Course)

class CourseSectionQuerySet(models.query.QuerySet):
    '''Course Query Set'''

    def by_course(self, course):
        '''Return all CourseSections from a given course.'''
        return self.filter(course=course)

class CourseSectionManager(models.Manager):
    '''Course Model Manager'''

    def get_queryset(self):
        '''Get the queryset of Course.'''
        return CourseSectionQuerySet(self.model, using=self._db)

    def all(self):
        '''Return all the courses.'''
        return self.get_queryset()

    def by_course(self, course):
        '''Return the queryset by course.'''
        return self.get_queryset().by_course(course=course)

class CourseSection(models.Model):
    '''Base model for a Course Section Type.'''

    course = models.ForeignKey(Course)
    name = models.CharField(
        max_length=120
    )
    slug = models.SlugField(
        default='default-slug',
        unique=True,
    )
    description = models.TextField(
        max_length=10000,
        default="",
        null=True
    )

    def get_all_categories(self):
        '''Return all the categories by section.'''
        return self.category_set.all()

    class Meta:
        '''Meta class invocation for CourseSection class.'''
        unique_together = ('course', 'name')

    def __unicode__(self):
        return self.course.name + " | " + self.name

def set_course_section_slug_receiver(sender, instance, created, *args, **kwargs):
    '''Receiver function for assigning a question the next index.'''

    if created:
        instance.slug = slugify(instance.name)
        instance.save()

post_save.connect(set_course_section_slug_receiver, sender=CourseSection)
