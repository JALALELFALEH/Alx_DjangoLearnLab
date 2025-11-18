from django.shortcuts import render
from .models import Library
from .models import Book
from django.views.generic import DetailView
# Create your views here.

def books_list(request):
    books = Book.objects.all()
    context = {'books': books }
    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(DetailView):
    model = Library
    context_object_name = 'library'
    template_name = 'relationship_app/library_details.html'