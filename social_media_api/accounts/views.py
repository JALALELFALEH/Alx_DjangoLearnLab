from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, FollowSerializer, UserProfileSerializer

# Register
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

# Login
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            return Response({'error': 'Invalid credentials'}, status=400)
        return Response(serializer.errors, status=400)

# Profile
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

# Follow - using GenericAPIView
class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowSerializer
    
    def post(self, request, user_id=None):
        # Get user_id from URL parameter or request data
        target_user_id = user_id if user_id else request.data.get('user_id')
        
        if not target_user_id:
            return Response({'error': 'User ID is required'}, status=400)
        
        user_to_follow = get_object_or_404(CustomUser, id=target_user_id)
        
        if request.user == user_to_follow:
            return Response({'error': 'You cannot follow yourself'}, status=400)
        
        if request.user.follow(user_to_follow):
            return Response({'message': f'Now following {user_to_follow.username}'})
        else:
            return Response({'message': f'Already following {user_to_follow.username}'})

# Unfollow - using GenericAPIView
class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowSerializer
    
    def post(self, request, user_id=None):
        # Get user_id from URL parameter or request data
        target_user_id = user_id if user_id else request.data.get('user_id')
        
        if not target_user_id:
            return Response({'error': 'User ID is required'}, status=400)
        
        user_to_unfollow = get_object_or_404(CustomUser, id=target_user_id)
        
        if request.user.unfollow(user_to_unfollow):
            return Response({'message': f'Unfollowed {user_to_unfollow.username}'})
        else:
            return Response({'message': f'Not following {user_to_unfollow.username}'})

# User profile detail
class UserProfileDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'username'