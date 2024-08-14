from django.urls import reverse, resolve
from django.test import TestCase
from user.views import RegistrationView, LoginView, LogoutView, ProfileView, UpdateProfileView, EmailConfirmationView, EmailConfirmedView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

class URLTests(TestCase):

    def test_register_url(self):
        url = reverse('user:register')
        self.assertEqual(resolve(url).func.view_class, RegistrationView)

    def test_login_url(self):
        url = reverse('user:login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_logout_url(self):
        url = reverse('user:logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)

    def test_profile_url(self):
        url = reverse('user:profile')
        self.assertEqual(resolve(url).func.view_class, ProfileView)

    def test_update_profile_url(self):
        url = reverse('user:update')
        self.assertEqual(resolve(url).func.view_class, UpdateProfileView)

    def test_confirm_email_url(self):
        uid = 'test-uid'
        token = 'test-token'
        url = reverse('user:confirm_email', kwargs={'uid': uid, 'token': token})
        self.assertEqual(resolve(url).func.view_class, EmailConfirmationView)

    def test_email_confirmed_url(self):
        url = reverse('user:email_confirmed')
        self.assertEqual(resolve(url).func.view_class, EmailConfirmedView)

    def test_invalid_token_url(self):
        url = reverse('user:invalid_token')
        self.assertEqual(resolve(url).func.view_class, EmailConfirmationView)

    def test_password_change_url(self):
        url = reverse('user:password_change')
        self.assertEqual(resolve(url).func.view_class, PasswordChangeView)

    def test_password_change_done_url(self):
        url = reverse('user:password_change_done')
        self.assertEqual(resolve(url).func.view_class, PasswordChangeDoneView)

    def test_password_reset_url(self):
        url = reverse('user:password_reset')
        self.assertEqual(resolve(url).func.view_class, PasswordResetView)

    def test_password_reset_done_url(self):
        url = reverse('user:password_reset_done')
        self.assertEqual(resolve(url).func.view_class, PasswordResetDoneView)

    def test_password_reset_confirm_url(self):
        uidb64 = 'test-uidb64'
        token = 'test-token'
        url = reverse('user:password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
        self.assertEqual(resolve(url).func.view_class, PasswordResetConfirmView)

    def test_password_reset_complete_url(self):
        url = reverse('user:password_reset_complete')
        self.assertEqual(resolve(url).func.view_class, PasswordResetCompleteView)