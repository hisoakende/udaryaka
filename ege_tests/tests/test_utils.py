from django.test import TestCase
from ..models import *
from ..utils import *


class GetTestTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        WordFromDictionary.objects.create(
            word='земля',
            accented_character=5,
            part_of_speech='noun'
        )
        UsersTest.objects.create(
            test_id=1,
            type_test='open'
        )
        ConnectionTestAndWord.objects.create(
            test=UsersTest.objects.get(test_id=1),
            word=WordFromDictionary.objects.get(word='земля')
        )
        cls.expected_result = {0: {'possible_values': ['зЕмля', 'землЯ'], 'correct_value': 1}}

    def test_get_random_test(self):
        self.assertEqual(get_test(1), self.expected_result)

    def test_get_not_random_test(self):
        self.assertEqual(get_test(test_id=1), self.expected_result)


class ParsedWordsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        WordFromDictionary.objects.create(
            word='бегать',
            accented_character=2,
            part_of_speech='verb'
        )

    def test_parsed_words_test(self):
        words_parc = parsed_words(WordFromDictionary.objects.all())
        expected_result = {0: {'possible_values': ['бЕгать', 'бегАть'], 'correct_value': 0}}
        self.assertEqual(words_parc, expected_result)


class CheckTestForExistenceTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        WordFromDictionary.objects.create(
            word='земля',
            accented_character=5,
            part_of_speech='noun'
        )
        UsersTest.objects.create(
            test_id=1,
            type_test='open'
        )
        ConnectionTestAndWord.objects.create(
            test=UsersTest.objects.get(test_id=1),
            word=WordFromDictionary.objects.get(word='земля')
        )

    def test_test_is_existence(self):
        self.assertEqual(check_test_for_existence(1), 200)

    def test_test_is_not_existence(self):
        self.assertEqual(check_test_for_existence(2), 204)


class CheckUserAnswersTestCase(TestCase):

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

    def test_check_user_answers(self):
        request = {'question-0': 'вероисповЕдание', 'question-1': 'ждАла'}
        expected_result = ([('вероисповЕдание', True), ('ждАла', False)], '1/2')
        self.assertEqual(check_user_answers(1, request), expected_result)


class AddedIncorrectMarkTestCase(TestCase):

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

    def test_added_incorrect_mark(self):
        expected_result = {0: {'possible_values': ['вЕроисповедание', 'верОисповедание', 'вероИсповедание',
                                                   'вероиспОведание', 'вероисповЕдание', 'вероисповедАние',
                                                   'вероисповеданИе', 'вероисповеданиЕ'],
                               'correct_value': 4,
                               'user_incorrect_value': 0},
                           1: {'possible_values': ['ждАла', 'ждалА'],
                               'correct_value': 1,
                               'user_incorrect_value': 0}}
        words = {0: {'possible_values': ['вЕроисповедание', 'верОисповедание', 'вероИсповедание',
                                         'вероиспОведание', 'вероисповЕдание', 'вероисповедАние',
                                         'вероисповеданИе', 'вероисповеданиЕ'],
                     'correct_value': 4},
                 1: {'possible_values': ['ждАла', 'ждалА'],
                     'correct_value': 1}}
        user_answers = [('вЕроисповедание', False), ('ждАла', False)]
        self.assertEqual(added_incorrect_mark(words, user_answers), expected_result)
