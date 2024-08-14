from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile_picture', 'bio']

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'profile_picture', 'bio']