'''Models page for the questions Caprende module.'''

from __future__ import unicode_literals

from django.db import models

from categories.models import Category, SubCategory
from course.models import Course, CourseSection
from users.models import MyUser

from .utils import upload_location

# Create your models here.

class QuestionQueryset(models.query.QuerySet):
    '''QuerySet for the Question class.'''

    def sort_by_test(self, test):
        '''Sort for questions by test.'''
        return self.filter(test=test)

    def sort_by_category(self, category):
        '''Sort for questions by category.'''
        return self.filter(category=category)

    def sort_by_subcategory(self, subcategory):
        '''Sort for questions by subcategory.'''
        return self.filter(subcategory=subcategory)

class QuestionManager(models.Manager):
    '''ModelManager for the Question class.'''

    def get_queryset(self):
        '''Get the queryset for questions.'''
        return QuestionQueryset(self.model, using=self._db)

    def sort_by_test(self, test):
        '''Sort for questions by test.'''
        return self.get_queryset().sort_by_test(test=test)

    def sort_by_category(self, category):
        '''Sort for questions by category.'''
        return self.get_queryset().sort_by_category(category=category)

    def sort_by_subcategory(self, subcategory):
        '''Sort for questions by subcategory.'''
        return self.get_queryset().sort_by_subcategory(subcategory=subcategory)

    def all(self):
        '''Return all the questions.'''
        return self.get_queryset()

class Question(models.Model):
    '''Base model for a Question for Caprende.'''

    course = models.ForeignKey(Course)
    section = models.ForeignKey(CourseSection)
    category = models.ForeignKey(Category)
    subcategory = models.ForeignKey(SubCategory)
    #FIXME: pre_save signal comparing both subcategories, checking that subcategory upwards match attributes
    question_text = models.TextField(
        max_length=1000,
    )
    passage = models.TextField(
        max_length=2000,
    )
    figure = models.FileField(
        upload_to=upload_location,
        null=True,
        blank=True,
    )
    option_A = models.CharField(
        max_length=300,
    )
    option_B = models.CharField(
        max_length=300,
    )
    option_C = models.CharField(
        max_length=300,
    )
    option_D = models.CharField(
        max_length=300,
    )
    option_E = models.CharField(
        max_length=300,
    )
    answer_letter = models.CharField(
        max_length=1,
    )
    answer_explanation = models.TextField(
        max_length=2000,
    )

    def __unicode__(self):
        return self.question_text

class QuestionResponseQueryset(models.query.QuerySet):
    '''QuerySet for the Question class.'''

    def sort_by_course(self, course):
        '''Sort for question responses by course.'''
        return self.filter(course=course)

    def sort_by_category(self, category):
        '''Sort for question responses by category.'''
        return self.filter(category=category)

    def sort_by_subcategory(self, subcategory):
        '''Sort for question responses by subcategory.'''
        return self.filter(subcategory=subcategory)

    def sort_by_user(self, user):
        '''Sort for question responses from a user.'''
        return self.filter(user=user)

class QuestionResponseManager(models.Manager):
    '''ModelManager for the QuestionResponse class.'''

    def get_queryset(self):
        '''Return the default queryset.'''
        return QuestionResponseQueryset(self.model, using=self._db)

    def create_response(self, user, question, correct=True):
        '''Create a QuestionResponse object after a user answers a question.'''

        response = self.model(
            user=user,
            course=question.course,
            section=question.section,
            category=question.category,
            subcategory=question.subcategory,
            question=question,
            correct=correct,
        )
        response.save(using=self._db)
        return response

class QuestionResponse(models.Model):
    '''Base model for a QuestionResponse for Caprende.'''

    user = models.ForeignKey(MyUser)
    course = models.ForeignKey(Course)
    section = models.ForeignKey(CourseSection)
    category = models.ForeignKey(Category)
    subcategory = models.ForeignKey(SubCategory)
    question = models.ForeignKey(Question)
    correct = models.BooleanField()

    def __unicode__(self):
        return self.user.username + " | " + self.question.question_text


