from django.db import models
from django.conf import settings
from books.models import Book


class Borrowing(models.Model):
    """
    Model representing a book borrowing event by a user.
    """

    # Date when the book was borrowed. auto_now_add=True sets it to current date automatically.
    borrow_date = models.DateField(auto_now_add=True)

    # Date when the book is expected to be returned.
    expected_return_date = models.DateField()

    # Date when the book was actually returned.
    # null=True, blank=True because it is empty until the book is returned.
    actual_return_date = models.DateField(null=True, blank=True)

    # ForeignKey to the Book model.
    # related_name='borrowings' allows us to access all borrowings of a book (e.g. book.borrowings.all())
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")

    # ForeignKey to the User model using the AUTH_USER_MODEL setting.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrowings"
    )

    def __str__(self):
        # String representation for admin panel and console
        return f"{self.book.title} borrowed by {self.user.email}"
