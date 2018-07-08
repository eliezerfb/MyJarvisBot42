from django.urls import path
from myjarvisbot.hello.views import CommandReceiveView


urlpatterns = [
    path('<str:bot_token>/', CommandReceiveView.as_view(), name='command'),
]
