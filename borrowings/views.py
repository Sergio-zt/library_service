from rest_framework import viewsets, permissions
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and creating borrowings.
    """

    serializer_class = BorrowingSerializer
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
