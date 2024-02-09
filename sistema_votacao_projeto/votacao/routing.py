
from .consumers import PresencaConsumer
from channels.routing import URLRouter

from django.urls import re_path



websocket_urlpatterns = [
    re_path(
        r'ws/manage_presenca/(?P<reuniao_id>\w+)/$', PresencaConsumer.as_asgi(),
    ),
    re_path(
        r'ws/manage_presenca/$', PresencaConsumer.as_asgi(),  # rota sem reuniao_id
    ),
]


