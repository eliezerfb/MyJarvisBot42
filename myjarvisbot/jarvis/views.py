"""
Baseado em:
https://khashtamov.com/en/how-to-create-a-telegram-bot-using-python/
"""

import json
from functools import partial

import telepot
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from myjarvisbot.jarvis.mixins import ListaComprasMixin, BotMixin

TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)


class CommandReceiveView(ListaComprasMixin, BotMixin, View):
    def post(self, request, bot_token):
        if bot_token != settings.TELEGRAM_BOT_TOKEN:
            return HttpResponseForbidden('Invalid token')

        raw = request.body.decode('utf-8')

        try:
            payload = json.loads(raw)
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
        else:
            print(payload)
            chat_id = payload['message']['chat']['id']
            name = payload['message']['chat']['first_name']
            cmd = payload['message'].get('text')  # command

            msg = ' '.join(cmd.split()[1:])

            commands = {
                '/start': partial(self.start, name=name, chat_id=chat_id),
                'help': self.display_help,
                'lista': self.display_lista_compras,
                'compra': partial(self.insert_item_lista, data=msg),
                'comprar': partial(self.insert_item_lista, data=msg),
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
