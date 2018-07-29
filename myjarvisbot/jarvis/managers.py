from django.db import models
from myjarvisbot.utils.semana_ano import get_semana_ano


class ListaDaSemanaQuerySet(models.QuerySet):
    def lista_da_semana(self):
        semana, ano = get_semana_ano()
        return self.filter(semana=semana,
                           ano=ano).order_by('secao', 'produto')


ListaDaSemanaManager = models.Manager.from_queryset(ListaDaSemanaQuerySet)
