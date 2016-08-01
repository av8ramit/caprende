'''Models page for the notifications Caprende module.'''
# pylint: disable=no-member

from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.

class NotificationQuerySet(models.query.QuerySet):
    '''QuerySet for the Notification class.'''

    def by_user(self, recipient):
        '''Return notifications by recipient.'''
        return self.filter(recipient=recipient)

    def mark_all_read(self, recipient):
        '''Mark all notifications by recipient as read.'''
        qs = self.unread().get_user(recipient)
        qs.update(read=True)

    def mark_all_unread(self, recipient):
        '''Mark all notifications by recipient as unread.'''
        qs = self.read().get_user(recipient)
        qs.update(read=False)

    def unread(self):
        '''Return all notifications that are unread.'''
        return self.filter(read=False)

    def read(self):
        '''Return all notifications that are read.'''
        return self.filter(read=True)

    def recent(self):
        '''Return the most recent notifications that are unread.'''
        return self.unread()[:5]


class NotificationManager(models.Manager):
    '''ModelManager for the Notification class.'''

    def get_queryset(self):
        '''Get the original QuerySet of Notifications.'''
        return NotificationQuerySet(self.model, using=self._db)

    def all_unread(self, user):
        '''Return all unread notifications by user.'''
        return self.get_queryset().by_user(user).unread()

    def all_read(self, user):
        '''Return all read notifications by user.'''
        return self.get_queryset().by_user(user).read()

    def all_for_user(self, user):
        '''Return all notifications for a user.'''
        return self.get_queryset().by_user(user)

    def get_recent_for_user(self, user, num=5):
        '''Return a recent amount of notifications for a user.'''
        return self.get_queryset().by_user(user)[:num]

    def create(self, text, user, link):
        '''Create and return a Notification object.'''

        notification = self.model(
            text=text,
            recipient=user,
            read=False,
            link=link
        )
        notification.save(using=self._db)
        return notification


class Notification(models.Model):
    '''Base model for a Notification for Caprende.'''

    text = models.TextField(
        max_length=1000,
    )
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL)
    read = models.BooleanField(
        default=False
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        auto_now=False
    )
    link = models.CharField(
        max_length=350,
        null=True,
        blank=True
    )
    objects = NotificationManager()

    class Meta:
        '''Meta class invocation for Notification class.'''
        ordering = ['-timestamp']

    def __unicode__(self):
        return self.text

    @property
    def get_link(self):
        '''Get the link to check the notification as read and then go to the link.'''

        if self.link is None:
            link = reverse("notifications_all")
        else:
            link = self.link

        context = {
            "text": self.text,
            "verify_read": reverse("notifications_read", kwargs={"id": self.id}),
            "target_url": link,
        }
        return "<a href='%(verify_read)s?next=%(target_url)s'>%(text)s</a>" % context

