import json
import telepot
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


def _insert_item_lista(command):
    produto = command.split(',')
    quantidade = '' if len(produto) < 2 else produto[1].strip()
    obj = ItensLista(produto=produto[0].title(), quantidade=quantidade)
    obj.save()


def _display_lista():
    itens_lista = ItensLista.objects.all()
    itens_lista = ItensLista.objects.order_by('categoria',)
    lista = []
    categoria_ant = ''
    for item in itens_lista:
        if item not in lista:
            categoria = '*{}*\n'.format(item.categoria.upper())
            if categoria != categoria_ant:
                categoria_ant = categoria
            else:
                categoria = ''

            item_dict = dict(categoria=categoria,
                             produto=item.produto,
                             quantidade=item.quantidade)
        lista.append(item_dict)
    lista = render_to_string('lista.md', {'items': lista})
    return lista.replace('\n\n', '\n')


class CommandReceiveView(View):
    def post(self, request, bot_token):
        if bot_token != settings.TELEGRAM_BOT_TOKEN:
            return HttpResponseForbidden('Invalid token')

        commands = {
            '/start': _display_help,
            'help': _display_help,
            'lista': _display_lista,
        }

        raw = request.body.decode('utf-8')

        try:
            payload = json.loads(raw)
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
        else:
            chat_id = payload['message']['chat']['id']
            cmd = payload['message'].get('text')  # command

            func = commands.get(cmd.split()[0].lower())
            if func:
                TelegramBot.sendMessage(chat_id, func(), parse_mode='Markdown')
            elif cmd.split()[0].strip().lower()[:6] == 'compra':
                TelegramBot.sendMessage(chat_id, 'Ok')
                _insert_item_lista(' '.join(cmd.split()[1:]))
                TelegramBot.sendMessage(chat_id, 'Anotado!')
            else:
                TelegramBot.sendMessage(chat_id,
                                        'Desculpe! eu não entendi :(')

        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)
