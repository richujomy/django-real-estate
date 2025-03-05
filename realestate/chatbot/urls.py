from django.urls import path
from chatbot.views import chat_interface, chat_api

urlpatterns = [
    path('chat/', chat_interface, name='chat_interface'),
    path('api/', chat_api, name='chat_api'),
]