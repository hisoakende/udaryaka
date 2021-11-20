from django.db import models


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

    class Meta:
        ordering = ['word']
        verbose_name = 'Слово для тестов'
        verbose_name_plural = 'Слова для тестов'

    def __str__(self):
        return self.word