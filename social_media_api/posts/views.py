from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):  # This must be PostViewSet
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
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        
        # Check if user already liked this post
        if Like.objects.filter(user=request.user, post=post).exists():
            return Response({'message': 'You already liked this post'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create like
        like = Like.objects.create(user=request.user, post=post)
        
        # Create notification (we'll implement this later)
        # self.create_notification(post.author, request.user, 'like', post=post)
        
        return Response({'message': 'Post liked successfully'}, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({'message': 'Post unliked successfully'})
        except Like.DoesNotExist:
            return Response({'message': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        post = self.get_object()
        likes = post.likes.all()
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)
    
    def create_notification(self, recipient, actor, verb, post=None, comment=None):
        # This will be implemented in notifications
        pass

class CommentViewSet(viewsets.ModelViewSet):  # This must be CommentViewSet
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwner]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FeedView(APIView):  # This must be FeedView
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Get users that the current user is following
        following_users = request.user.following.all()
        
        # Get posts from followed users
        feed_posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        
        # Apply pagination
        page = self.paginate_queryset(feed_posts)
        if page is not None:
            serializer = PostSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = PostSerializer(feed_posts, many=True)
        return Response(serializer.data)
    
    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            from rest_framework.pagination import PageNumberPagination
            self._paginator = PageNumberPagination()
            self._paginator.page_size = 10
        return self._paginator
    
    def paginate_queryset(self, queryset):
        return self.paginator.paginate_queryset(queryset, self.request, view=self)
    
    def get_paginated_response(self, data):
        return self.paginator.get_paginated_response(data)