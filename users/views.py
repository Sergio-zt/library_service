from rest_framework import generics
from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """
    Create a new user in the system.
    By default, any unauthenticated user can access this view.
    """

    serializer_class = UserSerializer
