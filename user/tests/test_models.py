from django.test import TestCase
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils import timezone
from user.models import User
import uuid

class UserModelTest(TestCase):

    def setUp(self):
        """Create a user instance for testing."""
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='testpassword'
        )

    def test_user_creation(self):
        """Test that a user is created correctly."""
        user = User.objects.get(email='testuser@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('testpassword'))
        self.assertFalse(user.is_email_confirmed)
        self.assertIsNotNone(user.email_confirmation_token)
        self.assertIsNotNone(user.email_confirmation_sent_at)

    def test_generate_confirmation_token(self):
        """Test that generate_confirmation_token generates a valid token."""
        token = self.user.generate_confirmation_token()
        # Decode the token
        decoded_uid = urlsafe_base64_decode(token).decode('utf-8')
        # Check if the decoded UID is a valid UUID
        try:
            uuid.UUID(decoded_uid)
            valid_uuid = True
        except ValueError:
            valid_uuid = False
        self.assertTrue(valid_uuid)

    def test_save_generates_token_if_needed(self):
        """Test that save() generates a confirmation token if one does not exist."""
        user = User(
            email='newuser@example.com',
            username='newuser',
            password='newpassword'
        )
        user.save()
        self.assertIsNotNone(user.email_confirmation_token)
        self.assertIsNotNone(user.email_confirmation_sent_at)
        self.assertFalse(user.is_email_confirmed)


    def test_custom_user_manager_create_user(self):
        """Test the CustomUserManager.create_user method."""
        user = User.objects.create_user(
            email='manageruser@example.com',
            username='manageruser',
            password='managerpassword'
        )
        self.assertEqual(user.email, 'manageruser@example.com')
        self.assertTrue(user.check_password('managerpassword'))

    def test_custom_user_manager_create_superuser(self):
        """Test the CustomUserManager.create_superuser method."""
        superuser = User.objects.create_superuser(
            email='superuser@example.com',
            username='superuser',
            password='superuserpassword'
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.check_password('superuserpassword'))
