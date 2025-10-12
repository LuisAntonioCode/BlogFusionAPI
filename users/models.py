# Importación de models para definición de modelos de base de datos
from django.db import models
# Importación de AbstractUser para extender el modelo de usuario por defecto
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser
    que modifica el comportamiento por defecto para usar email como campo de login
    en lugar de username, manteniendo todas las funcionalidades estándar
    de autenticación, permisos y gestión de Django.
    """

    # Override del campo email para hacerlo único (requerido para login)
    email = models.EmailField(unique=True)
    # Configuración para usar email como campo de autenticación principal
    USERNAME_FIELD = 'email'  # Campo usado para login (en lugar de 'username')
    # Solo email y password serán obligatorios
    REQUIRED_FIELDS = []
