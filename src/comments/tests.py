'''Tests page for the comments Caprende module.'''

from django.test import TestCase

from course.models import Course, CourseSection
from categories.models import Category, SubCategory
from questions.models import Question
from users.models import MyUser

from .models import Comment

# Create your tests here.

class CommentTests(TestCase):
    '''Tests related to the actual Comment functionality.'''

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

    def test_comment_creation(self):
        '''Tests creating a question.'''

        Comment.objects.create_comment(
            user=self.user,
            text="Testing Comment Creation",
            question=self.question,
        )

    def test_reply_creation(self):
        '''Tests creating a reply.'''

        new_comment = Comment.objects.create_comment(
            user=self.user,
            text="Testing Comment Creation",
            question=self.question,
        )

        Comment.objects.create_comment(
            user=self.user,
            parent=new_comment,
            text="Testing Reply Creation",
            question=self.question,
        )

    def test_comment_misc(self):
        '''Testing the Comment model methods and misc attributes.'''

        new_comment = Comment.objects.create_comment(
            user=self.user,
            text="Testing Comment Creation",
            question=self.question,
        )

        new_reply = Comment.objects.create_comment(
            user=self.user,
            parent=new_comment,
            text="Testing Reply Creation",
            question=self.question,
        )

        #Test is_child
        assert not new_comment.is_child()
        assert new_reply.is_child()

        #Test get_children
        assert len(new_comment.get_children()) == 1
        assert new_comment.get_children()[0] == new_reply
        assert new_reply.get_children() is None
