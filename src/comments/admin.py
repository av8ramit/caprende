'''Admin page for the comments Caprende module.'''

from django.contrib import admin

from .models import Comment

# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    '''Admin page for the comments Caprende module.'''

    list_display = ['__unicode__', 'text']

    class Meta:
        '''Meta class invocation for Comment.'''
        model = Comment


admin.site.register(Comment, CommentAdmin)
