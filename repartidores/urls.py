from django.urls import path
from repartidores import views
from repartidores.vistas_entregas import (IniciarRepartoView, ConfirmarEntregaView, MisAsignacionesView)
from repartidores.vistas_gps import RutaPedidoView

urlpatterns = [
    path("mi-ubicacion/", views.MiUbicacionView.as_view()),
    path("mis-asignaciones/", MisAsignacionesView.as_view()),
    path("restaurantes/<int:restaurante_id>/ubicacion/", views.PuntoRestauranteView.as_view()),
    path("pedidos/<int:pedido_id>/asignacion/", views.AsignacionDetalleView.as_view()),
    path("pedidos/<int:pedido_id>/ubicacion/", views.UbicacionAsignadaView.as_view()),
    path("pedidos/<int:pedido_id>/ruta/", RutaPedidoView.as_view()),
    path("pedidos/<int:pedido_id>/iniciar-reparto/", IniciarRepartoView.as_view()),
    path("pedidos/<int:pedido_id>/confirmar-entrega/", ConfirmarEntregaView.as_view()),
]