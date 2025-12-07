from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    CustomLoginView, 
    PostListView, 
    PostDetailView, 
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)

urlpatterns = [
    # Home page - shows all posts
    path('', PostListView.as_view(), name='home'),
    
    # Post CRUD URLs - Fixed according to task requirements
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    
    # Profile URLs
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    
    # Password Reset URLs
    path('password-reset/', 
            auth_views.PasswordResetView.as_view(template_name='blog/password_reset.html'), 
            name='password_reset'),
    path('password-reset/done/', 
            auth_views.PasswordResetDoneView.as_view(template_name='blog/password_reset_done.html'), 
            name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
            auth_views.PasswordResetConfirmView.as_view(template_name='blog/password_reset_confirm.html'), 
            name='password_reset_confirm'),
    path('password-reset-complete/', 
            auth_views.PasswordResetCompleteView.as_view(template_name='blog/password_reset_complete.html'), 
            name='password_reset_complete'),
]