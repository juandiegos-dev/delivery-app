from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Administración
    path("admin/", admin.site.urls),

    # Autenticación
    path("api-auth/", include("rest_framework.urls")),
    path("api/auth/", include("accesos.urls")),

    # Catálogo
    path("api/", include("catalogo.urls")),

    # Pedidos
    path("api/pedidos/", include("pedidos.urls")),
]