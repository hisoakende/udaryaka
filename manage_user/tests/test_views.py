from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse

from ..views import KeyVerification


class KeyVerificationTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user('user')

    def setUp(self):
        session = self.client.session
        session['user'] = {'username': 'user', 'key': 1}
        session.save()

    def test_get_context_data_with_error(self):
        self.view = KeyVerification()
        self.get = RequestFactory().get(reverse('key_verification'))
        self.view.request = self.get
        result = self.view.get_context_data(error=True)
        self.assertIn('error', result)

    def test_correct_key_verification_redirect(self):
        response = self.client.post(reverse('key_verification'), data={'key': 1})
        self.assertRedirects(response, reverse('successful_registration'))

    def test_uncorrect_key_verification(self):
        response = self.client.post(reverse('key_verification'), data={'key': 2})
        self.assertEqual(response.status_code, 200)
