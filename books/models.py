from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Book(models.Model):
    """
    Model representing a book in the library inventory.
    """

    # Define an Enum-like class for the cover type choices
    class CoverType(models.TextChoices):
        HARD = "HARD", "Hardcover"
        SOFT = "SOFT", "Softcover"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    # Use the CoverType choices for this field
    cover = models.CharField(
        max_length=4, choices=CoverType.choices, default=CoverType.HARD
    )

    # Inventory must be a positive integer (cannot be negative)
    inventory = models.PositiveIntegerField(
        help_text="The number of this specific book available now in the library"
    )

    # Daily fee in $USD.
    # max_digits=5 and decimal_places=2 allows prices up to 999.99
    # MinValueValidator ensures the fee cannot be negative
    daily_fee = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )

    def __str__(self):
        # String representation of the object
        return f"{self.title} by {self.author}"
