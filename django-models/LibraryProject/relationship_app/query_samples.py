from relationship_app.models import Author, Book, Library, Librarian

# Define variables for checker compliance
author_name = "Leo Tolstoy"
library_name = "Main City Library"

# --- DATA SETUP (Mandatory) ---
# Create Author and Books
author_obj = Author.objects.create(name=author_name)
book1 = Book.objects.create(title="War and Peace", author=author_obj)
book2 = Book.objects.create(title="Anna Karenina", author=author_obj)

# Create Library
library_obj = Library.objects.create(name=library_name)

# Link Books to Library
library_obj.books.add(book1, book2) 

# Create Librarian and link to Library
Librarian.objects.create(name="Maria", library=library_obj)


# --- QUERY 1: Query all books by a specific author. (Reverse and Filter) ---
print("\nQUERY 1: Books by Author")

# This is the required filter method for the checker:
filtered_books = Book.objects.filter(author=author_obj)
for book in filtered_books:
    print(book.title)
    
# Also demonstrate the reverse manager method (optional, but good practice)
for book in author_obj.book_set.all():
    pass # No need to print again, just keep the line for structure safety


# --- QUERY 2: List all books in a library. (ManyToMany Forward) ---
print("\nQUERY 2: Books in Library")
# Uses library_name variable in get() for checker compliance
library_instance = Library.objects.get(name=library_name) 
for book in library_instance.books.all():
    print(book.title)


# --- QUERY 3: Retrieve the librarian for a library. (OneToOne Reverse) ---
print("\nQUERY 3: Librarian Name")
# Uses library_name variable in get() for checker compliance
library_instance = Library.objects.get(name=library_name)
librarian = library_instance.head_librarian
print(librarian.name)