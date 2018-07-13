from django.test import TestCase

from myjarvisbot.jarvis import views
from myjarvisbot.jarvis.models import ItensLista



class TestInsertItemListaComQuantide(TestCase):
    def setUp(self):
        views._insert_item_lista(command='tomate, 1kg')

    def test_insert_item_descricao(self):
        self.assertEqual(ItensLista.objects.all()[0].produto, 'Tomate')

    def test_insert_item_quantidade(self):
        self.assertEqual(ItensLista.objects.all()[0].quantidade, '1kg')


class TestInsertItemListaSemQuantide(TestCase):
    def setUp(self):
        views._insert_item_lista(command='tomate')

    def test_insert_item_descricao(self):
        self.assertEqual(ItensLista.objects.all()[0].produto, 'Tomate')

    def test_insert_item_quantidade(self):
        self.assertEqual(ItensLista.objects.all()[0].quantidade, '')


class TestInsertItemListaProdutoComEspaco(TestCase):
    def setUp(self):
        views._insert_item_lista(command='Coco Ralado')

    def test_insert_item_descricao_com_espaco(self):
        self.assertEqual(ItensLista.objects.all()[0].produto, 'Coco Ralado')


class TestLista(TestCase):
    def setUp(self):
        self.obj = ItensLista.objects.bulk_create([
            ItensLista(produto='Tomate', categoria='horti'),
            ItensLista(produto='Cebola', categoria='horti'),
            ItensLista(produto='Carne Moída', categoria='carnes',
                       quantidade='2'),
        ])

    def test_retorno_lista(self):
        expected = '\n\n*CARNES*\n - Carne Moída 2\n\n*HORTI*\n - Tomate\n - Cebola\n'
        self.assertEqual(views._display_lista(), expected)
