"""Configuration WSGI du projet ``acronyme``.

Expose la callable WSGI sous la variable de module ``application``,
attendue par les serveurs WSGI (Gunicorn, uWSGI, Apache mod_wsgi…).

Pour plus d'informations, voir la documentation Django :
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
