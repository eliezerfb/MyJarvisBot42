import json
import telepot
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

from myjarvisbot.jarvis.models import Lista, ItensLista


TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)

def _display_help():
    return render_to_string('help.md')


def _insert_item_lista(command):
    produto = command.split(',')
    quantidade = '' if len(produto) < 2 else produto[1].strip()
    obj = ItensLista(produto=produto[0], quantidade=quantidade)
    obj.save()

# def _display_planetpy_feed():
#     return 'Feed'


class CommandReceiveView(View):
    def post(self, request, bot_token):
        if bot_token != settings.TELEGRAM_BOT_TOKEN:
            return HttpResponseForbidden('Invalid token')

        commands = {
            '/start': _display_help,
            'help': _display_help
            # 'feed': _display_planetpy_feed,
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
            elif cmd.split()[0].strip() == 'compra':
                _insert_item_lista(cmd.split()[1:])
                TelegramBot.sendMessage(chat_id, 'Ok, anotado!')
            else:
                TelegramBot.sendMessage(chat_id,
                                        'I do not understand you, Sir!')

        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)
