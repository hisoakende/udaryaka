from random import randint

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from manage_user.forms import RegistrationForm
from manage_user.utils import get_message_text, user_activation


class SuccessfulRegistration(TemplateView):
    """Представление страницы успешной регистрации"""
    template_name = 'templates_for_manage_users_profile/successful_registration.html'

    def test_func(self):
        return self.request.session.get('successful_registration')

    def get(self, request, *args, **kwargs):
        del request.session['successful_registration']
        return super().get(request, *args, **kwargs)


class KeyVerification(UserPassesTestMixin, TemplateView):
    """Проверка кода подтверждения, отправленного пользователю на email """
    template_name = 'templates_for_manage_users_profile/key_verification.html'

    def test_func(self):
        return self.request.session.get('user')

    def post(self, request, *args, **kwargs):
        user_data = request.session['user']
        if int(request.POST['key']) == user_data['key']:
            user_activation(user_data['username'])
            login(request, User.objects.get(username=user_data['username']))
            request.session['successful_registration'] = True
            return redirect('successful_registration')
        else:
            return super().get(request, *args, **kwargs, error=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if kwargs.get('error'):
            context['error_message'] = 'Неверный код!'
        return context


class Registration(CreateView):
    """Регистрация нового пользователя"""
    template_name = 'templates_for_manage_users_profile/registration.html'
    success_url = reverse_lazy('key_verification')
    form_class = RegistrationForm
    model = User

    def post(self, request, *args, **kwargs):
        if self.get_form().is_valid():
            key = randint(100000, 999999)
            send_mail('Подтверждение регистрации',
                      get_message_text('key_verification', username=request.POST['username'], key=key),
                      settings.DEFAULT_FROM_EMAIL,
                      [request.POST['email']], fail_silently=False)
            request.session['user'] = {'username': request.POST['username'], 'key': key}
        return super().post(request, *args, **kwargs)
