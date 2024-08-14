from django.test import TestCase
from user.forms import RegistrationForm, LoginForm , UpdateForm
from user.models import User
from django.contrib.auth import authenticate

class RegistrationFormTest(TestCase):

    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'password_confirm': 'password123',
            'profile_picture': None,
            'bio': 'This is a test bio'
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'password_confirm': 'differentpassword',
            'profile_picture': None,
            'bio': 'This is a test bio'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password_confirm', form.errors)

    def test_missing_fields(self):
        form_data = {
            'username': '',
            'email': 'test@example.com',
            'password': 'password123',
            'password_confirm': 'password123',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

class LoginFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='password123'
        )

    def test_valid_login(self):
        form_data = {
            'username': 'test@example.com',
            'password': 'password123'
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = authenticate(email='test@example.com', password='password123')
        self.assertIsNotNone(user)

    def test_invalid_login(self):
        form_data = {
            'username': 'test@example.com',
            'password': 'wrongpassword'
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())


class UpdateFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='password123'
        )
        self.form_data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'profile_picture': None,
            'bio': 'Updated bio'
        }

    def test_valid_update(self):
        form = UpdateForm(instance=self.user, data=self.form_data)
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.username, 'updateduser')
        self.assertEqual(updated_user.email, 'updated@example.com')

    def test_invalid_update(self):
        form_data = {
            'username': '',
            'email': 'invalid-email',
            'profile_picture': None,
            'bio': 'Updated bio'
        }
        form = UpdateForm(instance=self.user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)