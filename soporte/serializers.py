from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from .models import Solicitud

class SolicitudSerializer(serializers.ModelSerializer):
    # Campos que se muestran en lectura pero se protegen en escritura
    usuario_nombre = serializers.ReadOnlyField(source='usuario.username')

    class Meta:
        model = Solicitud
        fields = ['id', 'titulo', 'descripcion', 'categoria', 'estado', 'fecha_creacion', 'usuario', 'usuario_nombre']
        read_only_fields = ['id', 'fecha_creacion', 'usuario']

    def validate_titulo(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("El título de la solicitud debe tener al menos 5 caracteres.")
        return value

    def validate(self, attrs):
        # 1. Obtener el usuario desde el request
        user = self.context["request"].user

        # 2. Si el usuario no es staff y se envió el campo 'estado'
        if not user.is_staff and "estado" in attrs:
            # Calcular estado actual
            estado_actual = self.instance.estado if self.instance else "Pendiente"

            # Si el estado enviado es distinto del actual, bloquear
            if attrs["estado"] != estado_actual:
                raise PermissionDenied("No tienes permisos para modificar el estado de la solicitud.")

        # 3. Retornar los atributos procesados
        return attrs