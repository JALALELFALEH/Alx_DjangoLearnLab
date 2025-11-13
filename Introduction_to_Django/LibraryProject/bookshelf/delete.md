In [44]: Book.objects.all()
Out[44]: <QuerySet [<Book: >, <Book: Nineteen Eighty-Four>]>

In [45]: book.delete()
Out[45]: (1, {'bookshelf.Book': 1})

In [46]: Book.objects.all()
Out[46]: <QuerySet [<Book: >]>