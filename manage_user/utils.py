from random import randint

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail


def user_activation(username):
    """Активация пользователя"""
    user = User.objects.get(username=username)
    user.is_active = True
    user.save()


def get_message_text(type_message, **kwargs):
    """Получения текста сообщения какого-либо типа"""
    if type_message == 'key_verification':
        return get_key_verification_text(kwargs['username'], kwargs['key'])
    else:
        raise ValueError('Невозможно создать текст сообщения')


def get_key_verification_text(username, key):
    return f'Здравствуйте, {username}!\nВаш код подтверждения - {key}'


def send_and_return_key(username, email):
    """Функция высылает и возвращает ключ подтверждения"""
    key = randint(100000, 999999)
    send_mail('Подтверждение регистрации',
              get_message_text('key_verification', username=username, key=key),
              settings.DEFAULT_FROM_EMAIL,
              [email], fail_silently=False)
    return key


def get_user_email(s):
    if '@' in s:
        return s
    else:
        return User.objects.get(username=s).email


def get_username(s):
    if '@' in s:
        return User.objects.get(email=s).username
    else:
        return s


def get_hidden_email(email):
    """Возвращает скрытый email """
    index = email.index('@')
    return email[:3] + len(email[3:index]) * '*' + email[index:]
