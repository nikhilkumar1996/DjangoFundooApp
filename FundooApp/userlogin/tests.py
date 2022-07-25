from rest_framework.test import APITestCase
from django.urls import reverse
import pdb


class TestUserLogin(APITestCase):
    def test_register_user(self):
        url = reverse('register')
        user_data = {
            "firstname": "demoName",
            "lastname": "demoTitle",
            "email": "demo@gmail.com",
            "password": "demo123",
            "phone_no": "9763458392"

        }
        res = self.client.post(url, user_data, format="json")
        # pdb.set_trace()
        self.assertEqual(res.status_code, 200)

    def test_login_user(self):
        url = reverse('getallusers')
        res = self.client.get(url, format="json")
        # pdb.set_trace()
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.status_code, 200)


