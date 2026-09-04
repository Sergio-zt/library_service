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


class Payment(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"

    class TypeChoices(models.TextChoices):
        PAYMENT = "PAYMENT", "Payment"
        FINE = "FINE", "Fine"

    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )
    type = models.CharField(
        max_length=10, choices=TypeChoices.choices, default=TypeChoices.PAYMENT
    )
    borrowing = models.ForeignKey(
        "borrowings.Borrowing", on_delete=models.CASCADE, related_name="payments"
    )
    session_url = models.URLField(
        max_length=500, blank=True, null=True
    )  # Link to Stripe
    session_id = models.CharField(
        max_length=255, blank=True, null=True
    )  # Unique session ID Stripe
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment {self.id} ({self.status}) for borrowing {self.borrowing_id}"
