'''Tests page for the questions Caprende module.'''

from django.test import TestCase

from course.models import Course, CourseSection
from categories.models import Category, SubCategory
from users.models import MyUser

from .models import Question, QuestionResponse

# Create your tests here.

class QuestionTests(TestCase):
    '''Tests related to the actual Category and Subcategory functionality.'''

    def setUp(self):
        '''Set up the test and category infrastructure.'''

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

        #User creation
        self.user = MyUser.objects.create_user(
            username="test",
            email="test@yahoo.com",
            password="password1!",
        )


    def tearDown(self):
        '''Tear down the infrastructure.'''
        pass

    def test_question_creation(self):
        '''Tests creating a question.'''
        question = Question(
            course=self.course,
            section=self.coursesection,
            category=self.category,
            subcategory=self.subcategory,
            question_text="Here is an example question.",
            option_A="Here is option A.",
            option_B="Here is option B.",
            answer_letter="A",
            answer_explanation="Here is an example explanation.",
            index=1,
        )
        question.save()

    def test_question_response_creation(self):
        '''Tests creating a question response.'''
        question = Question(
            course=self.course,
            section=self.coursesection,
            category=self.category,
            subcategory=self.subcategory,
            question_text="Here is an example question.",
            option_A="Here is option A.",
            option_B="Here is option B.",
            answer_letter="A",
            answer_explanation="Here is an example explanation.",
            index=1,
        )
        question.save()

        response = QuestionResponse.objects.create_response(
            user=self.user,
            question=question,
            attempt="A",
        )
        assert response.correct




