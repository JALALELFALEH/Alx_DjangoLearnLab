from django.shortcuts import render
from .models import Book, Library
from django.views.generic import DetailView
# Create your views here.

def books_list(request):
    books = Book.objects.all()
    context = {'books': books }
    return render(request, 'books/list_books.html', context)

class LibraryDetailView(DetailView):
    model = Library
    context_object_name = 'library'
    template_name = 'library_details.html'