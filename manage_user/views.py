from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView

from manage_user.forms import RegistrationForm


class Registration(CreateView):
    """Регистрация нового пользователя"""
    template_name = 'templates_for_manage_users_profile/registration.html'
    success_url = reverse_lazy('homepage')
    form_class = RegistrationForm
    model = User
