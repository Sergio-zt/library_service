from django.db import models


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
