from rest_framework import viewsets, permissions
from .models import Solicitud
from .serializers import SolicitudSerializer
from .permissions import EsAdminOPropietario

class SolicitudViewSet(viewsets.ModelViewSet):
    serializer_class = SolicitudSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdminOPropietario]

    def get_queryset(self):
        user = self.request.user
        # Si es admin, ve todas las solicitudes. Si es usuario normal, solo ve las suyas.
        if user.is_staff:
            return Solicitud.objects.all().order_by('-fecha_creacion')
        return Solicitud.objects.filter(usuario=user).order_by('-fecha_creacion')

    def perform_create(self, serializer):
        # Asigna automáticamente el usuario autenticado al crear la solicitud
        serializer.save(usuario=self.request.user)

    def perform_update(self, serializer):
        user = self.request.user
        # Si el usuario NO es staff y está intentando cambiar el campo 'estado', lo bloqueamos
        if not user.is_staff:
            # Comparamos si en la petición se intenta enviar un estado distinto al actual
            estado_actual = serializer.instance.estado
            nuevo_estado = self.request.data.get('estado', estado_actual)
            if nuevo_estado != estado_actual:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("No tienes permisos para modificar el estado de la solicitud.")
        
        serializer.save()