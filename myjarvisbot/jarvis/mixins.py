from django.template.loader import render_to_string

from myjarvisbot.jarvis.models import ItensLista


class ListaMixin:
    @staticmethod
    def display_lista():
        itens_lista = ItensLista.objects.lista_da_semana()
        lista, secao_ant = [], ''

        for item in itens_lista:
            secao = '\n\n*{}*'.format(item.get_secao_display().upper())
            secao = '' if secao == secao_ant else secao
            if secao != '':
                secao_ant = secao

            quantidade = item.quantidade
            if item.quantidade != '':
                quantidade = ' {}'.format(item.quantidade.strip())

            item_dict = dict(secao=secao,
                             produto='\n - {}'.format(item.produto),
                             quantidade=quantidade)

            lista.append(item_dict)

        return render_to_string('lista.md', {'items': lista})