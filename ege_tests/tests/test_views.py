from django.test import TestCase, RequestFactory
from django.urls import reverse

from ege_tests.views import *
from ege_tests.models import WordFromDictionary
from ege_tests.utils import *


class HomepageTestView(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class AllWordsByPartOfSpeechTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        words_with_accented_character = ['рука', 'голова', 'белый', 'черный', 'бегать', 'прыгать', 'сделанная',
                                         'рожденный', 'смотря', 'делая', 'быстро', 'бегло']
        accented_characters = [4, 6, 2, 2, 2, 3, 3, 5, 6, 2, 2, 2]
        for word_index in range(len(words_with_accented_character)):
            WordFromDictionary.objects.create(
                word=words_with_accented_character[word_index],
                accented_character=accented_characters[word_index],
                part_of_speech=parts_of_speech_en[word_index//2]
            )

    def setUp(self):
        self.view = AllWordsByPartOfSpeech()
        self.correct_args_to_request = parts_of_speech_en
        self.uncorrect_args_to_request = ['123', 'abc', '---']

    def test_view_url_exists_at_desired_location(self):
        for c_arg in self.correct_args_to_request:
            response = self.client.get(reverse('words_by_parts_of_speech', kwargs={'part_of_speech': c_arg}))
            self.assertEqual(response.status_code, 200)
        for unc_arg in self.uncorrect_args_to_request:
            response = self.client.get(reverse('words_by_parts_of_speech', kwargs={'part_of_speech': unc_arg}))
            self.assertEqual(response.status_code, 404)

    def test_get_queryset(self):
        qs = [['головА', 'рукА'], ['бЕлый', 'чЕрный'], ['бЕгать', 'прЫгать'], ['рождЕнный', 'сдЕланная'],
              ['дЕлая', 'смотрЯ'], ['бЕгло', 'бЫстро']]
        for arg in self.correct_args_to_request:
            request = RequestFactory().get(reverse('words_by_parts_of_speech', kwargs={'part_of_speech': arg}))
            self.view.request = request
            self.view.kwargs = {'part_of_speech': arg}
            qs_response = self.view.get_queryset()
            self.assertEqual(list(map(str, qs_response)), qs[self.correct_args_to_request.index(arg)])

    def test_get_context_data(self):
        for arg in self.correct_args_to_request:
            response = self.client.get(reverse('words_by_parts_of_speech', kwargs={'part_of_speech': arg}))
            part_of_speech_topic = get_part_of_speech_ru_plural(arg)
            self.assertEqual(part_of_speech_topic, response.context['part_of_speech_topic'])
