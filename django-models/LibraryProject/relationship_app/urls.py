from django.urls import path
from django.contrib.auth import views as v
from . import views


urlpatterns = [
    path('', views.list_books, name='book-list'),
    path('library/<int:pk>/', viewsLibraryDetailView.as_view(), name='library-detail'),
    path('login/' , v.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', v.LogoutView.as_view(template_name='relationship_app/logout.html')),
    path('register/', views.register, name='register'),
]
