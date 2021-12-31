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
                part_of_speech=parts_of_speech_en[word_index // 2]
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


class UsersTestPageTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        WordFromDictionary.objects.create(
            word='вероисповедание',
            accented_character=10,
            part_of_speech='noun'
        )
        WordFromDictionary.objects.create(
            word='ждала',
            accented_character=5,
            part_of_speech='verb'
        )
        UsersTest.objects.create(
            test_id=1,
            type_test='open'
        )
        ConnectionTestAndWord.objects.create(
            test=UsersTest.objects.get(test_id=1),
            word=WordFromDictionary.objects.get(word='вероисповедание')
        )
        ConnectionTestAndWord.objects.create(
            test=UsersTest.objects.get(test_id=1),
            word=WordFromDictionary.objects.get(word='ждала')
        )

    def setUp(self):
        self.view = UsersTestPage()
        self.view.kwargs = {'test_id': 1}
        self.get = RequestFactory().get(reverse('users_test', kwargs={'test_id': 1}))
        self.post = RequestFactory().post(reverse('users_test', kwargs={'test_id': 1}),
                                          data={'question-0': ['вероисповЕдание'], 'question-1': ['ждАла']})

    def test_get_queryset_get(self):
        self.view.request = self.get
        qs_response = self.view.get_queryset()
        expected_result = {0: {'possible_values': ['вЕроисповедание', 'верОисповедание', 'вероИсповедание',
                                                   'вероиспОведание', 'вероисповЕдание', 'вероисповедАние',
                                                   'вероисповеданИе', 'вероисповеданиЕ'],
                               'correct_value': 4},
                           1: {'possible_values': ['ждАла', 'ждалА'],
                               'correct_value': 1}}
        self.assertEqual(qs_response, expected_result)

    def test_get_queryset_post(self):
        self.view.request = self.post
        qs_response = self.view.get_queryset()
        expected_result = {0: {'possible_values': ['вЕроисповедание', 'верОисповедание', 'вероИсповедание',
                                                   'вероиспОведание', 'вероисповЕдание', 'вероисповедАние',
                                                   'вероисповеданИе', 'вероисповеданиЕ'],
                               'correct_value': 4},
                           1: {'possible_values': ['ждАла', 'ждалА'],
                               'correct_value': 1,
                               'user_incorrect_value': 0}}
        self.assertEqual(qs_response, expected_result)

    def test_get_context_data_get(self):
        response = self.client.get(reverse('users_test', kwargs={'test_id': 1}))
        self.assertEqual(response.context['test_id'], 1)

    def test_get_context_data_post(self):
        response = self.client.post(reverse('users_test', kwargs={'test_id': 1}),
                                    data={'question-0': ['вероисповЕдание'], 'question-1': ['ждАла']})
        self.assertEqual(response.context['correct_count'], '1/2')
