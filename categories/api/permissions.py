from rest_framework.permissions import BasePermission, SAFE_METHODS  # Importacion de la clase BasePermission y SAFE_METHODS de Django REST Framework

# Permiso personalizado que permite acceso de solo lectura a cualquier usuario
# y acceso completo únicamente a usuarios administradores. 
class IsAdminOrReadOnly(BasePermission):
    # Metodo que determina si el usuario tiene permiso para realizar la accion solicitada
    def has_permission(self, request, view):
        # Acceso libre para métodos de solo lectura (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        # Para otros metodos, solo se permite el acceso a usuarios administradores
        return request.user.is_staff