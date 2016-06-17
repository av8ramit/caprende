'''Models page for the comments Caprende module.'''
# pylint: disable=no-member

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models

from questions.models import Question
from users.models import MyUser

# Create your models here.

class CommentManager(models.Manager):
    '''ModelManager for the Comment class.'''

    def all(self):
        '''Return all the comments that are parents.'''
        return super(CommentManager, self).filter(active=True).filter(parent=None)

    def create_comment(self, user=None, text=None, question=None, parent=None):
        '''Create a comment.'''

        if not user:
            raise ValueError("Must include a user when adding a Comment.")

        comment = self.model(
            user=user,
            text=text,
            question=question,
            parent=parent,
        )
        if parent is not None:
            comment.parent = parent
        comment.save(using=self._db)
        return comment

class Comment(models.Model):
    '''Base model for a comment for Caprende.'''

    user = models.ForeignKey(MyUser)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
    )
    question = models.ForeignKey(
        Question,
        null=True,
        blank=True,
    )
    text = models.TextField()
    updated = models.DateTimeField(
        auto_now=True,
        auto_now_add=False,
    )
    timestamp = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
    )
    active = models.BooleanField(default=True)

    objects = CommentManager()

    class Meta:
        '''Meta class invocation for Comment class.'''
        ordering = ['-timestamp']

    def __unicode__(self):
        return self.text + " | " + self.user.username

    def get_comment(self):
        '''Return the text of the comment.'''
        return self.text

    def is_child(self):
        '''Returns a boolean value is the comment is a child or not.'''
        return self.parent is not None

    def get_children(self):
        '''Returns all the children of the comment.'''

        if self.is_child():
            return None
        else:
            return Comment.objects.filter(parent=self)

    def get_absolute_url(self):
        '''Returns the URL of the comment thread.'''
        return reverse("comment_thread", kwargs={"comment_id": self.id})

