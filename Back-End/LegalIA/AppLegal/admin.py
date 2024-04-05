# El archivo admin.py se utiliza para hacer que tus modelos sean accesibles a través del sitio 
# de administración de Django. Esto es muy útil para crear, leer, actualizar y eliminar (CRUD) 
# registros de tus modelos directamente desde una interfaz web generada automáticamente por Django
from django.contrib import admin
from .models import Documento, Template  # Asegúrate de importar los modelos correctamente

# Registro simple de modelos sin personalización
#admin.site.register(Documento)
#admin.site.register(Template)

# Si deseas personalizar la interfaz de admin, puedes definir clases ModelAdmin
@admin.register(Documento)  # Decorador para registrar el modelo con la clase ModelAdmin personalizada
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'fecha_creacion')  # Ejemplo de personalización
    search_fields = ('titulo', 'contenido')  # Permite buscar por título y contenido

@admin.register(Template)   # Decorador para registrar el modelo con la clase ModelAdmin personalizada
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'fecha_creacion')
    search_fields = ('title', 'content')
