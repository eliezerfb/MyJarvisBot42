from django.test import TestCase

from myjarvisbot.jarvis.models import UsersTelegram



class TestModelUsersTelegram(TestCase):
    def setUp(self):
        self.obj = UsersTelegram(username='eliezerfb', chat_id='123')
        self.obj.save()

    def test_create(self):
        self.assertTrue(UsersTelegram.objects.exists())

    def test_field_username(self):
        self.assertEqual(self.obj.username, 'eliezerfb')

    def test_field_chat_id(self):
        self.assertEqual(self.obj.chat_id, '123')

    def test_str(self):
        self.assertEqual(str(self.obj), 'eliezerfb')
