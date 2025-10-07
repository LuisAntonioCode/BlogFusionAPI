# Importaciones de Django REST Framework para manejo de API
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
# Importaciones de serializadores personalizados
from users.api.serializers import (
    UserRegisterSerializer, 
    UserDataSerializer, 
    UserUpdateSerializer,
    UserDeleteSerializer
)

class UserRegisterView(APIView):
    """Vista para registro de nuevos usuarios"""
    serializer_class = UserRegisterSerializer
    
    def post(self, request): # Crear nuevo usuario con validación de datos.
        """
        Proceso:
        1. Valida datos de entrada (email, username, passwords)
        2. Crea usuario con contraseña hasheada
        3. Retorna datos del usuario sin información sensible
        """
        # Inicializar serializer con datos de la petición
        serializer = self.serializer_class(data=request.data)
        # Validar datos y lanzar excepción automática si hay errores
        if serializer.is_valid(raise_exception=True):
            # Guardar usuario en base de datos
            user = serializer.save()
            # Preparar respuesta usando serializer seguro (sin contraseña)
            response_data = UserDataSerializer(user).data
            # Retornamos datos sin información sensible
            return Response(response_data, status=status.HTTP_201_CREATED)

class UserView(APIView):
    """
    Vista para operaciones CRUD del usuario autenticado.
    Maneja las operaciones:
    - GET: Consultar datos del perfil
    - PATCH: Actualizar información parcial
    - DELETE: Eliminar cuenta con validaciones de seguridad
    Requiere autenticación JWT válida para todas las operaciones.
    """
    # Solo usuarios autenticados pueden acceder a estos endpoints
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request): # Obtener datos del usuario autenticado
        """
        Retorna información del perfil sin datos sensibles como contraseña.
        Usa request.user que viene del token JWT decodificado.
        """
        # Serializar datos del usuario 
        serializer = UserDataSerializer(request.user)
        # Retornar datos con status 200 OK
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request): # Actualizar datos del usuario autenticado
        """
        Permite actualizaciones parciales (no todos los campos son obligatorios).
        Valida datos antes de persistir cambios en base de datos.
        """
        # Inicializar serializer para actualización de los datos usuario
        serializer = UserUpdateSerializer(
            request.user,  # Instancia del usuario a actualizar
            data=request.data,  # Datos nuevos para actualizar
            partial=True  # Permite actualizaciones parciales
        )
        # Validar y actualizar cambios si los datos son correctos
        if serializer.is_valid(raise_exception=True):
            # Guardar cambios en la base de datos
            serializer.save()
            # Retornar datos actualizados 
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request): # Eliminar cuenta del usuario autenticado con validaciones de seguridad
        """
        Requiere confirmación explícita y contraseña actual para prevenir
        eliminaciones accidentales o maliciosas. Operación irreversible.
        """
        # serializer para Validar datos de confirmación (confirm_deletion=true, password)
        serializer = UserDeleteSerializer(
            data=request.data,  # Datos de confirmación
            context={'request': request} # Contexto para validar contraseña
        )
        # Validar datos y proceder a eliminar si son correctos
        if serializer.is_valid(raise_exception=True):
            user = request.user
            # Guardar información antes de eliminar (para logging/respuesta)
            username = user.username 
            # Eliminar el usuario permanentemente de la base de datos
            user.delete()
            # Retornar mensaje de éxito de eliminación 
            return Response(
                {
                    'message': f'Usuario {username} eliminado exitosamente'
                }, 
                status=status.HTTP_200_OK
            )
        # Si hay errores de validación, se lanzan excepciones automáticas
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)