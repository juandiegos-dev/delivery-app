from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/auth/", include("accesos.urls")),
    path("api/", include("catalogo.urls")),
    path("api/pedidos/", include("pedidos.urls")),
    path("api/repartidores/", include("repartidores.urls")),
    path("api/notificaciones/", include("notificaciones.urls")),
    path("", include("frontend.urls")),
]