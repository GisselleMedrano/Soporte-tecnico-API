from rest_framework import permissions

class EsAdminOPropietario(permissions.BasePermission):
    def has_permission(self, request, view):
        #exigir autenticación
        if not request.user or not request.user.is_authenticated:
            return False
        return True 
    def has_object_permission(self, request, view, obj):
        #administradores is staff con acceso total
        if request.user.is_staff:
            return True

        if request.method == 'DELETE':
            return False

        return obj.usuario == request.user
    