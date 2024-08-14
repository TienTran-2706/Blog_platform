from django.test import Client, TestCase
from django.urls import reverse
from user.forms import RegistrationForm
from unittest.mock import patch
from django.utils.crypto import get_random_string



class RegistrationViewTest(TestCase):
    def test_registration_view_get(self):
        client = Client()
        response = client.get(reverse('user:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/register.html')
        form = response.context['form']
        self.assertIsInstance(form, RegistrationForm)

    #@patch('user.views.EmailService.send_confirmation_email')
    # def test_registration_view_post_valid_data(self, mock_send_email):
    #     mock_send_email.return_value = True  # Mock the send email method

    #     client = Client()
    #     data = {
    #         'username': 'testuser',
    #         'email': 'test@example.com',
    #         'password': 'password',
    #         'profile_picture': '',
    #         'bio': '',
    #     }

    #     response = client.post(reverse('user:register'), data)
    #     self.assertEqual(response.status_code, 302)  # Expect a redirect

    #     # Get the URL that the view redirected to
    #     redirect_url = response.url

    #     # Extract the uid and token from the redirect URL
    #     import re
    #     match = re.search(r'confirm-email/([^/]+)/([^/]+)/', redirect_url)
    #     if match:
    #         uid = match.group(1)
    #         token = match.group(2)

    #         # Reverse the confirm_email URL with the extracted uid and token
    #         confirm_email_url = reverse('user:confirm_email', kwargs={'uid': uid, 'token': token})

    #         # Make sure that the view redirected to the correct URL
    #         self.assertEqual(redirect_url, confirm_email_url)
    #     else:
    #         self.fail("Redirect URL does not match the expected pattern.")

