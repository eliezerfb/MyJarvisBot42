from datetime import datetime
from django.db import models


class ItensLista(models.Model):
    semana = models.PositiveSmallIntegerField(
        default=datetime.today().isocalendar()[1]
    )
    ano = models.PositiveSmallIntegerField(default=datetime.today().year)
    produto = models.CharField(max_length=50)
    quantidade = models.CharField(max_length=10, default='', blank=True)
    categoria = models.CharField(max_length=10, default='', blank=True)

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
