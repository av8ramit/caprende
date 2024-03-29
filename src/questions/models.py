'''Models page for the questions Caprende module.'''
# pylint: disable=no-member

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save

from categories.models import Category, SubCategory
from course.models import Course, CourseSection
from users.models import MyUser

from .utils import upload_location

# Create your models here.

class QuestionQueryset(models.query.QuerySet):
    '''QuerySet for the Question class.'''

    def sort_by_course(self, course):
        '''Sort for questions by course.'''
        return self.filter(course=course)

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

    def get_index(self, course, index):
        '''Return the question with the corresponding index and course.'''
        return self.get_queryset().filter(course=course).get(index=index)

    def get_latest(self, course):
        '''Return the latest question by course.'''
        qs = self.get_queryset().filter(course=course)
        if len(qs) >= 1:
            return qs[0]
        else:
            return None

    def all(self):
        '''Return all the questions.'''
        return self.get_queryset()

class Question(models.Model):
    '''Base model for a Question for Caprende.'''

    course = models.ForeignKey(Course)
    section = models.ForeignKey(CourseSection)
    category = models.ForeignKey(Category)
    subcategory = models.ForeignKey(SubCategory)
    question_text = models.TextField(
        max_length=1000,
    )
    question_text = models.TextField(
        max_length=1000,
    )
    passage = models.TextField(
        max_length=2000,
        null=True,
        blank=True,
    )
    source = models.CharField(
        max_length=600,
        null=True,
        blank=True,
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
        null=True,
        blank=True,
    )
    option_D = models.CharField(
        max_length=300,
        null=True,
        blank=True,
    )
    option_E = models.CharField(
        max_length=300,
        null=True,
        blank=True,
    )
    answer_letter = models.CharField(
        max_length=1,
    )
    answer_explanation = models.TextField(
        max_length=2000,
    )
    index = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )
    objects = QuestionManager()

    class Meta:
        '''Meta class invocation for Question class.'''
        unique_together = ('index', 'course')
        ordering = ['course', '-index']

    def __unicode__(self):
        return self.question_text

    def get_absolute_url(self):
        '''Return the URL to the question.'''
        return reverse("question_detail", kwargs={"course_slug" : self.course.slug, "question_index" : self.index})

    def category_string(self):
        '''Return the category string.'''
        return unicode(self.category).split(" | ")[-1]

    def choices(self):
        '''Return a list of choices for the question.'''
        choices = []
        if self.option_A:
            choices.append((self.option_A, "A", self.answer_letter == 'A'))
        if self.option_B:
            choices.append((self.option_B, "B", self.answer_letter == 'B'))
        if self.option_C:
            choices.append((self.option_C, "C", self.answer_letter == 'C'))
        if self.option_D:
            choices.append((self.option_D, "D", self.answer_letter == 'D'))
        if self.option_E:
            choices.append((self.option_E, "E", self.answer_letter == 'E'))
        return choices

def set_question_index_receiver(sender, instance, *args, **kwargs):
    '''Receiver function for assigning a question the next index.'''

    #New question created
    if instance.index is None:
        latest_question = Question.objects.get_latest(instance.course)

        #If a question for this course has been created
        if latest_question is not None:
            instance.index = latest_question.index + 1
        #First question in this course
        else:
            instance.index = 1

pre_save.connect(set_question_index_receiver, sender=Question)

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

    def get_response(self, user, question):
        '''Return the response for a user for a particular question.'''
        try:
            return self.get(user=user, question=question)
        except self.model.DoesNotExist:
            return None

class QuestionResponseManager(models.Manager):
    '''ModelManager for the QuestionResponse class.'''

    def get_queryset(self):
        '''Return the default queryset.'''
        return QuestionResponseQueryset(self.model, using=self._db)

    def create_response(self, user, question, attempt):
        '''Create a QuestionResponse object after a user answers a question.'''

        response = self.model(
            user=user,
            course=question.course,
            section=question.section,
            category=question.category,
            subcategory=question.subcategory,
            question=question,
            attempt=attempt,
            correct=attempt == question.answer_letter,
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
    attempt = models.CharField(
        max_length=1,
    )
    correct = models.BooleanField()

    objects = QuestionResponseManager()

    class Meta:
        '''Meta class invocation for QuestionResponse class.'''
        unique_together = ('user', 'question')

    def __unicode__(self):
        return self.user.username + " | " + self.question.question_text

