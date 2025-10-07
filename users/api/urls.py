# Importación de path para definición de rutas URL
from django.urls import path
# Importación de vistas personalizadas para gestión de usuarios
from .views import UserRegisterView, UserView
# Importación de vistas JWT de SimpleJWT para autenticación por tokens
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Configuración de rutas URL para la API de usuarios
urlpatterns = [
    # Endpoint para registro de nuevos usuarios
    # POST: Crear cuenta nueva con email, username, password
    path('auth/register/', UserRegisterView.as_view(), name='register_user'),
    
    # Endpoint para gestión del perfil del usuario autenticado
    # GET: Obtener datos del usuario actual
    # PATCH: Actualizar datos del perfil
    # DELETE: Eliminar cuenta con validación de contraseña
    path('auth/me/', UserView.as_view(), name='data_user'),
    
    # Endpoint para obtener tokens JWT (login)
    # POST: Autenticación con email/password, retorna access y refresh token
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Endpoint para renovar access token usando refresh token
    # POST: Envía refresh token válido, recibe nuevo access token
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]