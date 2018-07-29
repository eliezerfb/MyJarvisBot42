from datetime import datetime

from django.db import models

from myjarvisbot.jarvis.managers import ListaDaSemanaManager
from myjarvisbot.utils.semana_ano import get_semana_ano

SEMANA, ANO = get_semana_ano()


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
        (CEREAIS, 'CEREAIS'),
        (MERCEARIA, 'MERCEARIA'),
        (FRIOS, 'FRIOS'),
        (PADARIA, 'PADARIA'),
        (HORTIFRUTI, 'HORTIFRUTI'),
        (CARNES, 'CARNES'),
        (HIGIENE, 'HIGIENE'),
        (LIMPEZA, 'LIMPEZA'),
        (BEBIDAS, 'BEBIDAS'),
        (OUTROS, 'OUTROS')
    )
    semana = models.PositiveSmallIntegerField(default=SEMANA)
    ano = models.PositiveSmallIntegerField(default=ANO)
    produto = models.CharField(max_length=50)
    quantidade = models.CharField(max_length=10, default='', blank=True)
    secao = models.PositiveSmallIntegerField(
        'seção', choices=SECOES, blank=True, default=OUTROS
    )

    objects = ListaDaSemanaManager()

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
