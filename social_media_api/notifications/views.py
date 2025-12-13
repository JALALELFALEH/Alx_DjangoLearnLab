from rest_framework import viewsets, permissions
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        # Mark all as read when user views notifications
        Notification.objects.filter(recipient=request.user, read=False).update(read=True)
        return super().list(request, *args, **kwargs)