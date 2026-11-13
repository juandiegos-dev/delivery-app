from django.urls import path

from catalogo import views

urlpatterns = [
    path("restaurantes/", views.RestauranteListaCrearView.as_view()),
    path("restaurantes/<int:restaurante_id>/menu/", views.MenuView.as_view()),
]