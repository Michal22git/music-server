from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import UserRegisterForm, UserUpdateProfileForm


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Welcome back {self.request.user.username}!")
        return response
    
    def get_form(form):
        form = super().get_form(form_class=None)
        form.fields['username'].widget.attrs.update({'class': 'form-input','placeholder':'Username'})
        form.fields['password'].widget.attrs.update({'class': 'form-input','placeholder':'Password'})
        return form


class CustomLogoutView(SuccessMessageMixin, LogoutView):
    next_page = reverse_lazy('app:home')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, 'You have been logged out successfully, see you soon!')
        return response


class UserRegisterView(SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully, now you can login!"


class UserProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    success_message = "Data has been updated!"

    def get_object(self):
        return self.request.user
