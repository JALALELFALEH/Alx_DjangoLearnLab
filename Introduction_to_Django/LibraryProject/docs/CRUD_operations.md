Create:

In [22]: book = Book.objects.create(
    ...:     title = "1984",
    ...:     author = "George Orwell",
    ...:     publication_year = 1949,
    ...: )

In [24]: Book.objects.all()
Out[24]: <QuerySet [<Book: >, <Book: 1984>]>




Retrieve : 

In [31]: books = Book.objects.all()

In [32]: for book in books:
    ...:     print(book.title, book.author, book.publication_year)
    ...:
  None
1984 George Orwell 1949


Update : 

In [31]: books = Book.objects.all()

In [32]: for book in books:
    ...:     print(book.title, book.author, book.publication_year)
    ...:
  None
1984 George Orwell 1949



Delete : 
In [44]: Book.objects.all()
Out[44]: <QuerySet [<Book: >, <Book: Nineteen Eighty-Four>]>

In [45]: book.delete()
Out[45]: (1, {'bookshelf.Book': 1})

In [46]: Book.objects.all()
Out[46]: <QuerySet [<Book: >]>