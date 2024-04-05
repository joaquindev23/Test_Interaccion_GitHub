from rest_framework import permissions
from rest_framework.permissions import BasePermission
from AppLegal.permissions import IsAuthorOrReadOnly

class IsAuthorOrReadOnly(permissions.BasePermission):
    
    #Permiso personalizado para permitir solo a los autores de un objeto editarlo.
    
    def has_object_permission(self, request, view, obj):
        # Los permisos de lectura están permitidos para cualquier solicitud,
        # por lo que siempre permitiremos solicitudes GET, HEAD o OPTIONS.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Los permisos de escritura solo están permitidos al autor del objeto.
        return obj.author == request.user