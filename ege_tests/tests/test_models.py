from django.test import TestCase
from ege_tests.models import *


class WordFromDictionaryTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        WordFromDictionary.objects.create(
            word='нога',
            accented_character=4,
            part_of_speech='noun'
        )

    def test_object_name_is_label_of_word(self):
        word_from_dict = WordFromDictionary.objects.all().first()
        self.assertEqual(str(word_from_dict), 'нога')
