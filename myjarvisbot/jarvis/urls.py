from django.urls import path
from myjarvisbot.jarvis.views import CommandReceiveView


urlpatterns = [
    path('<str:bot_token>/', CommandReceiveView.as_view(), name='command'),
]
