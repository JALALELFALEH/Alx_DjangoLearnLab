from django.urls import path
from django.contrib.auth import views 
from .views import list_books, LibraryDetailView, register, admin_view, librarian_view, member_view, add_book, edit_book, delete_book


urlpatterns = [
    path('', list_books, name='book-list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
    path('login/' , views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(template_name='relationship_app/logout.html')),
    path('register/', register, name='register'),
    path('admin_area/', admin_view, name='admin_view'),
    path('librarian_desk/', librarian_view, name='librarian_view'),
    path('member_area/', member_view, name='member_view'),
    path('add_book/', add_book, name='book_add'),
    path('edit_book/', edit_book, name='book_edit'),
    path('delete_book/', delete_book, name='book_delete'),
]
