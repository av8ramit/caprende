Caprende
===================


This is the Github repository for the entire caprende django project. It includes multiple individual applications as well as the linting executable, pylintrc, gitignore, and the pip requirements list.

----------


Modules
-------------

These are the individual caprende modules that work together to create the website.

#### <i class="icon-file"></i> caprende
This is the main module that is created by default. This contains the url resolution file, the settings file, views file, and wsgi file.

#### <i class="icon-file"></i> users

This contains the main MyUser and UserProfile class. The UserProfile class is a ForeignKey object of the MyUser class. The MyUser class overwrites django-allauth default user class. The UserProfile class contains all the personal information regarding the user. The MyUser class contains the email, password, and username.

#### <i class="icon-file"></i> course

This contains the Course and CourseSection class. Each course is created for any test. Individual sections obviously correspond to larger sections in the course or test itself. 

#### <i class="icon-file"></i> categories

This contains the Category and SubCategory class that both connect to the Course module. Each CourseSection has a set of Category objects and each of those corresponding Category objects has a set of SubCategories.

#### <i class="icon-file"></i> questions

Each Question object is assigned to a SubCategory. This application also contains the QuestionResponse object. For every Question in a Course that a user answers, a QuestionResponse object is created. Based on the set of a user's QuestionResponse objects we create an analysis report.

#### <i class="icon-file"></i> comments

In this module we have a Comments object. Users can post comments on different Questions to help each other figure out the answer.

#### <i class="icon-file"></i> contact

Anytime there are any issues a Contact object can be created and filed and the administrators can respond to the email or User that creates it. Once an issue is resolved you can close and/or delete the issue.

> **Tip:** Add a description to the README.md file for every application that is added.


----------


Commit Protocol
-------------------

> **Pre-Merge Check List:**

> - Run the "./lint" script to validate your commits pass the pylint check.
> - Add a test infrastructure for your module. Run "python manage.py test" and make sure all tests pass.
> - Create a branch in github using the following nomenclature /user/github_username/feature/feature_name and create a pull-request prior to merging.


