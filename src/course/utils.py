'''Utils page for the course Caprende module.'''

def upload_location(instance, filename):
    '''Define the location in the media directory where and how to store the file.'''
    return "course/%s/%s" % (instance.name, filename)



