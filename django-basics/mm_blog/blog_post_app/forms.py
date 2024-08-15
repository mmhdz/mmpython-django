from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User



