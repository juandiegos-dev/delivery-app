from django.urls import path

from catalogo import views

urlpatterns = [
    path("restaurantes/", views.RestauranteListaCrearView.as_view()),
    path("restaurantes/<int:restaurante_id>/menu/", views.MenuView.as_view()),
    path("restaurantes/<int:restaurante_id>/productos/", views.ProductoCrearView.as_view()),
    path("productos/<int:pk>/", views.ProductoDetalleView.as_view()),
]