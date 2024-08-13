from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth import login, authenticate
from .models import User
from .forms import UserRegistrationForm, UserUpdateForm


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'user/user_registration.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(self.request, user)
        return redirect('user_profile')


class UserProfileView(DetailView):
    model = User
    template_name='user/user_profile.html'
    context_object_name = 'user'

class UpdateProfileView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user/user_update.html'

    def get_object(self, queryset=None):
        return self.request.user