from datetime import datetime

from django.test import TestCase

from myjarvisbot.jarvis.models import ItensLista


class ItensListaModelTest(TestCase):
    def setUp(self):
        self.obj = ItensLista(produto='tomate')
        self.obj.save()

    def test_field_produto(self):
        self.assertEqual(self.obj.produto, 'tomate')

    def test_produto(self):
        self.assertEqual(str(self.obj), 'Tomate')

    def test_create(self):
        self.assertTrue(ItensLista.objects.exists())

    def test_quantidade(self):
        self.assertEqual(self.obj.quantidade, '')

    def test_field_semana(self):
        self.assertEqual(self.obj.semana, int(datetime.today().strftime('%U')))

    def test_field_ano(self):
        self.assertEqual(self.obj.ano, datetime.today().year)
