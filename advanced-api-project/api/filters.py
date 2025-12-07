import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    publication_year = django_filters.NumberFilter()
    publictaion_year__gt = django_filters.NumberFilter(field_name='publication_year', lookup_expr='gt')
    publication_year__lt = django_filters.NumberFilter(field_name='publication_year', lookup_expr='lt')
    author__name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author']