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
        """
        Sends an email confirmation to the specified user.
        Args:
            user (User): The user to send the email confirmation to.
        """
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
            uid = urlsafe_base64_encode(from_bytes(user.pk)).decode()
            token_url = f'{protocol}://{domain}{reverse("user:confirm-email", args=[uid, token])}'

            # Send the email
            subject = 'Confirm your email address'
            message = render_to_string(
                'user/confirmation_email.html', {
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

            # Log the email sending result
            logger.info(f"Email confirmation sent to {user.email}")

        except Exception as e:
            logger.error(f"An error occurred while sending email confirmation: {e}")

    @staticmethod
    def confirm_email(token, uid):
        """
        Confirms the email address of the user with the specified token and user ID.

        Args:
            token (str): The email confirmation token.
            uid (str): The user ID.
        """
        try:
            # Validate the token
            try:
                user = User.objects.get(pk=urlsafe_base64_decode(uid).decode())
            except ObjectDoesNotExist:
                logger.error(f"Invalid user ID: {uid}")
                return

            if user.email_confirmation_token != token:
                logger.error(f"Invalid email confirmation token for {uid}")
                return

            # Validate the token expiration
            if timezone.now() > user.email_confirmation_token_expires:
                logger.error(f"Email confirmation token has expired for {uid}")
                return

            # Confirm the email address
            user.email_confirmed = True
            user.save()

            logger.info(f"Email confirmed for {user.email}")

        except Exception as e:
            logger.error(f"An error occurred while confirming email: {e}")