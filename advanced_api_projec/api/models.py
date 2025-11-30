"""
Models define the structure of our database.
Think of them as templates for storing different types of information.
"""

from django.db import models

class Author(models.Model):
    """
    Represents an Author in our library system.
    
    Each Author can have multiple Books (one-to-many relationship).
    For example: J.K. Rowling can have many Harry Potter books.
    
    Fields:
    - name: The author's full name
    - created_at: Auto-set when author is created
    - updated_at: Auto-updated when author is modified
    """
    
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Represents a Book in our library system.
    
    Each Book is written by one Author (many-to-one relationship).
    For example: "Harry Potter" book belongs to J.K. Rowling.
    
    Fields:
    - title: The book's title
    - publication_year: Year the book was published
    - author: Link to the Author who wrote this book
    - created_at/updated_at: Automatic timestamps
    
    Relationship Explanation:
    - ForeignKey creates a link from Book to Author
    - related_name='books' allows us to do: author.books.all() to get all books by an author
    - on_delete=CASCADE means: if author is deleted, all their books are also deleted
    """
    
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,  # Delete books when author is deleted
        related_name='books'  # This allows: author.books.all()
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'"{self.title}" by {self.author.name}'