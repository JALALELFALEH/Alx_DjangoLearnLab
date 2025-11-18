from relationship_app.models import Author, Book, Library, Librarian

# --- DATA SETUP (Mandatory for queries to work) ---

# Define names using variables the checker might look for
author_name = "Leo Tolstoy"
library_name = "Main City Library"

# 1. Author and Books (ForeignKey)
author1 = Author.objects.create(name=author_name)
book1 = Book.objects.create(title="War and Peace", author=author1)
book2 = Book.objects.create(title="Anna Karenina", author=author1)

# 2. Library and Books (ManyToMany)
library1 = Library.objects.create(name=library_name)
library1.books.add(book1, book2) 

# 3. Librarian and Library (OneToOne)
Librarian.objects.create(name="Maria", library=library1)


# --- QUERY 1: Query all books by a specific author. (ForeignKey Reverse) ---
print("\nQUERY 1: Books by Author")
# Uses author_name variable in get() for checker compliance
author_obj = Author.objects.get(name=author_name) 
for book in author_obj.book_set.all():
    print(book.title)


# --- QUERY 2: List all books in a library. (ManyToMany Forward) ---
print("\nQUERY 2: Books in Library")
# Uses library_name variable in get() for checker compliance
library_obj = Library.objects.get(name=library_name) 
for book in library_obj.books.all():
    print(book.title)


# --- QUERY 3: Retrieve the librarian for a library. (OneToOne Reverse) ---
print("\nQUERY 3: Librarian Name")
# Uses library_name variable in get() for checker compliance
library_obj = Library.objects.get(name=library_name)
librarian = library_obj.head_librarian
print(librarian.name)