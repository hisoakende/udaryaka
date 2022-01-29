from django.contrib.auth.models import User


def user_activation(username):
    """Активация пользователя"""
    user = User.objects.get(username=username)
    user.profile.is_active = True
    user.profile.save()


def get_message_text(type_message, **kwargs):
    """Получения текста сообщения какого-либо типа"""
    if type_message == 'key_verification':
        return get_key_verification_text(kwargs['username'], kwargs['key'])
    else:
        raise ValueError('Невозможно создать текст сообщения')


def get_key_verification_text(username, key):
    return f'Здравствуйте, {username}!\nВаш код подтверждения - {key}'
