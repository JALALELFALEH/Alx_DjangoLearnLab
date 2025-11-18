# relationship_app/models.py

from django.db import models

# Checks for the implementation of Author Model
class Author(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

# Checks for the implementation of Book model
class Book(models.Model):
    title = models.CharField(max_length=200)
    # Check 1: ForeignKey. Check 2: on_delete must be models.CASCADE
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    
class Library(models.Model):
    name = models.CharField(max_length=200)
    # Check 1: ManyToManyField. Check 2: related_name must be 'libraries'
    books = models.ManyToManyField(Book, related_name='libraries')
    def __str__(self):
        return self.name
    
# Checks for the implementation of Librarian model
class Librarian(models.Model):
    name = models.CharField(max_length=200)
    # Check 1: OneToOneField. Check 2: on_delete. Check 3: related_name must be 'head_librarian'
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='head_librarian')
    def __str__(self):
        return self.name