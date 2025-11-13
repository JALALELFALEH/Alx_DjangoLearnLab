In [33]: books = Book.objects.all()

In [34]: book = Book.objects.get(title="1984")

In [35]: print(book)
1984

In [36]: print(book.author)
George Orwell

In [37]: print(book.publication_year)
1949

In [38]: book.title = "Nineteen Eighty-Four"

In [39]: book.save()

In [40]: Book.objects.all()
Out[41]: <QuerySet [<Book: >, <Book: Nineteen Eighty-Four>]>