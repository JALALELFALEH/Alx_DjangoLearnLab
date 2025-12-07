"""
Unit tests for API endpoints.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Author, Book


class BookAPITests(APITestCase):
    """Test cases for Book API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2023,
            author=self.author
        )
        self.client = APIClient()
    
    def test_get_all_books(self):
        """Test retrieving all books."""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    def test_get_single_book(self):
        """Test retrieving a single book."""
        response = self.client.get(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')
    
    def test_create_book_unauthenticated(self):
        """Test creating a book without authentication."""
        data = {
            'title': 'New Book',
            'publication_year': 2024,
            'author': self.author.id
        }
        response = self.client.post('/api/books/create/', data)
        self.assertIn(response.status_code, 
                     [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_create_book_authenticated(self):
        """Test creating a book with authentication."""
        # Login using self.client.login
        self.client.login(username='testuser', password='testpass')
        data = {
            'title': 'My Book',
            'publication_year': 2024,
            'author': self.author.id
        }
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'My Book')
    
    def test_filter_books_by_title(self):
        """Test filtering books by title."""
        response = self.client.get('/api/books/?title=test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    def test_search_books(self):
        """Test searching books."""
        response = self.client.get('/api/books/?search=test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    def test_order_books(self):
        """Test ordering books."""
        response = self.client.get('/api/books/?ordering=-publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    def test_login_functionality(self):
        """Test login functionality."""
        # Test login works
        login_success = self.client.login(username='testuser', password='testpass')
        self.assertTrue(login_success)
        
        # Test logout works
        self.client.logout()
        login_failed = self.client.login(username='testuser', password='wrongpass')
        self.assertFalse(login_failed)