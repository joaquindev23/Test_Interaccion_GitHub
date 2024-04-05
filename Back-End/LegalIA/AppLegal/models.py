from django.db import models
from django.contrib.auth.models import User
from django.db import models
class Documento(models.Model):              # Define un modelo llamado Documento que hereda de models.Model
    titulo = models.CharField(max_length=255)   # Define un campo de texto llamado titulo
    archivo = models.FileField(upload_to='documentos/', default='documentos/default.txt')   # Define un campo de archivo llamado archivo
    contenido = models.TextField()  # Define un campo de texto llamado contenido
    fecha_creacion = models.DateTimeField(auto_now_add=True)    # Define un campo de fecha y hora llamado fecha_creacion
    fecha_modificacion = models.DateTimeField(auto_now=True)    # Define un campo de fecha y hora llamado fecha_modificacion
    usuario = models.ForeignKey(User, related_name='documentos', on_delete=models.CASCADE)  # Establece una relación de clave foránea con el modelo User, indicando quién creó el documento.
    #usuario = models.ForeignKey(User, on_delete=models.CASCADE) # establece una relación de clave foránea con el modelo User, indicando quién creó el documento.

    def __str__(self):                        # Define un método __str__ que devuelve el título del documento.
        return self.titulo
    
class Template(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    usuario = models.ForeignKey(User, related_name='templates', on_delete=models.CASCADE, null=True, blank=True)  # Opcional, basado en tus necesidades
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    # Omitido: Implementación de categorías o etiquetas para simplicidad
    def __str__(self):
        return self.title

class FileU(models.Model):
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, related_name='uploaded_files', on_delete=models.CASCADE, null=True, blank=True)  # Relaciona cada archivo con un usuario
    descripcion = models.TextField(null=True, blank=True)  # Campo opcional para describir el archivo
    etiquetas = models.CharField(max_length=255, blank=True)  # Etiquetas para mejorar la búsqueda de archivos
    
    def __str__(self):
        return f"{self.file.name} ({self.usuario.username})"
    


"""class User(models.Model):  # Define un modelo llamado User que hereda de models.Model
    username = models.CharField(max_length=100) # Define un campo de texto llamado username
    email = models.EmailField() # Define un campo de correo electrónico llamado email
    password = models.CharField(max_length=20) # Define un campo de texto llamado password
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):  # Define un método __str__ que devuelve el nombre de usuario.
        return self.username
"""     