"""
ASGI config for sistema_votacao_projeto project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

# ... o restante do código ASGI, como a configuração dos protocolos e a criação da aplicação final


import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_votacao_projeto.settings')

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack   
import votacao.routing


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            votacao.routing.websocket_urlpatterns
        )
    )
})



