from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import CreateUserView, ManageUserView

app_name = "users"

urlpatterns = [
    # Endpoint to get a new pair of tokens (Access + Refresh) by providing email and password
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # Endpoint to get a new Access token by providing a valid Refresh token
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", CreateUserView.as_view(), name="create"),
    path("me/", ManageUserView.as_view(), name="manage"),
]
