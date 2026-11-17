from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Administración de Django
    path("admin/", admin.site.urls),

    # Autenticación
    path("api-auth/", include("rest_framework.urls")),
    path("api/auth/", include("accesos.urls")),

    # Catálogo de restaurantes y productos
    path("api/", include("catalogo.urls")),

    # Gestión de pedidos
    path("api/pedidos/", include("pedidos.urls")),
]