from rest_framework.permissions import BasePermission


def rol_requerido(*roles):
    """Crea un permiso que solo deja pasar a usuarios autenticados con alguno de los roles."""

    class PermisoPorRol(BasePermission):
        message = "No tiene permiso para esta acción"

        def has_permission(self, request, view):
            return request.user.is_authenticated and request.user.rol in roles

    return PermisoPorRol