import json
import bcrypt
from django.test import (
    TestCase,
    Client
)
from .models import User

class UserTest(TestCase):
    def setUp(self):
        client = Client()
        User.objects.create(
            email = 'g@example.com',
            password = bcrypt.hashpw('asdf1234'.encode('utf-8'),bcrypt.gensalt())
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_SignUpView_post_success(self):
        user = {
            'email'     : 'd@example.com',
            'password'  : 'asdf1234'
        }
        response = self.client.post('/account/sign-up', json.dumps(user), content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        
    def test_SignInView_post_success(self):
        user = {
            'email'     : 'g@example.com',
            'password'  : 'asdf1234'
        }
        response = self.client.post('/account/sign-in', json.dumps(user), content_type = 'application/json')
        self.assertEqual(response.status_code, 200)