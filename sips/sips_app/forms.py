from django import forms
from . import models
from django.contrib.auth.forms import AuthenticationForm


class RegisterForm(forms.ModelForm):

    email = forms.CharField(widget=forms.EmailInput)
    handle = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = models.User
        fields = ["handle", "password", "email"]


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email')
