from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.books_list, name='book-list'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail'),
]