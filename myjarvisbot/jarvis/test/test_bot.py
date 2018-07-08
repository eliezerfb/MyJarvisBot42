from django.conf import settings
from django.test import TestCase
import json


class BotTest(TestCase):
    def test_post_invalid_token(self):
        resp = self.client.post('/bot/xpto/',
                                data=json.dumps({}),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 403)
