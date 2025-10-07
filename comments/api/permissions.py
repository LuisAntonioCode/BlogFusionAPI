from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthenticatedOwnerOrReadOnly(BasePermission):
    """
    Permiso personalizado para la gestión de comentarios.

    Reglas:
    - Operaciones de solo lectura (GET, HEAD, OPTIONS): permitidas para cualquier usuario, autenticado o no.
    - Operaciones de escritura (POST, PUT, PATCH, DELETE): requieren autenticación.
    - Un usuario autenticado puede crear comentarios.
    - Un usuario solo puede actualizar o eliminar los comentarios que él mismo creó.
    - El autor del post tiene permiso para eliminar (DELETE) cualquier comentario en su propio post.
    """

    # Permisos generales
    def has_permission(self, request, view):
        # Lectura siempre permitida (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        # Requiere usuario debe estar autenticado
        return bool(request.user and request.user.is_authenticated)
    
    # Permisos específicos 
    def has_object_permission(self, request, view, obj):
        # Lectura siempre permitida (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        
        # Permitir si el usuario es el autor del comentario
        # Solo si el usuario esta autenticado pueda (PUT, PATCH, DELETE) su comenario.
        if obj.user == request.user:
            return True

        # Permite al autor del post eliminar comentarios de su propio post
        if request.method == 'DELETE' and obj.post.user == request.user:
            return True
        # En cualquier otro caso, denegar el permiso
        return False