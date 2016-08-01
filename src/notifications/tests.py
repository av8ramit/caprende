'''Tests page for the notifications Caprende module.'''

from django.test import TestCase

from course.models import Course, CourseSection
from categories.models import Category, SubCategory
from questions.models import Question
from users.models import MyUser

from .models import Notification

# Create your tests here.

class NotificationTests(TestCase):
    '''Tests related to the actual Notification functionality.'''

    def setUp(self):
        '''Set up the user infrastructure.'''

        #User creation
        self.user = MyUser.objects.create_user(
            username="test",
            email="test@yahoo.com",
            password="password1!",
        )

        #Course Instantiation
        self.course = Course(
            name="testing course",
            slug="testing-course"
        )
        self.course.save()

        #Course Section Instantiation
        self.coursesection = CourseSection(
            name="Section 1",
            course=self.course
        )
        self.coursesection.save()

        #Category Instantiation
        self.category = Category(
            name="Category 1 for testing course",
            slug="cat-1-testing-course",
            section=self.coursesection,
        )
        self.category.save()

        #SubCategory Instantiation
        self.subcategory = SubCategory(
            name="SubCategory 1 for testing course",
            slug="subcategory-1-testing-course",
            category=self.category,
        )
        self.subcategory.save()

        self.question = Question(
            course=self.course,
            section=self.coursesection,
            category=self.category,
            subcategory=self.subcategory,
            question_text="Here is an example question.",
            option_A="Here is option A.",
            option_B="Here is option B.",
            answer_letter="A",
            answer_explanation="Here is an example explanation.",
        )
        self.question.save()

    def test_notification_creation(self):
        '''Test the creation of a notification.'''

        notification = Notification.objects.create(
            text="Notification test",
            user=self.user,
            link=self.question.get_absolute_url()
        )

        notification.read = True
        notification.save()

