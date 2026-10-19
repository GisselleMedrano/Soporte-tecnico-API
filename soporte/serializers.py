from rest_framework import serializers
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