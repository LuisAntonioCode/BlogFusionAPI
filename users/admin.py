# Importación del módulo admin de Django para panel de administración
from django.contrib import admin
# Importación de UserAdmin base para heredar funcionalidad estándar de usuarios
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Importación del modelo User 
from .models import User

@admin.register(User) # Decorator para registrar automáticamente el modelo en admin
class UserAdmin(BaseUserAdmin):
    '''
    Al usar 'pass', mantenemos toda la funcionalidad por defecto sin 
    modificaciones adicionales, lo cual es apropiado para un modelo User
    que sigue las convenciones estándar de Django.
    '''
    pass # Hereda toda la funcionalidad de BaseUserAdmin sin modificaciones

