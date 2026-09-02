from rest_framework import serializers
from django.db import transaction
from .models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Borrowing model.
    Handles validation and inventory decrement on creation.
    """

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )
        # These fields are automatically set or managed by the system,
        # so the user shouldn't be able to provide them in a POST request.
        read_only_fields = ("id", "borrow_date", "actual_return_date", "user")

    def validate_book(self, value):
        """
        Validate that the book has available inventory.
        DRF automatically calls validate_<field_name> for specific fields.
        """
        if value.inventory <= 0:
            raise serializers.ValidationError("This book is currently out of stock.")
        return value

    def create(self, validated_data):
        """
        Override the default create method to safely decrease book inventory.
        We use a database transaction to ensure both operations
        (creating borrowing and updating inventory) succeed or fail together.
        """
        with transaction.atomic():
            # Get the book from the validated data
            book = validated_data["book"]

            # Decrease inventory by 1 and save
            book.inventory -= 1
            book.save()

            # Call the standard DRF create method to save the Borrowing
            return super().create(validated_data)
