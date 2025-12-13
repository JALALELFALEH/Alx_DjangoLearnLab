from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.ReadOnlyField(source='actor.username')
    post_title = serializers.ReadOnlyField(source='target_post.title', default=None)
    
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'actor_username', 'verb', 
                'target_post', 'post_title', 'target_comment', 'read', 'created_at']
        read_only_fields = ['recipient', 'actor', 'created_at']