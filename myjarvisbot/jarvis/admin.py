from django.contrib import admin
from myjarvisbot.jarvis.models import ItensLista, UsersTelegram


class ItensListaModelAdmin(admin.ModelAdmin):
    list_display = ['produto', 'secao', 'semana', 'ano']

admin.site.register(ItensLista, ItensListaModelAdmin)
admin.site.register(UsersTelegram)
