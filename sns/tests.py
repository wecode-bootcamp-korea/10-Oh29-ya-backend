from account.models import User
from .models        import (
    Staff,
    Post,
    Hashtag,
    PostHashtag,
    LikePost
)

from django.test import TestCase, Client

clinet = Client()

class TestPostView(TestCase):
    def test_postview(self):
        response = clinet.get('/sns')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'data':data_list})
