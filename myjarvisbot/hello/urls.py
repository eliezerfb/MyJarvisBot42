from django.urls import path
from myjarvisbot.hello.views import CommandReceiveView


urlpatterns = [
    path('bot/<str:bot_token>/', CommandReceiveView.as_view(), name='command'),
]
