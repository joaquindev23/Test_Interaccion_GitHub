#Creada por defecto

"""
Configuración de URL para el proyecto LegalIA.

La lista `urlpatterns` dirige las URL a las vistas. Para obtener más información, consulte:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Ejemplos:

--> Vistas de funciones

    1. Agregue una importación: desde las vistas de importación de my_app
    2. Agregue una URL a urlpatterns: ruta('', views.home, nombre='home')

--> Vistas basadas en clases

    1. Agregue una importación: desde other_app.views import Inicio
    2. Agregue una URL a urlpatterns: ruta('', Home.as_view(), nombre='home')

--> Incluyendo otra URLconf

    1. Importe la función include(): desde django.urls importe include, ruta
    2. Agregue una URL a urlpatterns: ruta('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from AppLegal.views import home_view    # Importamos la vista home_view.
#from AppLegal.views import GenerateTextView, DocumentSummaryView, TextClassificationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('AppLegal.urlsapp')),  # Organiza bajo el prefijo 'api/',
    path('', home_view, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
