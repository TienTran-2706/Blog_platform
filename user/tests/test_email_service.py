from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils import timezone
from django.core.mail import send_mail
from user.models import User
from user.services import EmailService

class EmailServiceTest(TestCase):

    @patch('user.services.send_mail')
    @patch('user.services.get_current_site')
    def test_send_confirmation_email(self, mock_get_current_site, mock_send_mail):
        # Set up the mock for current site
        mock_get_current_site.return_value = MagicMock(domain='example.com', scheme='http')

        # Create a mock user
        user = User(username='testuser', email='test@example.com')
        user.email_confirmation_token = 'dummy-token'
        user.email_confirmation_token_expires = timezone.now() + timezone.timedelta(days=1)
        user.save = MagicMock()  # Mock the save method

        # Call the method to be tested
        EmailService.send_confirmation_email(user)

        # Check if send_mail was called
        mock_send_mail.assert_called_once()

        # Ensure that save was called on the user
        user.save.assert_called_once()

    @patch('user.models.User.objects.get')
    def test_confirm_email(self, mock_get_user):
        # Set up the mock user
        user = User(username='testuser', email='test@example.com')
        user.email_confirmation_token = 'dummy-token'
        user.email_confirmation_token_expires = timezone.now() + timezone.timedelta(days=1)
        user.save = MagicMock()
        mock_get_user.return_value = user

        # Encode the user ID
        uid = urlsafe_base64_encode(str(user.pk).encode('utf-8'))
        token = 'dummy-token'

        # Call the method to be tested
        EmailService.confirm_email(token, uid)

        # Check if the user’s email is confirmed
        self.assertTrue(user.is_email_confirmed)
        user.save.assert_called_once()

    @patch('user.models.User.objects.get')
    def test_confirm_email_invalid_token(self, mock_get_user):
        # Set up the mock user
        user = User(username='testuser', email='test@example.com')
        user.email_confirmation_token = 'correct-token'
        user.email_confirmation_token_expires = timezone.now() + timezone.timedelta(days=1)
        user.save = MagicMock()
        mock_get_user.return_value = user

        # Encode the user ID
        uid = urlsafe_base64_encode(str(user.pk).encode('utf-8'))
        invalid_token = 'wrong-token'

        # Call the method to be tested
        result = EmailService.confirm_email(invalid_token, uid)

        # Check if the user’s email is not confirmed
        self.assertFalse(user.is_email_confirmed)
        self.assertFalse(result)
        user.save.assert_not_called()

    @patch('user.models.User.objects.get')
    def test_confirm_email_token_expired(self, mock_get_user):
        # Set up the mock user
        user = User(username='testuser', email='test@example.com')
        user.email_confirmation_token = 'correct-token'
        user.email_confirmation_token_expires = timezone.now() - timezone.timedelta(days=1)
        user.save = MagicMock()
        mock_get_user.return_value = user

        # Encode the user ID
        uid = urlsafe_base64_encode(str(user.pk).encode('utf-8'))
        token = 'correct-token'

        # Call the method to be tested
        result = EmailService.confirm_email(token, uid)

        # Check if the user’s email is not confirmed
        self.assertFalse(user.is_email_confirmed)
        self.assertFalse(result)
        user.save.assert_not_called()
