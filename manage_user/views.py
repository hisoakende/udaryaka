from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView

from manage_user.forms import RegistrationForm, LoginUserForm
from manage_user.utils import user_activation, send_and_return_key, get_user_email, get_username, get_hidden_email


class SuccessfulRegistration(UserPassesTestMixin, TemplateView):
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
        return self.request.session.get('user_activation')

    def post(self, request, *args, **kwargs):
        user_data = request.session['user_activation']
        if int(request.POST['key']) == user_data['key']:
            user_activation(user_data['username'])
            login(request, User.objects.get(username=user_data['username']))
            request.session['successful_registration'] = True
            return redirect('successful_registration')
        else:
            return super().get(request, *args, **kwargs, error=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hidden_email'] = get_hidden_email(self.request.session['user_activation']['email'])
        if kwargs.get('error'):
            context['error_message'] = 'Неверный код!'
        return context


class Registration(UserPassesTestMixin, CreateView):
    """Регистрация нового пользователя"""
    template_name = 'templates_for_manage_users_profile/registration.html'
    success_url = reverse_lazy('key_verification')
    form_class = RegistrationForm
    model = User

    def test_func(self):
        return not self.request.user.is_authenticated

    def post(self, request, *args, **kwargs):
        if self.get_form().is_valid():
            request.session['user_activation'] = {'username': request.POST['username'], 'email': request.POST['email'],
                                                  'key': send_and_return_key(request.POST['username'],
                                                                             request.POST['email'])}
        return super().post(request, *args, **kwargs)


class LoginUser(UserPassesTestMixin, LoginView):
    """Авторизация пользователя"""
    template_name = 'templates_for_manage_users_profile/login.html'
    redirect_field_name = reverse_lazy('homepage')
    form_class = LoginUserForm

    def test_func(self):
        return not self.request.user.is_authenticated

    def post(self, request, *args, **kwargs):
        errors = self.get_form().non_field_errors().as_data()
        if errors:
            if errors[0].code == 'inactive':
                request.session['user_data_for_send_mail'] = {'username': get_username(request.POST['username']),
                                                              'email': get_user_email(request.POST['username'])}
        return super().post(request, *args, **kwargs)


class SendMailForActivationAPI(APIView):

    def get(self, request):
        user_data = request.session.pop('user_data_for_send_mail')
        request.session['user_activation'] = {'username': user_data['username'],
                                              'key': send_and_return_key(user_data['username'], user_data['email']),
                                              'email': user_data['email']}
        return Response(status=200)
