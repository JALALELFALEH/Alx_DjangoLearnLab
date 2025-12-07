from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    CustomLoginView,
    PostListView, 
    PostDetailView, 
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    TagPostsListView
)

urlpatterns = [
    # Home page - shows all posts
    path('', PostListView.as_view(), name='home'),
    
    # Post CRUD URLs
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    
    # Comment CRUD URLs
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('post/<int:pk>/comment/add/', views.add_comment, name='add_comment'),
    
    # Search and Tag URLs
    path('search/', views.search_posts, name='search'),
    path('tags/', views.tag_cloud, name='tag_cloud'),
    path('tags/<slug:tag_slug>/', TagPostsListView.as_view(), name='posts_by_tag'),
    
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
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