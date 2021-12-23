import random

from django.db import models
from django.urls import reverse


class WordFromDictionaryManager(models.Manager):
    """Менеджер модели WordFromDictionary"""

    def random(self, number_of_required=1):
        return random.choices(self.all(), k=number_of_required)


class WordFromDictionary(models.Model):
    """Слово, которое будет добавлено в тест по ударениям"""
    PART_OF_SPEECH = (
        ('noun', 'Имя существительное'),
        ('adjective', 'Имя прилагательное'),
        ('verb', 'Глагол'),
        ('participle', 'Причастие'),
        ('gerunds', 'Деепричастие'),
        ('adverb', 'Наречие')
    )

    word = models.CharField(verbose_name='Слово', max_length=50)
    accented_character = models.IntegerField(verbose_name='Буква под ударением (по счету)')
    part_of_speech = models.CharField(verbose_name='Часть речи', max_length=10, choices=PART_OF_SPEECH)
    objects = WordFromDictionaryManager()

    class Meta:
        ordering = ['word']
        verbose_name = 'Слово для тестов'
        verbose_name_plural = 'Слова для тестов'

    def __str__(self):
        return self.word


class ConnectionTestAndWord(models.Model):
    """Модель для привязки теста и слова для проверки ударения"""
    test_id = models.IntegerField(verbose_name='id теста')
    word = models.ForeignKey(WordFromDictionary, verbose_name='Слово для проверки', on_delete=models.CASCADE)

    class Meta:
        ordering = ['test_id']
        verbose_name = 'Связь между тестом и словом'
        verbose_name_plural = 'Связи между тестами и словами'

    def __str__(self):
        return f'id теста - {self.test_id}, слово - {self.word}'

    def get_absolute_url(self):
        return reverse('tests/id=', kwargs={'test_id': self.test_id})
