"""
Simple tests for the API.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Author, Book


class SimpleAPITests(TestCase):
    """Basic tests for the Book API."""
    
    def setUp(self):
        """Create test data before each test."""
        # Create a user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        
        # Create an author
        self.author = Author.objects.create(name="Test Author")
        
        # Create a book
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2023,
            author=self.author
        )
    
    # Test 1: Can view books
    def test_can_view_books(self):
        """Test that anyone can see the book list."""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, 200)
    
    # Test 2: Can view single book  
    def test_can_view_single_book(self):
        """Test that anyone can see a single book."""
        response = self.client.get(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, 200)
    
    # Test 3: Cannot create without login
    def test_cannot_create_without_login(self):
        """Test that you need to be logged in to create books."""
        data = {
            'title': 'New Book',
            'publication_year': 2024,
            'author': self.author.id
        }
        response = self.client.post('/api/books/create/', data)
        self.assertIn(response.status_code, [401, 403])
    
    # Test 4: Can create with login
    def test_can_create_with_login(self):
        """Test that logged in users can create books."""
        self.client.force_login(self.user)
        data = {
            'title': 'My Book',
            'publication_year': 2024,
            'author': self.author.id
        }
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, 201)
    
    # Test 5: Filtering works
    def test_filtering_works(self):
        """Test that filtering by title works."""
        response = self.client.get('/api/books/?title=test')
        self.assertEqual(response.status_code, 200)
    
    # Test 6: Searching works
    def test_searching_works(self):
        """Test that searching works."""
        response = self.client.get('/api/books/?search=test')
        self.assertEqual(response.status_code, 200)
    
    # Test 7: Ordering works
    def test_ordering_works(self):
        """Test that ordering works."""
        response = self.client.get('/api/books/?ordering=-publication_year')
        self.assertEqual(response.status_code, 200)