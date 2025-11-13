In [31]: books = Book.objects.all()

In [32]: for book in books:
    ...:     print(book.title, book.author, book.publication_year)
    ...:
  None
1984 George Orwell 1949