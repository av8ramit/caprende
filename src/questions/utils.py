'''Utils page for the questions Caprende module.'''

def upload_location(instance, filename):
    '''Define the location in the media directory where and how to store the file.'''
    return "question_%s_%s/%s" % (instance.id, instance.test, filename)

def next_question(question):
    '''Return the next question object with the higher index.'''
    course = question.course
    try:
        return course.question_set.all().get(course=question.course, index=question.index + 1)
    except question.DoesNotExist:
        return None