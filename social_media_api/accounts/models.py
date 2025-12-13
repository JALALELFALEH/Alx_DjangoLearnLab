from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    # We have both followers and following fields
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    
    def __str__(self):
        return self.username
    
    def follow(self, user):
        """Follow a user"""
        if user != self and user not in self.following.all():
            self.following.add(user)
            return True
        return False
    
    def unfollow(self, user):
        """Unfollow a user"""
        if user in self.following.all():
            self.following.remove(user)
            return True
        return False
    
    def is_following(self, user):
        """Check if following a user"""
        return user in self.following.all()