from rest_framework import serializers
from .models import Documento, Template, FileU
from django.contrib.auth.models import User
#from rest_framework import permissions
from .models import Template


class DocumentoSerializer(serializers.ModelSerializer): # Define una clase DocumentoSerializer que hereda de serializers.ModelSerializer
    
    fecha_creacion = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%fZ")
    fecha_modificacion = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%fZ")
    class Meta:                                         # Define una clase Meta que contiene la información del modelo Documento
        model = Documento
        fields = ['id', 'titulo', 'contenido', 'usuario', 'fecha_creacion', 'fecha_modificacion']   # Define los campos que se incluirán en la serialización

# Para evitar que se repitan los títulos de los documentos, puedes agregar una validación personalizada al campo título:
    def validate_titulo(self, value):
        if not value:
            raise serializers.ValidationError("El título no puede estar vacío.")
        if Documento.objects.filter(titulo=value).exists():
            raise serializers.ValidationError("Un documento con este título ya existe.")
        return value

class UserSerializer(serializers.ModelSerializer):      # Define una clase UserSerializer que hereda de serializers.ModelSerializer
    documentos = serializers.PrimaryKeyRelatedField(many=True, queryset=Documento.objects.all())    # Define un campo documentos que establece una relación de clave foránea con el modelo Documento
    #documentos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  
    class Meta:
        model = User
        fields = ['id', 'username', 'documentos']   # fields = ['id', 'username', 'email']  # Ajusta según lo que quieras exponer

"""Define un serializador para tu modelo de documento que incluya el archivo"""
class FileSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Documento
        fields = ('titulo', 'archivo')

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ['id', 'title', 'content']

class FileUploadSerializer(serializers.Serializer):
    class Meta:
        model = FileU
        fields = ['file', 'title', 'content']

    file = serializers.FileField()  # Define un campo file que será un archivo
    title = serializers.CharField(max_length=100)  # Define un campo title que será una cadena de texto
    content = serializers.CharField()  # Define un campo content que será una cadena de texto