Create:

In [22]: book = Book.objects.create(
    ...:     title = "1984",
    ...:     author = "George Orwell",
    ...:     publication_year = 1949,
    ...: )

In [24]: Book.objects.all()
Out[24]: <QuerySet [<Book: >, <Book: 1984>]>