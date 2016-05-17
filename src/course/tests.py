'''Tests page for the course Caprende module.'''
# pylint: disable=bare-except,no-self-use,no-member

from django.test import TestCase

from .models import Course, CourseSection

# Create your tests here.

class CourseTests(TestCase):
    '''Tests related to the actual Course functionality.'''

    def test_course_creation(self):
        '''Tests creating a course.'''
        course = Course(
            name="testing course",
            slug="testing-course"
        )
        course.save()
        assert course.name == "testing course"
        assert course.slug == "testing-course"

        #Test get_absolute_url
        resp = self.client.get(course.get_absolute_url())
        self.assertEqual(resp.status_code, 200)

        course2 = Course(
            name="testing course",
            slug="testing-course"
        )
        try:
            course2.save()
            #If save was successful, course and course2 violate uniqueness
            raise RuntimeError("course2 has the same credentials as course")
        except:
            pass

    def test_section_creation(self):
        '''Tests creating sections for a course.'''
        course = Course(
            name="testing course",
            slug="testing-course"
        )
        course.save()
        coursesection = CourseSection(name="Section 1", course=course)
        coursesection.save()

        coursesection2 = CourseSection(name="Section 2", course=course)
        coursesection2.save()

        assert len(course.coursesection_set.all()) == 2

        coursesection3 = CourseSection(name="Section 1", course=course)
        try:
            coursesection3.save()
            #If save was successful, course and course2 violate uniqueness
            raise RuntimeError("coursesection3 has the same credentials as course")
        except:
            pass

