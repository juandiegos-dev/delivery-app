from django.shortcuts import render
from rest_framework import generics
from accesos.permissions import rol_requerido
from catalogo.models import Restaurante
from catalogo.serializers import ProductoSerializer, RestauranteSerializer
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import SAFE_METHODS, AllowAny
from catalogo.models import Producto, Restaurante

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
    
class ProductoCrearView(generics.CreateAPIView):
    serializer_class = ProductoSerializer
    permission_classes = [rol_requerido("restaurante")]

    def perform_create(self, serializer):
        restaurante = get_object_or_404(Restaurante, pk=self.kwargs["restaurante_id"])
        if restaurante.dueno != self.request.user:
            raise PermissionDenied("No puede modificar el menú de otro restaurante")
        serializer.save(restaurante=restaurante)    