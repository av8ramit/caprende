'''Utils page for the questions Caprende module.'''

from users.models import UserCategoryEnable

def upload_location(instance, filename):
    '''Define the location in the media directory where and how to store the file.'''
    return "question_%s_%s/%s" % (instance.id, instance.course, filename)

def prev_question_url(question, profile):
    '''Return the next question object with the lower index.'''

    try:
        for _ in range(len(question.course.question_set.all())):
            question = question.course.question_set.all().get(course=question.course, index=question.index - 1)
            if UserCategoryEnable.objects.get_category_enable(question.category, profile).enabled:
                return question.get_absolute_url()
            else:
                continue
    except question.DoesNotExist:
        return None

def next_question_url(question, profile):
    '''Return the next question object with the higher index.'''

    try:
        for _ in range(len(question.course.question_set.all())):
            question = question.course.question_set.all().get(course=question.course, index=question.index + 1)
            if UserCategoryEnable.objects.get_category_enable(question.category, profile).enabled:
                return question.get_absolute_url()
            else:
                continue
    except question.DoesNotExist:
        return None
