from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from accesos.permissions import rol_requerido
from catalogo.models import Restaurante
from catalogo.serializers import ProductoSerializer, RestauranteSerializer

# Create your views here.

class RestauranteListaCrearView(generics.ListCreateAPIView):
    queryset = Restaurante.objects.order_by("nombre")
    serializer_class = RestauranteSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [rol_requerido("restaurante")()]
        return [AllowAny()]

    def perform_create(self, serializer):
        if Restaurante.objects.filter(dueno=self.request.user).exists():
            raise ValidationError("Este usuario ya tiene un restaurante registrado")
        serializer.save(dueno=self.request.user)


class MenuView(generics.ListAPIView):
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        restaurante = get_object_or_404(Restaurante, pk=self.kwargs["restaurante_id"])
        return restaurante.productos.filter(disponible=True).order_by("nombre")