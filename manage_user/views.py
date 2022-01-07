from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView


class Registration(CreateView):
    """Регистрация нового пользователя"""
    template_name = 'templates_for_manage_users_profile/registration.html'
    success_url = reverse_lazy('homepage')
    form_class = UserCreationForm
    model = User
