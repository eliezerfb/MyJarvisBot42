from django.test import TestCase

from myjarvisbot.jarvis import views
from myjarvisbot.jarvis.models import ItensLista




class TestInsertItemListaComQuantide(TestCase):
    def setUp(self):
        views._insert_item_lista(command='Tomate, 1kg')

    def test_insert_item_descricao(self):
        self.assertEqual(ItensLista.objects.all()[0].produto, 'Tomate')

    def test_insert_item_quantidade(self):
        self.assertEqual(ItensLista.objects.all()[0].quantidade, '1kg')


class TestInsertItemListaSemQuantide(TestCase):
    def setUp(self):
        views._insert_item_lista(command='Tomate')

    def test_insert_item_descricao(self):
        self.assertEqual(ItensLista.objects.all()[0].produto, 'Tomate')

    def test_insert_item_quantidade(self):
        self.assertEqual(ItensLista.objects.all()[0].quantidade, '')
