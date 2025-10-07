# Importacion de Django REST Framework para serialización de datos
from rest_framework import serializers
# Importación del modelo User
from users.models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer para el registro de nuevos usuarios con validación de contraseña"""
    
    # Campo adicional para confirmación de contraseña (no se guarda en BD)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        # Campos que serán procesados en la serialización
        fields = ['id', 'email', 'username', 'password', 'password_confirm']
        # Configuraciones adicionales para campos específicos
        extra_kwargs = {
            'password': {'write_only': True}  # Password nunca se devuelve en respuestas
        }
    
    def validate(self, attrs):
        """Valida que password y password_confirm sean idénticos"""
        # Comparar ambas contraseñas
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        # Retornar datos validados para continuar con el proceso
        return attrs
    
    def create(self, validated_data):
        """
        Método personalizado para crear usuario con contraseña hasheada
        Override del método create() de ModelSerializer
        """
        # Remover password_confirm ya que no existe en el modelo User
        validated_data.pop('password_confirm', None)
        # Extraer password para procesamiento especial
        password = validated_data.pop('password', None)
        
        # Crear instancia de User con datos validados (excepto password)
        instance = self.Meta.model(**validated_data)
        
        # Hashear contraseña usando el método seguro de Django
        if password is not None:
            instance.set_password(password)  # Aplica hash PBKDF2/Argon2
        
        # Guardar usuario en base de datos
        instance.save()
        return instance

class UserDataSerializer(serializers.ModelSerializer):
    """Serializer para mostrar datos completos del usuario (consultas GET)"""
    
    class Meta:
        model = User
        # Campos de solo lectura para respuestas completas de usuario
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'date_joined']

class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer para actualizaciones parciales del usuario """
    
    class Meta:
        model = User
        # Solo campos editables por el usuario (excluye id, date_joined, etc.)
        fields = ['email', 'username', 'first_name', 'last_name']

class UserInfoSerializer(serializers.ModelSerializer):
    """Serializer ligero para información básica del usuario"""
    
    class Meta:
        model = User
        # Campos mínimos para referencias rápidas o datos públicos
        fields = ['email', 'username']

class UserDeleteSerializer(serializers.Serializer):
    """
    Serializer para validación segura de eliminación de cuenta
    No hereda de ModelSerializer porque no interactúa directamente con el modelo
    """
    
    # Campo booleano obligatorio para confirmar intención de eliminación
    confirm_deletion = serializers.BooleanField(required=True)
    # Password para verificar identidad antes de eliminar
    password = serializers.CharField(required=True, write_only=True)
    
    def validate_confirm_deletion(self, value):
        """
        Validador específico para confirm_deletion
        Se ejecuta automáticamente por DRF cuando se valida este campo
        """
        # Rechazar si no se confirma explícitamente la eliminación
        if not value:
            raise serializers.ValidationError("Debe confirmar la eliminación")
        return value
    
    def validate_password(self, value):
        """Verifica que la contraseña ingresada coincida con la del usuario actual"""

        # Obtener usuario actual desde el contexto de la request
        user = self.context['request'].user
        # Usar el método check_password de Django para verificar hash
        if not user.check_password(value):
            raise serializers.ValidationError("Contraseña incorrecta")
        return value