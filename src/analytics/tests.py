'''Tests page for the analytics Caprende module.'''

from django.test import TestCase

from course.models import Course, CourseSection
from categories.models import Category, SubCategory
from questions.models import Question
from users.models import MyUser

from .models import CategoryDataSet, SubCategoryDataSet

# Create your tests here.

class AnalyticsTests(TestCase):
    '''Tests related to the actual Analytics functionality.'''

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
        self.user = MyUser.objects.create_test_user(
            username="test",
            email="test@yahoo.com",
            password="password1!",
        )

        #Question creation
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
            index=1,
        )
        self.question.save()

    def tearDown(self):
        '''Tear down the infrastructure.'''
        pass

    def test_category_data_set_creation(self):
        '''Tests creating a category data set.'''

        CategoryDataSet.objects.create(
            user=self.user,
            category=self.category,
        )

    def test_subcategory_data_set_creation(self):
        '''Tests creating a subcategory data set.'''

        SubCategoryDataSet.objects.create(
            user=self.user,
            subcategory=self.subcategory,
        )

    def test_category_data_set_misc(self):
        '''Test add_correct and add_miss.'''

        dataset = CategoryDataSet.objects.create(
            user=self.user,
            category=self.category,
        )

        #Test attributes over 50 data entries
        missed = 0
        correct = 0
        for i in range(50):
            if i % 2:
                dataset.add_miss()
                missed += 1
                assert dataset.missed == missed
                assert dataset.correct == correct
                assert dataset.percent == (correct * 100) / (correct + missed)
            else:
                dataset.add_correct()
                correct += 1
                assert dataset.missed == missed
                assert dataset.correct == correct
                assert dataset.percent == (correct * 100) / (correct + missed)

    def test_subcategory_data_set_misc(self):
        '''Test add_correct and add_miss.'''

        dataset = SubCategoryDataSet.objects.create(
            user=self.user,
            subcategory=self.subcategory,
        )

        #Test attributes over 50 data entries
        missed = 0
        correct = 0
        for i in range(50):
            if i % 2:
                dataset.add_miss()
                missed += 1
                assert dataset.missed == missed
                assert dataset.correct == correct
                assert dataset.percent == (correct * 100) / (correct + missed)
            else:
                dataset.add_correct()
                correct += 1
                assert dataset.missed == missed
                assert dataset.correct == correct
                assert dataset.percent == (correct * 100) / (correct + missed)
