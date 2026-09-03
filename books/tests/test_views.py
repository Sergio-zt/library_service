from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from books.models import Book

User = get_user_model()


class BookApiTests(APITestCase):
    """
    Test suite for Book API endpoints and permissions.
    """

    def setUp(self):
        # 1. Create a regular user
        self.user = User.objects.create_user(
            email="user@test.com", password="testpassword"
        )

        # 2. Create an admin (staff) user
        self.admin = User.objects.create_superuser(
            email="admin@test.com", password="adminpassword"
        )

        # 3. Create a sample book
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=5,
            daily_fee="2.50",
        )

        self.list_url = reverse("books:book-list")

        # Payload for testing POST requests (creating a book)
        self.new_book_payload = {
            "title": "New API Book",
            "author": "New Author",
            "cover": "SOFT",
            "inventory": 10,
            "daily_fee": "1.99",
        }

    def test_list_books_allowed_for_anyone(self):
        """Test that unauthenticated users can retrieve the books list."""
        res = self.client.get(self.list_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["title"], "Test Book")

    def test_create_book_forbidden_for_regular_user(self):
        """Test that a regular user cannot create a book."""
        # Authenticate as a regular user
        self.client.force_authenticate(self.user)

        # Try to create a book
        res = self.client.post(self.list_url, self.new_book_payload)

        # Expect a 403 Forbidden error because of IsAdminOrReadOnly permission
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_allowed_for_admin(self):
        """Test that an admin user can create a book."""
        # Authenticate as an admin
        self.client.force_authenticate(self.admin)

        # Try to create a book
        res = self.client.post(self.list_url, self.new_book_payload)

        # Expect 201 Created status
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Verify the book was actually added to the database
        book_exists = Book.objects.filter(title="New API Book").exists()
        self.assertTrue(book_exists)
