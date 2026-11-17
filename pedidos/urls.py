from django.urls import path

from pedidos import views

urlpatterns = [
    path("", views.PedidoCrearView.as_view()),
    path("mis-pedidos/", views.MisPedidosView.as_view()),
    path("recibidos/", views.PedidosRecibidosView.as_view()),
    path("<int:pk>/", views.PedidoDetalleView.as_view()),
]