import datetime
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from books.models import Book
from borrowings.models import Borrowing

User = get_user_model()


class BorrowingApiTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.com", password="testpassword"
        )

        self.book_available = Book.objects.create(
            title="Available Book",
            author="Test Author",
            cover="HARD",
            inventory=1,
            daily_fee="2.00",
        )

        self.book_out_of_stock = Book.objects.create(
            title="Out of Stock Book",
            author="Test Author",
            cover="SOFT",
            inventory=0,
            daily_fee="1.50",
        )

        self.list_url = reverse("borrowings:borrowing-list")

    def test_create_borrowing_decreases_inventory(self):
        self.client.force_authenticate(self.user)

        payload = {
            "book": self.book_available.id,
            "expected_return_date": (
                datetime.date.today() + datetime.timedelta(days=5)
            ).isoformat(),
        }

        res = self.client.post(self.list_url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.book_available.refresh_from_db()
        self.assertEqual(self.book_available.inventory, 0)

    def test_cannot_borrow_out_of_stock_book(self):
        self.client.force_authenticate(self.user)

        payload = {
            "book": self.book_out_of_stock.id,
            "expected_return_date": (
                datetime.date.today() + datetime.timedelta(days=5)
            ).isoformat(),
        }

        res = self.client.post(self.list_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_return_book_increases_inventory(self):
        """Testing custom book return method"""
        self.client.force_authenticate(self.user)

        borrowing = Borrowing.objects.create(
            book=self.book_available,
            user=self.user,
            expected_return_date=datetime.date.today() + datetime.timedelta(days=5),
        )
        self.book_available.inventory -= 1
        self.book_available.save()

        return_url = reverse("borrowings:borrowing-return-book", args=[borrowing.id])

        res = self.client.post(return_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.book_available.refresh_from_db()
        self.assertEqual(self.book_available.inventory, 1)
        borrowing.refresh_from_db()
        self.assertIsNotNone(borrowing.actual_return_date)
