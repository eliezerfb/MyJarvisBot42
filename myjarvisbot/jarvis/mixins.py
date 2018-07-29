from django.template.loader import render_to_string

from myjarvisbot.jarvis.models import ItensLista
from myjarvisbot.jarvis.models import UsersTelegram
from myjarvisbot.utils.semana_ano import get_semana_ano


class BotMixin:
    def display_help(self):
        return render_to_string('help.md')

    def start(self, name, chat_id):
        UsersTelegram.objects.update_or_create(
            name=name,
            defaults={'chat_id': chat_id}
        )
        return self.display_help()


class ListaComprasMixin:
    def display_lista_compras(self):
        itens_lista = ItensLista.objects.lista_da_semana()
        lista, secao_ant = [], ''

        for item in itens_lista:
            secao = '\n\n*{}*'.format(item.get_secao_display())
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

    def insert_item_lista(self, data):
        produto = data.split(',')
        quantidade = '' if len(produto) < 2 else produto[1].strip()
        semana, ano = get_semana_ano()
        secao = ItensLista.OUTROS

        produto = produto[0].strip().title()

        ultimo_item_lista = ItensLista.objects.all().filter(produto=produto)
        ultimo_item_lista = ultimo_item_lista.order_by('-ano', '-semana')
        if ultimo_item_lista:
            secao = ultimo_item_lista.first().secao

        ItensLista.objects.update_or_create(
            produto=produto,
            semana=semana,
            ano=ano,
            defaults={'quantidade': quantidade,
                      'secao': secao},
        )
        return 'Ok, anotado!'
