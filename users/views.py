from rest_framework import generics, permissions
from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """
    Create a new user in the system.
    By default, any unauthenticated user can access this view.
    """

    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    Manage the authenticated user's profile.
    Allows GET (retrieve profile) and PUT/PATCH (update profile).
    """

    serializer_class = UserSerializer

    # Only authenticated users can access this endpoint
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """
        Retrieve and return the authenticated user.
        This overrides the default behavior, which usually looks for an ID in the URL.
        """
        # self.request.user contains the user attached to the provided JWT token
        return self.request.user
