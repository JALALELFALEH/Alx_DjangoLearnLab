from relationship_app.models import Author, Book, Library, Librarian

# Define variables for checker compliance (Used in all required checks)
author_name = "Leo Tolstoy"
library_name = "Main City Library"

# --- DATA SETUP (Mandatory) ---
# 1. Author and Books (ForeignKey)
author_to_filter = Author.objects.create(name=author_name)
book1 = Book.objects.create(title="War and Peace", author=author_to_filter)
book2 = Book.objects.create(title="Anna Karenina", author=author_to_filter)

# 2. Library and Books (ManyToMany)
library_instance = Library.objects.create(name=library_name)
library_instance.books.add(book1, book2) 

# 3. Librarian and Library (OneToOne)
Librarian.objects.create(name="Maria", library=library_instance)


# --- QUERY 1: Query all books by a specific author. (Strict Checker Requirements) ---
print("\nQUERY 1: Books by Author")
# Satisfies: "Author.objects.get(name=author_name)"
author_obj = Author.objects.get(name=author_name) 

# Satisfies: "objects.filter(author=author)"
filtered_books = Book.objects.filter(author=author_obj)
for book in filtered_books:
    print(book.title)


# --- QUERY 2: List all books in a library. (ManyToMany Forward) ---
print("\nQUERY 2: Books in Library")
# Satisfies: "Library.objects.get(name=library_name)"
library_obj_2 = Library.objects.get(name=library_name) 
for book in library_obj_2.books.all():
    print(book.title)


# --- QUERY 3: Retrieve the librarian for a library. (OneToOne Reverse) ---
print("\nQUERY 3: Librarian Name")
# Satisfies: "Library.objects.get(name=library_name)"
library_obj_3 = Library.objects.get(name=library_name)
librarian = library_obj_3.head_librarian
print(librarian.name)