# API REST - Gestión de Soporte Técnico

API RESTful desarrollada con Django y Django REST Framework para gestionar solicitudes de soporte técnico mediante autenticación por sesión y control de acceso por perfil.

## Características

- Autenticación por sesión (SessionAuthentication) con validación CSRF en operaciones de escritura.
- Control de permisos en servidor con el permiso personalizado EsAdminOPropietario.
- Administradores (is_staff): acceso total a todas las solicitudes, modificación de estados y eliminación de registros.
- Usuarios normales: creación de solicitudes y consulta de registros propios. Pueden modificar titulo, descripcion y categoria, pero no el estado ni eliminar.
- Solicitudes ajenas responden 404 Not Found para no revelar existencia de datos.
- Campos protegidos asignados en servidor: id, usuario y fecha_creacion.

## Tecnologías

- Python 3
- Django 6.1.2
- Django REST Framework 3.18.3
- SQLite

## Instalación y ejecución (Windows / PowerShell)

1. Clonar el repositorio:

git clone [https://github.com/GisselleMedrano/Soporte-tecnico-API](https://github.com/GisselleMedrano/Soporte-tecnico-API)
cd Soporte-tecnico-API