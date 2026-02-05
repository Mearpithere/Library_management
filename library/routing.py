from django.urls import path
from library import consumers


websocket_urlpatterns = [
    path('ws/books/', consumers.BookConsumer.as_asgi()),
]