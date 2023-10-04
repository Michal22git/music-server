from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, CreateView

from .forms import UserRegisterForm


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Welcome back {self.request.user.username}!")
        return response


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


@method_decorator(login_required, name='dispatch')
class UserProfileView(DetailView):
    template_name = 'users/profile.html'

    def get_object(self):
        return self.request.user
