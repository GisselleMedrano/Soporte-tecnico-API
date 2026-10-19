from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Solicitud

class SolicitudApiTests(APITestCase):
    def setUp(self):
        # 1. Crear usuarios de prueba según la configuración de la evaluación
        self.admin_user = User.objects.create_superuser(
            username='Valeria', 
            password='Inacap2026'
        )
        self.normal_user = User.objects.create_user(
            username='Usuario1', 
            password='Inacap2025'
        )
        self.otro_usuario = User.objects.create_user(
            username='Usuario2', 
            password='Inacap2025'
        )

        # 2. Crear una solicitud inicial para el usuario normal
        self.solicitud_normal = Solicitud.objects.create(
            titulo='Falla en impresora del piso 2',
            descripcion='No imprime documentos PDF.',
            categoria='Hardware',
            usuario=self.normal_user
        )

        self.url_list = '/api/solicitudes/'

    def test_crear_solicitud_valida(self):
        """Escenario 1: Usuario autenticado registra una solicitud válida (201 Created)"""
        self.client.login(username='Usuario1', password='Inacap2025')
        data = {
            'titulo': 'Error de conexion VPN',
            'descripcion': 'No se puede conectar a la red corporativa.',
            'categoria': 'Redes'
        }
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['usuario'], self.normal_user.id)

    def test_usuario_consulta_solo_sus_solicitudes(self):
        """Escenario 2 y 3: Usuario consulta sus solicitudes y se aísla de las ajenas (404)"""
        # Crear solicitud de otro usuario
        Solicitud.objects.create(
            titulo='Problema ajeno',
            descripcion='Secreto',
            categoria='Software',
            usuario=self.otro_usuario
        )

        self.client.login(username='Usuario1', password='Inacap2025')
        response = self.client.get(self.url_list)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Solo debe ver 1 solicitud (la suya propia)
        self.assertEqual(len(response.data), 1)

        # Intentar consultar el detalle de una solicitud ajena por ID debe dar 404 Not Found
        url_detalle = f"{self.url_list}{self.solicitud_normal.id + 1}/"
        response_detalle = self.client.get(url_detalle)
        self.assertEqual(response_detalle.status_code, status.HTTP_404_NOT_FOUND)

    def test_usuario_normal_no_puede_cambiar_estado(self):
        """Escenario 4: Usuario normal intenta cambiar el estado (rechazado)"""
        self.client.login(username='Usuario1', password='Inacap2025')
        url_detalle = f"{self.url_list}{self.solicitud_normal.id}/"
        
        data = {'estado': 'Resuelta'}
        response = self.client.patch(url_detalle, data, format='json')
        
        # Debe ser rechazado por seguridad (403 Forbidden o 400 Bad Request)
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    def test_administrador_cambia_estado_y_elimina(self):
        """Escenario 5 y 7: Administrador cambia estado (200) y elimina registro (204)"""
        self.client.login(username='Valeria', password='Inacap2026')
        url_detalle = f"{self.url_list}{self.solicitud_normal.id}/"
        
        # Cambiar estado como administrador
        data = {'estado': 'En proceso'}
        response_patch = self.client.patch(url_detalle, data, format='json')
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        
        # Eliminar registro como administrador
        response_delete = self.client.delete(url_detalle)
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

    def test_datos_invalidos_retornan_400(self):
        """Escenario 6: Usuario envía datos inválidos o vacíos (400 Bad Request)"""
        self.client.login(username='Usuario1', password='Inacap2025')
        data = {
            'titulo': 'ABC', # Demasiado corto según la validación del serializer
            'descripcion': '',
            'categoria': 'Invalida'
        }
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)