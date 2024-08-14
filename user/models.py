from django.utils import timezone
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from base.base_model import BaseModel
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Custom user model manager where email is the unique identifier for authentication."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class User(BaseModel, AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='media', blank=True)
    bio = models.TextField(blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_email_confirmed = models.BooleanField(default=False)
    email_confirmation_token = models.CharField(max_length=255, blank=True, null=True)
    email_confirmation_sent_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


    def generate_confirmation_token(self):
        """
        Generates a URL-safe base64 encoded token for email_confirmation_token field.
        """
        uid = uuid.uuid4().hex
        return urlsafe_base64_encode(force_bytes(uid))

    def save(self, *args, **kwargs):
        """
        Saves the current user instance.

        If the user has not been confirmed and does not have an email confirmation token,
        generates a new token before saving.
        """
        if self.email_confirmation_token is None and not self.is_email_confirmed:
            self.email_confirmation_token = self.generate_confirmation_token()
            self.email_confirmation_sent_at = timezone.now()
        super().save(*args, **kwargs)
