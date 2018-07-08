from datetime import datetime
from django.db import models


# Create your models here.
class Lista(models.Model):
    semana = models.PositiveSmallIntegerField(
        default=datetime.today().isocalendar()[1]
    )
    ano = models.PositiveSmallIntegerField(default=datetime.today().year)


class ItensLista(models.Model):
    produto = models.CharField(max_length=20)
#    quantidade = models.CharField(max_length=10, default='')
