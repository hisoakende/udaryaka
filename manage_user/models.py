from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def created_user_profile(**kwargs):
    """Создание или обновление профиль пользователя"""
    if kwargs['created']:
        kwargs['instance'].is_active = False
        kwargs['instance'].save()
