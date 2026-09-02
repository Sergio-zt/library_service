from rest_framework import serializers
from django.contrib.auth import get_user_model

# get_user_model() is the safest way to reference our custom User model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User object.
    Handles user creation and password hashing.
    """

    class Meta:
        model = User
        fields = ("id", "email", "password", "first_name", "last_name", "is_staff")

        # read_only_fields cannot be modified by the user
        read_only_fields = ("id", "is_staff")

        # extra_kwargs allows us to set specific rules for fields
        extra_kwargs = {
            "password": {
                "write_only": True,  # Password will not be returned in the API response
                "min_length": 5,  # Basic validation for password length
            }
        }

    def create(self, validated_data):
        """
        Override the default create method to use our custom
        create_user method, which correctly hashes the password.
        """
        return User.objects.create_user(**validated_data)
