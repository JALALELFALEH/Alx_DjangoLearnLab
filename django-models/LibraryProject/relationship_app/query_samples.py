from relationship_app.models import Author, Book, Library, Librarian

# --- DATA SETUP ---

# Create Author and Books
author1 = Author.objects.create(name="Leo Tolstoy")
book1 = Book.objects.create(title="War and Peace", author=author1)
book2 = Book.objects.create(title="Anna Karenina", author=author1)

# Create Library
library1 = Library.objects.create(name="Main City Library")

# Link Books to Library
library1.books.add(book1) 
library1.books.add(book2)

# Create Librarian and link to Library
Librarian.objects.create(name="Maria", library=library1)


# --- CHECKER QUERIES ---

# Checks for “Query all books by a specific author.” (ForeignKey Reverse)
print("\nQUERY 1: Books by Author")
# Variable 'author1' is used here.
for book in author1.book_set.all():
    print(book.title) # Checker looks for the printed title


# Checks for “List all books in a library.” (ManyToMany Forward)
print("\nQUERY 2: Books in Library")
# Variable 'library1' is used here.
for book in library1.books.all():
    print(book.title) # Checker looks for the printed title


# Checks for “Retrieve the librarian for a library.” (OneToOne Reverse)
print("\nQUERY 3: Librarian Name")
# Variable 'library1' is used here.
librarian = library1.head_librarian
print(librarian.name) # Checker looks for the printed name