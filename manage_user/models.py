from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """Расширение стандартной модели пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name='Активный', default=False)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def created_user_profile(**kwargs):
    """Создание или обновление профиль пользователя"""
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])
    else:
        kwargs['instance'].profile.save()
