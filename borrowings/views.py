from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and creating borrowings.
    """

    serializer_class = BorrowingSerializer
    queryset = Borrowing.objects.all()
    # Only authenticated users can interact with borrowings
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        Filter the queryset based on user roles and query parameters.
        """
        queryset = Borrowing.objects.all()

        # 1. Filter by current user (if they are not a staff member)
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        # 2. Filter by is_active (from URL parameters: ?is_active=True)
        is_active = self.request.query_params.get("is_active")
        if is_active is not None:
            if is_active.lower() == "true":
                # Active means actual_return_date is still empty
                queryset = queryset.filter(actual_return_date__isnull=True)
            elif is_active.lower() == "false":
                # Inactive means it has been returned
                queryset = queryset.filter(actual_return_date__isnull=False)

        # 3. Filter by user_id (from URL parameters: ?user_id=1)
        # Only staff members are allowed to filter by other user's IDs
        user_id = self.request.query_params.get("user_id")
        if user_id is not None and self.request.user.is_staff:
            queryset = queryset.filter(user_id=user_id)

        return queryset

    def perform_create(self, serializer):
        """
        Automatically assign the logged-in user to the borrowing.
        """
        # self.request.user contains the currently authenticated user
        serializer.save(user=self.request.user)

    @action(
        detail=True,
        methods=["POST"],
        url_path="return",
    )
    def return_book(self, request, pk=None):
        """
        Custom action to return a borrowed book.
        Sets actual_return_date to today and increases book inventory by 1.
        """
        # Retrieve the specific borrowing instance using its ID (pk)
        borrowing = self.get_object()

        # Check if the book has already been returned
        if borrowing.actual_return_date is not None:
            return Response(
                {"detail": "This book has already been returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Use atomic transaction to ensure data integrity
        with transaction.atomic():
            # Set the return date to today
            borrowing.actual_return_date = timezone.now().date()
            borrowing.save()

            # Increase the book's inventory by 1
            book = borrowing.book
            book.inventory += 1
            book.save()

        # Return a success message
        return Response(
            {"detail": "Book returned successfully!"}, status=status.HTTP_200_OK
        )
