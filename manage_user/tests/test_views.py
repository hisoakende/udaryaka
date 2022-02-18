from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class KeyVerificationTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user('user')

    def setUp(self):
        session = self.client.session
        session['user_activation'] = {'username': 'user', 'email': 'example@gmail.com', 'key': 1}
        session.save()

    def test_correct_key_verification_redirect(self):
        response = self.client.post(reverse('key_verification'), data={'key': 1})
        self.assertRedirects(response, reverse('successful_registration'))

    def test_uncorrect_key_verification(self):
        response = self.client.post(reverse('key_verification'), data={'key': 2})
        self.assertEqual(response.status_code, 200)
