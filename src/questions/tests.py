'''Tests page for the questions Caprende module.'''
# pylint: disable=too-many-instance-attributes

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

        self.course2 = Course(
            name="testing course2",
            slug="testing-course2"
        )
        self.course2.save()

        #Course Section Instantiation
        self.coursesection = CourseSection(
            name="Section 1",
            course=self.course
        )
        self.coursesection.save()

        self.coursesection2 = CourseSection(
            name="Section 2",
            course=self.course2
        )
        self.coursesection2.save()

        #Category Instantiation
        self.category = Category(
            name="Category 1 for testing course",
            slug="cat-1-testing-course",
            section=self.coursesection,
        )
        self.category.save()

        self.category2 = Category(
            name="Category 1 for testing course",
            slug="cat-1-testing-course2",
            section=self.coursesection2,
        )
        self.category2.save()


        #SubCategory Instantiation
        self.subcategory = SubCategory(
            name="SubCategory 1 for testing course",
            slug="subcategory-1-testing-course",
            category=self.category,
        )
        self.subcategory.save()

        self.subcategory2 = SubCategory(
            name="SubCategory 2 for testing course",
            slug="subcategory-2-testing-course",
            category=self.category2,
        )
        self.subcategory2.save()

        #User creation
        self.user = MyUser.objects.create_test_user(
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
        )
        question.save()

        response = QuestionResponse.objects.create_response(
            user=self.user,
            question=question,
            attempt="A",
        )
        assert response.correct

    def test_question_index_creation(self):
        '''Tests the automatic index creation.'''
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
        )
        question.save()
        assert question.index == 1

        question2 = Question(
            course=self.course,
            section=self.coursesection,
            category=self.category,
            subcategory=self.subcategory,
            question_text="Here is another example question.",
            option_A="Here is option A.",
            option_B="Here is option B.",
            answer_letter="A",
            answer_explanation="Here is an example explanation.",
        )
        question2.save()
        assert question2.index == 2

        question3 = Question(
            course=self.course2,
            section=self.coursesection2,
            category=self.category2,
            subcategory=self.subcategory2,
            question_text="Here is another example question.",
            option_A="Here is option A.",
            option_B="Here is option B.",
            answer_letter="A",
            answer_explanation="Here is an example explanation.",
        )
        question3.save()
        assert question3.index == 1

        question4 = Question(
            course=self.course,
            section=self.coursesection,
            category=self.category,
            subcategory=self.subcategory,
            question_text="Here is another another example question.",
            option_A="Here is option A.",
            option_B="Here is option B.",
            answer_letter="A",
            answer_explanation="Here is an example explanation.",
        )
        question4.save()
        assert question4.index == 3
