from django.test import TestCase
from ..models import *
from ..utils import *


class GetRandomTestTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        WordFromDictionary.objects.create(
            word='бегать',
            accented_character=2,
            part_of_speech='verb'
        )

    def test_get_random_test(self):
        words_api = get_random_test(1)
        expected_result = {
            0: {'possible_values': ['бЕгать', 'бегАть'], 'correct_value': 0},
        }
        self.assertEqual(words_api, expected_result)


class CheckTestForExistenceTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        WordFromDictionary.objects.create(
            word='земля',
            accented_character=5,
            part_of_speech='noun'
        )
        ConnectionTestAndWord.objects.create(
            test_id=1,
            word=WordFromDictionary.objects.get(word='земля')
        )

    def test_check_test_for_existence(self):
        res_1 = check_test_for_existence(1)
        res_2 = check_test_for_existence(2)
        self.assertEqual(res_1, 200)
        self.assertEqual(res_2, 204)
