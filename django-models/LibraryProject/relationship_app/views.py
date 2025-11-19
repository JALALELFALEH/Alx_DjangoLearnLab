from django.shortcuts import render
from .models import Library
from .models import Book
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect 
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test

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

def is_admin(user):
    return user.is_athenticated and user.userprofile.role == 'ADMIN'

def is_librarian(user):
    return user.is_authenticated and user.userprofile.role == 'LIBRARIAN'

def is_member(user):
    return user.is_authenticated and user.userprofile.role == 'MEMBER'

@user_passes_test(is_admin, login_url='/login/')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html', {})

@user_passes_test(is_librarian, login_url='/login/')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html', {})

@user_passes_test(is_member, login_url='/login/')
def member_view(request):
    return render(request, 'relationship_app/member_view.html', {})