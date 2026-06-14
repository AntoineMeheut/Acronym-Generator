"""Configuration ASGI du projet ``acronyme``.

Expose la callable ASGI sous la variable de module ``application``,
attendue par les serveurs ASGI (Daphne, Uvicorn, Hypercorn…).

Pour plus d'informations, voir la documentation Django :
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()
