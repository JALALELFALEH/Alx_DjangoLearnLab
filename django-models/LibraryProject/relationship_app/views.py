from django.shortcuts import render
from .models import Library
from .models import Book
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect 
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def list_books(request):
    books = Book.objects.all()
    context = {'books': books }
    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(DetailView):
    model = Library
    context_object_name = 'library'
    template_name = 'relationship_app/library_detail.html'

def register(request):
    if request.method == 'POST' :
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book-list')
        
    else:
        form = UserCreationForm()

    context = {'form' : form}

    return render(request, 'relationship_app/register.html', context)