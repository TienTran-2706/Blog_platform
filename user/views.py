from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import  UpdateView, DetailView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.shortcuts import  redirect
from django.contrib.auth import authenticate
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.contrib.auth.views import PasswordResetCompleteView as DjangoPasswordResetCompleteView
from django.contrib.auth.views import PasswordResetConfirmView as DjangoPasswordResetConfirmView
from django.contrib.auth.views import PasswordResetDoneView as DjangoPasswordResetDoneView
from django.contrib.auth.views import PasswordResetView as DjangoPasswordResetView
from django.contrib.auth.views import PasswordChangeDoneView as DjangoPasswordChangeDoneView
from django.contrib.auth.views import PasswordChangeView as DjangoPasswordChangeView


from django.urls import reverse_lazy
from .models import User
from .forms import RegistrationForm, UpdateForm, LoginForm

from .services import EmailService
import logging
logger = logging.getLogger(__name__)

def custom_error_handler(request, exception):
    logger.error(f"An error occurred: {exception}")
    return HttpResponse("An error occurred. Please try again later.", status=500)


class RegistrationView(View):
    """
    View for user registration.

     Methods:
        get(request): Handles GET requests and renders the registration form.
        post(request): Handles POST requests and creates a new user if the form data is valid.
    """

    def get(self, request):
        """
        Renders the registration form.

        Args:
            request: The HTTP request object.

        Returns:
            Renders the 'user/egistration.html' template with the form.
        """
        try:
            form = RegistrationForm()
            logger.info('User registration from rendered')
            return render(request, 'user/registration.html', {'form': form})
        except Exception as e:
            # Handle unexpected error
            logger.error(f"An error occurred: {e}")
            return custom_error_handler(request, e)
    def post(self, request):
            """
            Handles POST requests and creates a new user if the form data is valid.

            Args:
                request (HttpRequest): The incoming request object.

            Returns:
                HttpResponse: A response object with a redirect to the confirmation page if the user is created successfully.
            """
            try:
                form = RegistrationForm(request.POST)
                if form.is_valid():
                    user = form.save(commit=False)
                    user.is_active = False
                    user.save()
                    EmailService.send_confirmation_email(user)
                    return redirect('user:confirm-email')
                return render(request, 'user/registration.html', {'form': form})
            except IntegrityError as e:
                logger.error(f"IntegrityError occurred: {e}")
                return custom_error_handler(request, e)
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                return custom_error_handler(request, e)


class LoginView(View):

    def get(self, request):
        """
        Renders the login form.
        """
        try:
            form = LoginForm()
            logger.info('Login form rendered')
            return render(request, 'user/login.html', {'form': form})
        except Exception as e:
            # Handle unexpected error
            logger.error(f"An error occurred: {e}")
            return custom_error_handler(request, e)

    def post(self, request):
        """
        Handles POST requests and logs in the user if the form data is valid.
        """
        try:
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('profile')
                else:
                    form.add_error(None, 'Invalid username or password')
            return render(request, 'user/login.html', {'form': form})
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return custom_error_handler(request, e)


class LogoutView(DjangoLogoutView):
    """
    View for user logout.
    """

    next_page = reverse_lazy('home')

class ProfileView(LoginRequiredMixin, DetailView):
    """
    Displays the user profile page.

    This view requires the user to be authenticated. It displays the user's
    profile information, including the username, profile picture, and bio.

    Attributes:
        model (User): The user model.
        template_name (str): The name of the template to render.
        context_object_name (str): The name of the context variable to store the user object.

    Methods:
        get_object(self, queryset=None): Ensures that users can only see their own profile.
    """

    model = User
    template_name='user/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        """
        Ensures that users can only see their own profile.

        Args:
            queryset (QuerySet): The queryset of users to filter.

        Raises:
            PermissionDenied: If the user trying to access the profile is not the same as the logged in user.

        Returns:
            User: The logged in user's profile.
        """
        # Ensure users can only see their own profile
        try:
            if not self.request.user.is_authenticated:
                raise PermissionDenied
            obj = self.request.user
            return obj
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return custom_error_handler(self.request, e)

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """
    View for updating user profiles.

    This view requires the user to be authenticated. It allows the user to update
    their own profile information, including the username, email, profile picture,
    and bio.

    Attributes:
        model (User): The user model.
        form_class (UpdateForm): The form to use for updating the user profile.
        template_name (str): The name of the template to render.

    Methods:
        get_object(self, queryset=None): Ensures that users can only update their own profile.
        form_valid(self, form): Additional security check to ensure user is editing their own profile.
    """

    model = User
    form_class = UpdateForm()
    template_name = 'user/update.html'

    def get_object(self, queryset=None):
        """
        Ensures that users can only update their own profile.

        Args:
            queryset (QuerySet): The queryset of users to filter.

        Returns:
            User: The logged in user's profile.
        """
        # Ensure users can only update their own profile
        try:
            if not self.request.user.is_authenticated:
                raise PermissionDenied
            obj = self.request.user
            return obj
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return custom_error_handler(self.request, e)

    def form_valid(self, form):
        """
        Additional security check to ensure user is editing their own profile.

        Args:
            form (UpdateForm): The form instance.

        Returns:
            HttpResponse: The response to the form submission.
        """
        # Additional security check to ensure user is editing their own profile
        try:
            if not form.is_valid():
                raise PermissionDenied
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return custom_error_handler(self.request, e)


class EmailConfirmationView(View):
    """
    View for confirming a user's email address.

    This view handles the GET request to the email confirmation link. It decodes the token
    from the URL, retrieves the corresponding user, confirms the user's email address, and saves
    the changes to the database. If the token is invalid or the user is not found, it redirects
    to the 'invalid_token' page.

    Attributes:
        None

    Methods:
        get(self, request, token): Handles the GET request and confirms the user's email address.
    """
    def get(self, request, token):
        try:
            # Decode the token
            uid = force_str(urlsafe_base64_decode(token))
            # Get the user by the decoded UID
            user = User.objects.get(email_confirmation_token=uid)
            # Confirm the user
            user.is_email_confirmed = True
            user.email_confirmation_token = None  # Clear the token
            user.save()
            return redirect('email_confirmed')
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            # Handle errors, such as invalid token or user not found
            return redirect('invalid_token')


class EmailConfirmedView(View):
    """
    View for displaying the email confirmation success page.

    This view handles the GET request to the email confirmation success page. It renders
    the 'email_confirmed.html' template.

    Attributes:
        template_name (str): The name of the template to render.

    Methods:
        get(self, request): Renders the 'email_confirmed.html' template.
    """
    template_name = 'user/email_confirmed.html'

    def get(self, request):
        return render(request, self.template_name)

class PasswordChangeView(DjangoPasswordChangeView):
    """
    View for changing the user's password.

    Attributes:
        success_url (str): The URL to redirect to after the password is changed.
    """

    success_url = reverse_lazy('password_change_done')


class PasswordChangeDoneView(DjangoPasswordChangeDoneView):
    """
    View for displaying a success message after the password is changed.
    """

    template_name = 'password_change_done.html'


class PasswordResetView(DjangoPasswordResetView):
    """
    View for resetting the user's password.
    """

    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'


class PasswordResetDoneView(DjangoPasswordResetDoneView):
    """
    View for displaying a success message after the password reset email is sent.
    """

    template_name = 'password_reset_done.html'


class PasswordResetConfirmView(DjangoPasswordResetConfirmView):
    """
    View for confirming the password reset.
    """

    template_name = 'password_reset_confirm.html'


class PasswordResetCompleteView(DjangoPasswordResetCompleteView):
    """
    View for displaying a success message after the password is reset.
    """

    template_name = 'password_reset_complete.html'