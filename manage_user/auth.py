from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class EmailAuthBackend(ModelBackend):
    """Авторизация пользователя по email или username"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        if '@' in username:
            data = {'email': username}
        else:
            data = {'username': username}
        try:
            user = User.objects.get(**data)
            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
