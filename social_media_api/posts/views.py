from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwner]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'content']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwner]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Add Like view using GenericAPIView
class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        # Use get_object_or_404 as specified
        post = get_object_or_404(Post, pk=pk)
        
        # Use get_or_create as specified
        like, created = Like.objects.get_or_create(
            user=request.user, 
            post=post
        )
        
        if created:
            # Create notification
            from notifications.models import Notification
            from django.contrib.contenttypes.models import ContentType
            
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='like',
                content_type=ContentType.objects.get_for_model(post),
                object_id=post.id,
                target=post
            )
            
            return Response({'message': 'Post liked successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'You already liked this post'}, status=status.HTTP_400_BAD_REQUEST)

class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({'message': 'Post unliked successfully'})
        except Like.DoesNotExist:
            return Response({'message': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)

class FeedView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    
    def get_queryset(self):
        # Get users that the current user is following
        following_users = self.request.user.following.all()
        
        # Get posts from followed users
        return Post.objects.filter(author__in=following_users).order_by('-created_at')