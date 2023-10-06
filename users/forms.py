from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class':'form-input','placeholder':'Email'})
    )

    username = forms.CharField(
        help_text='',
        widget=forms.TextInput(attrs={'class':'form-input','placeholder':'Username'})
    )

    password1 = forms.CharField(
        label='Password',
        help_text='',
        widget=forms.PasswordInput(attrs={'class':'form-input','placeholder':'Password'})
    )

    password2 = forms.CharField(
        label='Confirm password',
        help_text='',
        widget=forms.PasswordInput(attrs={'class':'form-input','placeholder':'Re-type password'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateProfileForm(forms.ModelForm):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

    class Meta:
        model = User
        fields = ['username', 'email']
