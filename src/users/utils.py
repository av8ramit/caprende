'''Forms page for the users Caprende module.'''

def upload_location(instance, filename):
    '''Define the location in the media directory where and how to store the file.'''
    return "%s/%s" % (instance.username, filename)
