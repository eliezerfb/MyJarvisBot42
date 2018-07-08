from datetime import datetime
from django.test import TestCase

from myjarvisbot.jarvis.models import Lista, ItensLista


class ListaModelTest(TestCase):
    def setUp(self):
        self.obj = Lista()
        self.obj.save()

    def test_create(self):
        self.assertTrue(Lista.objects.exists())

    def test_field_semana(self):
        self.assertEqual(self.obj.semana, datetime.today().isocalendar()[1])

    def test_field_ano(self):
        self.assertEqual(self.obj.ano, datetime.today().year)


class ItensListaModelTest(TestCase):
    def setUp(self):
        self.obj = ItensLista(produto='Tomate')
        self.obj.save()

    def test_field_produto(self):
        self.assertEqual(self.obj.produto, 'Tomate')

    def test_create(self):
        self.assertTrue(ItensLista.objects.exists())

    def test_quantidade(self):
        self.assertEqual(self.obj.quantidade, '')
