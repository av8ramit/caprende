'''Utils page for the questions Caprende module.'''

def upload_location(instance, filename):
    '''Define the location in the media directory where and how to store the file.'''
    return "question_%s_%s/%s" % (instance.id, instance.test, filename)
