from django.db import models
from django.contrib.auth.models import User

class Solicitud(models.Model):
    # Opciones para categoría y estado según la evaluación
    CATEGORIA_CHOICES = [
        ('Hardware', 'Hardware'),
        ('Software', 'Software'),
        ('Redes', 'Redes'),
    ]
    
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En proceso', 'En proceso'),
        ('Resuelta', 'Resuelta'),
    ]

    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='Pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return f"{self.titulo} ({self.estado})"