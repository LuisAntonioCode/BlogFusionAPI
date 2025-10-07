from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthenticatedOwnerOrReadOnly(BasePermission):
    """
    Permiso personalizado para controlar el acceso a publicaciones (Post).
    - Permite realizar operaciones de solo lectura (GET, HEAD, OPTIONS) a cualquier usuario (autenticado o no)
    - Requiere que el usuario esté autenticado para crear nuevos posts.
    - Solo el autor de un post puede actualizarlo o eliminarlo.
    """

    def has_permission(self, request, view):
        # Lectura siempre permitida (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        # El usuario debe estar autenticado
        return bool(request.user and request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        # Lectura siempre permitida (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        # Solo usuarios autenticados puedan (PUT, PATCH, DELETE) sus posts y solo el propietario del post puede modificarlo o eliminarlo
        return obj.user == request.user
