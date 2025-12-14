"""
Serializers are like translators that convert between:
- Python objects (Django models) and JSON data (API format)
"""

from rest_framework import serializers
from django.utils import timezone
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    This serializer translates Book models to/from JSON.
    
    It handles all fields of the Book model and includes
    validation to make sure the publication year is not in the future.
    """
    
    class Meta:
        model = Book  # Tell it which model to use
        fields = '__all__'  # Include ALL fields from the Book model
    
    def validate_publication_year(self, value):
        """
        Custom validation for publication_year.
        This automatically checks if someone tries to set a future publication year.
        """
        current_year = timezone.now().year
        
        # Check if the publication year is in the future
        if value > current_year:
            raise serializers.ValidationError(
                f'Publication year cannot be in the future! Current year is {current_year}.'
            )
        
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    This serializer translates Author models to/from JSON.
    
    It includes:
    - The author's basic information (name, etc.)
    - A nested list of all books by this author
    """
    
    # This is the magic part! It includes all books by this author
    # 'books' comes from the related_name we set in the Book model
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = '__all__'  # Include all fields + our custom 'books' field