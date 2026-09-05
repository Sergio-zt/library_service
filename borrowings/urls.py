from django.urls import path, include
from rest_framework.routers import DefaultRouter
from borrowings.views import BorrowingViewSet

# Create a router instance
router = DefaultRouter()

# Register our BorrowingViewSet with the router
# This automatically generates all standard CRUD URLs and our custom 'return' action
router.register(r"borrowings", BorrowingViewSet)

# app_name helps Django namespace the URLs
app_name = "borrowings"

urlpatterns = [
    # Include all generated URLs from the router
    path("", include(router.urls)),
]
