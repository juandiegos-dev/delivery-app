from django.urls import path

from pedidos import views
from pedidos.vistas_cancelaciones import CancelarPedidoView
from pedidos.vistas_fallos import FallarPedidoView

urlpatterns = [
    path("", views.PedidoCrearView.as_view()),
    path("mis-pedidos/", views.MisPedidosView.as_view()),
    path("recibidos/", views.PedidosRecibidosView.as_view()),
    path("<int:pk>/estado/", views.CambiarEstadoView.as_view()),
    path("<int:pk>/cancelar/", CancelarPedidoView.as_view()),
    path("<int:pk>/fallido/", FallarPedidoView.as_view()),
    path("<int:pk>/", views.PedidoDetalleView.as_view()),
]
