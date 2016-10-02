'''Tests page for the categories Caprende module.'''
# pylint: disable=bare-except,no-self-use,no-member


from django.test import TestCase

from course.models import Course, CourseSection

from .models import Category, SubCategory

# Create your tests here.

class CategoryTests(TestCase):
    '''Tests related to the actual Category and Subcategory functionality.'''

    def test_category_creation(self):
        '''Tests creating a category.'''
        course = Course(
            name="testing course",
            slug="testing-course"
        )
        course.save()

        coursesection = CourseSection(name="Section 1", course=course)
        coursesection.save()

        category = Category(
            name="Category 1 for testing course",
            slug="cat-1-testing-course",
            section=coursesection,
        )
        category.save()

        assert category.course == course
        assert category.section == coursesection

        assert len(course.get_all_categories()) == 1
        assert len(course.get_all_subcategories()) == 0

        #Test get_absolute_url
        resp = self.client.get(category.get_absolute_url())
        self.assertEqual(resp.status_code, 302)

    def test_category_uniqueness(self):
        '''Testing the uniqueness of a Category.'''

        course = Course(
            name="testing course",
            slug="testing-course"
        )
        course.save()

        coursesection = CourseSection(name="Section 1", course=course)
        coursesection.save()

        category = Category(
            name="Category 1 for testing course",
            slug="cat-1-testing-course",
            section=coursesection,
        )
        category.save()

        category2 = Category(
            name="Category 2 for testing course",
            slug="cat-2-testing-course",
            section=coursesection,
        )
        category2.save()

        course2 = Course(
            name="testing course2",
            slug="testing-course2"
        )
        course2.save()

        assert len(coursesection.category_set.all()) == 2

        coursesection2 = CourseSection(name="Section 2", course=course2)
        coursesection2.save()

        category3 = Category(
            name="Category 2 for testing course",
            slug="cat-3-testing-course2",
            section=coursesection2,
        )
        category3.save()
        #Same category name, different coursesection

        #Attempt to save to the same category
        category3.section = coursesection
        try:
            category3.save()
            #If save was successful, category and category3 violate uniqueness
            raise RuntimeError("category3 has the same credentials as course")
        except:
            pass


    def test_subcategory_creation(self):
        '''Tests creating a subcategory.'''

        course = Course(
            name="testing course",
            slug="testing-course"
        )
        course.save()

        coursesection = CourseSection(name="Section 1", course=course)
        coursesection.save()

        category = Category(
            name="Category 1 for testing course",
            slug="cat-1-testing-course",
            section=coursesection,
        )
        category.save()

        subcategory = SubCategory(
            name="SubCategory 1 for testing course",
            slug="subcategory-1-testing-course",
            category=category,
        )
        subcategory.save()

        assert len(course.get_all_categories()) == 1
        assert len(course.get_all_subcategories()) == 1

        #Test get_absolute_url
        resp = self.client.get(subcategory.get_absolute_url())
        self.assertEqual(resp.status_code, 302)

    def test_subcategory_uniqueness(self):
        '''Testing the uniqueness of a SubCategory.'''

        course = Course(
            name="testing course",
            slug="testing-course"
        )
        course.save()

        coursesection = CourseSection(name="Section 1", course=course)
        coursesection.save()

        category = Category(
            name="Category 1 for testing course",
            slug="cat-1-testing-course",
            section=coursesection,
        )
        category.save()

        subcategory = SubCategory(
            name="SubCategory 1 for testing course",
            slug="subcategory-1-testing-course",
            category=category,
        )
        subcategory.save()

        subcategory2 = SubCategory(
            name="SubCategory 2 for testing course",
            slug="subcategory-2-testing-course",
            category=category,
        )
        subcategory2.save()


        course2 = Course(
            name="testing course2",
            slug="testing-course2"
        )
        course2.save()

        coursesection2 = CourseSection(name="Section 2", course=course2)
        coursesection2.save()

        category2 = Category(
            name="Category 1 for testing course",
            slug="cat-1-testing-course2",
            section=coursesection2,
        )
        category2.save()

        #Saving a subcategory with the same name as another one that exists under a new category
        #Should save properly
        subcategory4 = SubCategory(
            name="SubCategory 1 for testing course",
            slug="subcategory-1-testing-course2",
            category=category2,
        )
        subcategory4.save()

        subcategory3 = SubCategory(
            name="SubCategory 2 for testing course",
            slug="subcategory-3-testing-course",
            category=category,
        )

        try:
            subcategory3.save()
            #If save was successful, subcategory and subcategory3 violate uniqueness
            raise RuntimeError("subcategory3 has the same credentials as course")
        except:
            pass





