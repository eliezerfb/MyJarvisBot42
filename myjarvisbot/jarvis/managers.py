from django.db import models
from datetime import datetime


class ListaDaSemanaQuerySet(models.QuerySet):
    TODAY = datetime.today()

    def _get_semana_ano(self):
        semana = self.TODAY.strftime('%U')
        ano = self.TODAY.strftime('%Y')
        return semana, ano

    def lista_da_semana(self):
        semana, ano = self._get_semana_ano()
        return self.filter(semana=semana,
                           ano=ano).order_by('secao', 'produto')


ListaDaSemanaManager = models.Manager.from_queryset(ListaDaSemanaQuerySet)
