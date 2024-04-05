#Creada por defecto

"""
Configuración WSGI para el proyecto LegalIA.

Expone el WSGI invocable como una variable a nivel de módulo denominada ``application``.

Para obtener más información sobre este archivo, consulte
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""


import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectlegal.settings')

application = get_wsgi_application()
