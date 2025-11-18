from relationship_app.models import Author, Book, Library, Librarian

# --- DATA SETUP (Minimum Required Data) ---

# 1. Author and Books (ForeignKey)
author1 = Author.objects.create(name="Leo Tolstoy")
book1 = Book.objects.create(title="War and Peace", author=author1)
Book.objects.create(title="Anna Karenina", author=author1)

# 2. Library and Books (ManyToMany)
library1 = Library.objects.create(name="Main City Library")
library1.books.add(book1) 

# 3. Librarian and Library (OneToOne)
Librarian.objects.create(name="Maria", library=library1)


# --- QUERY 1: Books by a specific author (ForeignKey Reverse) ---
# Goal: Find the books that belong to 'author1'.
print("\n--- QUERY 1: Books by Leo Tolstoy ---")
leo = Author.objects.get(name="Leo Tolstoy")
for book in leo.book_set.all():
    print(book.title)


# --- QUERY 2: List all books in a library (ManyToMany Forward) ---
# Goal: Find all books linked to 'library1'.
print("\n--- QUERY 2: Books in Main City Library ---")
main_lib = Library.objects.get(name="Main City Library")
for book in main_lib.books.all():
    print(book.title)


# --- QUERY 3: Retrieve the librarian for a library (OneToOne Reverse) ---
# Goal: Find the librarian linked to 'library1'.
print("\n--- QUERY 3: Librarian for Main City Library ---")
main_lib = Library.objects.get(name="Main City Library")
librarian = main_lib.head_librarian
print(librarian.name)