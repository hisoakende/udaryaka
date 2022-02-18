from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError

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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            return email
        else:
            raise ValidationError('Пользователь с такой электронной почтой уже существует.', code='existing_email')


class LoginUserForm(AuthenticationForm):
    """Форма авторизации"""
    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': attr_class, 'placeholder': 'Псевдоним или Электронная почта'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': attr_class, 'placeholder': 'Пароль'}))
    error_messages = {
        'invalid_login_or_email': 'Что-то неверно: псевдоним, электронная почта или пароль.',
        'inactive': 'Ты зарегистрирован не до конца.'
    }

    def get_invalid_login_error(self):
        return ValidationError(self.error_messages['invalid_login_or_email'], code='invalid_login_or_email')
