from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    username = forms.CharField(
        help_text=''
    )

    password1 = forms.CharField(
        label='Password',
        help_text='',
        widget=forms.PasswordInput()
    )

    password2 = forms.CharField(
        label='Confirm password',
        help_text='',
        widget=forms.PasswordInput()
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
