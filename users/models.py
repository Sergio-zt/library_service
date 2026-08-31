from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        
        # Normalize the email (lowercase the domain part)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        
        # Hash the password and save the user to the database
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        # Ensure is_staff and is_superuser are True for admins
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model representing a Customer or Staff in the Library System.
    """
    # Remove the username field completely
    username = None
    
    # Make email unique and required
    email = models.EmailField(_('email address'), unique=True)

    # Use email for logging in instead of username
    USERNAME_FIELD = 'email'
    
    # REQUIRED_FIELDS are fields required when creating a superuser via console
    # We leave it empty because email and password are required by default
    REQUIRED_FIELDS = []

    # Assign the custom manager to this model
    objects = UserManager()

    def __str__(self):
        # String representation of the object
        return self.email