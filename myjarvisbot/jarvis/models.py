from datetime import datetime
from django.db import models


class ItensLista(models.Model):
    semana = models.PositiveSmallIntegerField(
        default=datetime.today().isocalendar()[1]
    )
    ano = models.PositiveSmallIntegerField(default=datetime.today().year)
    produto = models.CharField(max_length=20)
    quantidade = models.CharField(max_length=10, default='')
