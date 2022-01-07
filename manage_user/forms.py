from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

attr_class = 'form-control shadow-none enter-inf'


class RegistrationForm(UserCreationForm):
    """Форма регистрации"""
    username = forms.CharField(
        label='', widget=forms.TextInput(attrs={'class': attr_class, 'placeholder': 'Псевдоним'}))
    email = forms.CharField(
        label='', widget=forms.EmailInput(attrs={'class': attr_class, 'placeholder': 'Электронная почта'}))
    password1 = forms.CharField(
        label='', widget=forms.PasswordInput(attrs={'class': attr_class, 'placeholder': 'Пароль'}))
    password2 = forms.CharField(
        label='', widget=forms.PasswordInput(attrs={'class': attr_class, 'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
