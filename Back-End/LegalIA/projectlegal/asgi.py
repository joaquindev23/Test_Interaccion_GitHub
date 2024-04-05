#Creada por defecto



"""
Configuración ASGI para el proyecto LegalIA.

Expone el ASGI invocable como una variable a nivel de módulo denominada ``aplicación``.

Para obtener más información sobre este archivo, consulte
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""


import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectlegal.settings')

application = get_asgi_application()
