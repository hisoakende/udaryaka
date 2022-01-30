from django.contrib.auth.models import User
from django.test import TestCase

from manage_user.utils import *


class UserActivationTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='user', password='user')

    def test_user_activation(self):
        user_activation('user')
        self.assertTrue(User.objects.get(username='user').is_active)


class GetMessageTextTestCase(TestCase):

    def test_raise_value_error(self):
        with self.assertRaises(ValueError):
            get_message_text('123456')

    def test_key_verification_message(self):
        excepted_result = 'Здравствуйте, user!\nВаш код подтверждения - 1'
        self.assertEqual(get_message_text('key_verification', username='user', key=1), excepted_result)


class GetKeyVerificationTextTestCase(TestCase):

    def test_get_message(self):
        excepted_result = 'Здравствуйте, user!\nВаш код подтверждения - 1'
        self.assertEqual(get_key_verification_text('user', 1), excepted_result)
