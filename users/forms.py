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

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError('This username is already taken')

        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError('This email address is already taken')

        if username == self.instance.username and email == self.instance.email:
            raise forms.ValidationError('You did not make any changes')

        return cleaned_data

    class Meta:
        model = User
        fields = ['username', 'email']
