from django.db import models
from django.conf import settings

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
    ]
    
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='actions')
    verb = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    target_post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, null=True, blank=True, related_name='post_notifications')
    target_comment = models.ForeignKey('posts.Comment', on_delete=models.CASCADE, null=True, blank=True, related_name='comment_notifications')
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.actor.username} {self.verb} - {self.recipient.username}"