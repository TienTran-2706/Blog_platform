from django.urls import path
from user.views import RegistrationView, LoginView, LogoutView, ProfileView, UpdateProfileView, EmailConfirmationView, EmailConfirmedView, PasswordChangeDoneView, PasswordResetCompleteView, PasswordChangeView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView

app_name = 'user'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('update-profile/', UpdateProfileView.as_view(), name='update'),
    path('confirm-email/<str:token>/', EmailConfirmationView.as_view(), name='confirm_email'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('invalid-token/', EmailConfirmationView.as_view(), name='invalid_token'),

    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
