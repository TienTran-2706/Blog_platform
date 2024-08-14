import logging
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from charset_normalizer import from_bytes
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from blog_platform import settings
from django.utils.encoding import force_bytes, force_str
from user.models import User

logger = logging.getLogger(__name__)

class EmailService:
    """
    A service class responsible for sending email confirmations to users.

    Attributes:
        None

    Methods:
        send_confirmation_email(user): Sends an email confirmation to the specified user.
        confirm_email(token, uid): Confirms the email address of the user with the specified token and user ID.
    """
    @staticmethod
    def send_confirmation_email(user):
        try:
            # Generate a secure random token
            token = get_random_string(length=32)
            user.email_confirmation_token = token
            user.email_confirmation_token_expires = timezone.now() + timezone.timedelta(days=1)
            user.save()

            # Get the current site configuration
            try:
                current_site = get_current_site(None)
            except ImproperlyConfigured as e:
                logger.error(f"Failed to get current site configuration: {e}")
                return

            # Generate the email confirmation link
            protocol = current_site.scheme or 'http'
            domain = current_site.domain
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token_url = f'{protocol}://{domain}{reverse("user:confirm_email", args=[uid, token])}'

            # Send the email
            subject = 'Confirm your email address'
            message = render_to_string(
                'user/confirm_email.html', {
                    'user': user,
                    'domain': domain,
                    'token': token,
                    'uid': uid,
                    'token_url': token_url,
                }
            )
            plain_message = strip_tags(message)
            try:
                send_mail(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    html_message=message,
                )
            except Exception as e:
                logger.error(f"Failed to send email confirmation to {user.email}: {e}")
                return
        except Exception as e:
            logger.error(f"An error occurred while sending email confirmation: {e}")

    @staticmethod
    def confirm_email(token, uid):
        try:
            # Decode the token
            uid = force_str(urlsafe_base64_decode(uid))
            # Get the user by the decoded UID
            user = User.objects.get(pk=uid)
            # Confirm the user
            if user.email_confirmation_token == token and user.email_confirmation_token_expires > timezone.now():
                # Confirm the user
                user.is_email_confirmed = True
                # Clear the token
                user.email_confirmation_token = None
                user.email_confirmation_token_expires = None
                user.save()
                return True
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            # Handle errors, such as invalid token or user not found
            return False