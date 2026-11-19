from django.urls import path
from repartidores import views

urlpatterns = [
    path("mi-ubicacion/", views.MiUbicacionView.as_view()),
    path("restaurantes/<int:restaurante_id>/ubicacion/", views.PuntoRestauranteView.as_view()),
    path("pedidos/<int:pedido_id>/asignacion/", views.AsignacionDetalleView.as_view()),
    path("pedidos/<int:pedido_id>/ubicacion/", views.UbicacionAsignadaView.as_view()),   
]