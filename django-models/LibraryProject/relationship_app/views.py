from django.shortcuts import render
from .models import Library
from .models import Book
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect 
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required

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

@permission_required('relationship_app.can_add_book', login_url='/login/')
def book_add(request):
    """View to handle adding a book, restricted by 'can_add_book' permission."""
    # In a real app, this would handle a form submission (POST)
    message = "You have permission to ADD a book."
    return render(request, 'relationship_app/permission_test.html', {'message': message})

@permission_required('relationship_app.can_change_book', login_url='/login/')
def book_edit(request, pk):
    """View to handle editing a book, restricted by 'can_change_book' permission."""
    book = get_object_or_404(Book, pk=pk)
    # In a real app, this would handle a form submission (POST)
    message = f"You have permission to EDIT book ID {pk}: {book.title}"
    return render(request, 'relationship_app/permission_test.html', {'message': message})

@permission_required('relationship_app.can_delete_book', login_url='/login/')
def book_delete(request, pk):
    """View to handle deleting a book, restricted by 'can_delete_book' permission."""
    book = get_object_or_404(Book, pk=pk)
    # In a real app, this would delete the object after confirmation
    message = f"You have permission to DELETE book ID {pk}: {book.title}"
    return render(request, 'relationship_app/permission_test.html', {'message': message})