from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254)
