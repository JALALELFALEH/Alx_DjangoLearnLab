from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('follow/', views.FollowUserView.as_view(), name='follow'),
    path('unfollow/', views.UnfollowUserView.as_view(), name='unfollow'),
    path('follow/<int:user_id>/', views.FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', views.UnfollowUserView.as_view(), name='unfollow-user'),
    path('profile/<str:username>/', views.UserProfileDetailView.as_view(), name='user-profile'),
]