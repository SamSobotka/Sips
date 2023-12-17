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


class CommentForm(forms.ModelForm):  # comments coming soon!
    class Meta:
        model = models.Comment
        # content
        fields = ["content"]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = models.Message
        fields = ['content']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['handle', 'bio', 'email']
