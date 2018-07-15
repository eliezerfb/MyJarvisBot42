from datetime import datetime
from django.db import models


class ItensLista(models.Model):
    SECOES = (
        (10, 'Cereais'),
        (20, 'Mercearia'),
        (30, 'Frios'),
        (40, 'Hortifruti'),
        (50, 'Carnes'),
        (60, 'Higiene'),
        (70, 'Limpeza'),
        (80, 'Bebidas'),
        (90, 'Outros')
    )
    semana = models.PositiveSmallIntegerField(
        default=int(datetime.today().strftime('%U'))
    )
    ano = models.PositiveSmallIntegerField(default=datetime.today().year)
    produto = models.CharField(max_length=50)
    quantidade = models.CharField(max_length=10, default='', blank=True)
    categoria = models.CharField(max_length=10, default='', blank=True)
    secao = models.PositiveSmallIntegerField(
        'seção', choices=SECOES, blank=True, default=90
    )

    class Meta:
        verbose_name_plural = 'itens da lista'
        verbose_name = 'item da lista'

    def __str__(self):
        return self.produto.title()


class UsersTelegram(models.Model):
    username = models.CharField(max_length=20)
    chat_id = models.CharField(max_length=10)

    def __str__(self):
        return self.username
