from django.urls import path
from .views import UserRegistrationView, UserProfileView, UpdateProfileView, EmailConfirmationView, EmailConfirmedView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('update/', UpdateProfileView.as_view(), name='user_update'),
    path('confirm-email/<str:token>/', EmailConfirmationView.as_view(), name='confirm_email'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('invalid-token/', EmailConfirmationView.as_view(), name='invalid_token'),  # Add this if needed
]
