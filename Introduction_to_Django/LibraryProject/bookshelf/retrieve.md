In [31]: books = Book.objects.all()

In [32]: book_description = Book.objects.get(title="1984")

In [33]: print(book_description.title, book_description.author, book_description.publication_year)
1984 George Orwell 1949
