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

        self.user2 = MyUser.objects.create_test_user(
            username="test2",
            email="test2@yahoo.com",
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

    def test_category_data_set_by_state(self):
        '''Test the retrieval by state function.'''

        self.user.profile.update(course=self.course)
        self.user2.profile.update(course=self.course)

        self.user.profile.update(state="California")
        self.user2.profile.update(state="California")

        self.user.profile.update(major="Engineering")
        self.user2.profile.update(major="Engineering")

        self.user.profile.update(university="UC Berkeley")
        self.user2.profile.update(university="UC Berkeley")

        dataset = CategoryDataSet.objects.create(
            user=self.user,
            category=self.category,
        )
        dataset.add_correct()
        dataset.add_correct()
        dataset.add_correct()
        dataset.add_miss()
        dataset.add_miss()

        assert CategoryDataSet.objects.stats_by_state(category=self.category, state="California") == (3, 5)
        assert CategoryDataSet.objects.stats_by_major(category=self.category, major="Engineering") == (3, 5)
        assert CategoryDataSet.objects.stats_by_university(category=self.category, university="UC Berkeley") == (3, 5)

        dataset2 = CategoryDataSet.objects.create(
            user=self.user2,
            category=self.category,
        )
        dataset2.add_correct()

        assert CategoryDataSet.objects.stats_by_state(category=self.category, state="California") == (4, 6)
        assert CategoryDataSet.objects.stats_by_major(category=self.category, major="Engineering") == (4, 6)
        assert CategoryDataSet.objects.stats_by_university(category=self.category, university="UC Berkeley") == (4, 6)

    def test_subcategory_data_set_by_state(self):
        '''Test the retrieval by state function.'''

        self.user.profile.update(course=self.course)
        self.user2.profile.update(course=self.course)

        self.user.profile.update(state="California")
        self.user2.profile.update(state="California")

        self.user.profile.update(major="Engineering")
        self.user2.profile.update(major="Engineering")

        self.user.profile.update(university="UC Berkeley")
        self.user2.profile.update(university="UC Berkeley")

        dataset = SubCategoryDataSet.objects.create(
            user=self.user,
            subcategory=self.subcategory,
        )
        dataset.add_correct()
        dataset.add_correct()
        dataset.add_correct()
        dataset.add_miss()
        dataset.add_miss()

        assert SubCategoryDataSet.objects.stats_by_state(subcategory=self.subcategory, state="California") == (3, 5)
        assert SubCategoryDataSet.objects.stats_by_major(subcategory=self.subcategory, major="Engineering") == (3, 5)
        assert SubCategoryDataSet.objects.stats_by_university(subcategory=self.subcategory, university="UC Berkeley") == (3, 5)

        dataset = SubCategoryDataSet.objects.create(
            user=self.user2,
            subcategory=self.subcategory,
        )
        dataset.add_correct()

        assert SubCategoryDataSet.objects.stats_by_state(subcategory=self.subcategory, state="California") == (4, 6)
        assert SubCategoryDataSet.objects.stats_by_major(subcategory=self.subcategory, major="Engineering") == (4, 6)
        assert SubCategoryDataSet.objects.stats_by_university(subcategory=self.subcategory, university="UC Berkeley") == (4, 6)

