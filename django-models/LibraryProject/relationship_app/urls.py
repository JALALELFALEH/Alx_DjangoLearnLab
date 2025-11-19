from django.urls import path
from django.contrib.auth import views as auth_views
from .views import list_books, LibraryDetailView, register_view


urlpatterns = [
    path('', list_books, name='book-list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
    path('login/' , auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html')),
    path('register/', register_view, name='register'),
]
