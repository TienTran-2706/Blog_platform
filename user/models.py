from datetime import timezone
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from base.base_model import BaseModel
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class User(BaseModel, AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='media')
    bio = models.TextField()

    is_email_confirmed = models.BooleanField(default=False)
    email_confirmation_token = models.CharField(max_length=255, blank=True, null=True)
    email_confirmation_sent_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = BaseUserManager()

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
        return urlsafe_base64_encode(force_bytes(uid)).decode()

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
    