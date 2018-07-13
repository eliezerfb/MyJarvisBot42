"""
Baseado em:
https://khashtamov.com/en/how-to-create-a-telegram-bot-using-python/
"""

import json
import telepot
from datetime import datetime
from functools import partial

from django.template.loader import render_to_string
from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

from myjarvisbot.jarvis.models import ItensLista



TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)

def _display_help():
    return render_to_string('help.md')

def _start(username, chat_id):
    return _display_help()


def _insert_item_lista(data):
    produto = data.split(',')
    quantidade = '' if len(produto) < 2 else produto[1].strip()
    semana = datetime.today().isocalendar()[1]
    ano = datetime.today().year

    ItensLista.objects.update_or_create(
        produto=produto[0].strip().title(),
        semana=semana,
        ano=ano,
        defaults={'quantidade': quantidade},
    )
    return 'Ok, anotado!'


def _display_lista():
    itens_lista = ItensLista.objects.filter(
        semana=datetime.today().isocalendar()[1],
        ano=datetime.today().year
    )
    itens_lista = ItensLista.objects.order_by('categoria',)
    lista, categoria_ant = [], ''

    for item in itens_lista:
        categoria = '\n\n*{}*'.format(item.categoria.upper())
        categoria = '' if categoria == categoria_ant else categoria
        if categoria != '':
            categoria_ant = categoria

        quantidade = item.quantidade
        if item.quantidade != '':
            quantidade = ' {}'.format(item.quantidade.strip())

        item_dict = dict(categoria=categoria,
                         produto='\n - {}'.format(item.produto),
                         quantidade=quantidade)

        lista.append(item_dict)

    return render_to_string('lista.md', {'items': lista})


class CommandReceiveView(View):
    def post(self, request, bot_token):
        if bot_token != settings.TELEGRAM_BOT_TOKEN:
            return HttpResponseForbidden('Invalid token')


        raw = request.body.decode('utf-8')

        try:
            payload = json.loads(raw)
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
        else:
            chat_id = payload['message']['chat']['id']
            username = payload['message']['from']['username']
            cmd = payload['message'].get('text')  # command

            msg = ' '.join(cmd.split()[1:])

            commands = {
                '/start': partial(_start, username=username, chat_id=chat_id),
                'help': _display_help,
                'lista': _display_lista,
                'compra': partial(_insert_item_lista, data=msg),
                'comprar': partial(_insert_item_lista, data=msg),
            }

            func = commands.get(cmd.split()[0].lower())

            if func:
                TelegramBot.sendMessage(chat_id, func(), parse_mode='Markdown')
            else:
                TelegramBot.sendMessage(chat_id,
                                        'Desculpe! eu não entendi :-(')

        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)
