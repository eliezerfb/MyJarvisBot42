from datetime import datetime

from django.db import models


class ItensLista(models.Model):
    CEREAIS = 10
    MERCEARIA = 20
    FRIOS = 30
    PADARIA = 35
    HORTIFRUTI = 40
    CARNES = 50
    HIGIENE = 60
    LIMPEZA = 70
    BEBIDAS = 80
    OUTROS = 90
    SECOES = (
        (CEREAIS, 'Cereais'),
        (MERCEARIA, 'Mercearia'),
        (FRIOS, 'Frios'),
        (PADARIA, 'Padaria'),
        (HORTIFRUTI, 'Hortifruti'),
        (CARNES, 'Carnes'),
        (HIGIENE, 'Higiene'),
        (LIMPEZA, 'Limpeza'),
        (BEBIDAS, 'Bebidas'),
        (OUTROS, 'Outros')
    )
    semana = models.PositiveSmallIntegerField(
        default=int(datetime.today().strftime('%U'))
    )
    ano = models.PositiveSmallIntegerField(default=datetime.today().year)
    produto = models.CharField(max_length=50)
    quantidade = models.CharField(max_length=10, default='', blank=True)
    secao = models.PositiveSmallIntegerField(
        'seção', choices=SECOES, blank=True, default=OUTROS
    )

    class Meta:
        verbose_name_plural = 'itens da lista'
        verbose_name = 'item da lista'

    def __str__(self):
        return self.produto.title()


class UsersTelegram(models.Model):
    name = models.CharField(max_length=50, blank=True)
    chat_id = models.CharField(max_length=10)

    def __str__(self):
        return self.name
