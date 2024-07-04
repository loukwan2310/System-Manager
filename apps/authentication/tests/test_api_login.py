from rest_framework.test import APITestCase

from apps.users.models import User


class APILoginTests(APITestCase):
    fixtures = []

    def setUp(self):
        self.user = User.objects \
            .create_user(username='test', email='test@gmail.com', password='12345678')  # pylint: disable=E1120

    def test_api_login_success(self):
        payload = {
            'username': 'test',
            'password': '12345678'  # pylint: disable=E1120
        }
        response = self.client.post('/api/v1/auth/login', data=payload, format='json')
        self.assertEqual(response.status_code, 200)
