from django.urls import path
from frontend import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("login/", views.login, name="login"),
    path("registro/", views.registro, name="registro"),
    path("restaurantes/", views.restaurantes, name="restaurantes"),
    path("mis-pedidos/", views.mis_pedidos, name="mis_pedidos"),
    path("panel-restaurante/", views.panel_restaurante, name="panel_restaurante"),
    path("panel-repartidor/", views.panel_repartidor, name="panel_repartidor"),
    path("ubicacion/", views.ubicacion, name="ubicacion"),
    path("seguimiento/<int:pedido_id>/", views.seguimiento, name="seguimiento"),
]