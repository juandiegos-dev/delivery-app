from rest_framework import serializers

from catalogo.models import Producto, Restaurante


class RestauranteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurante
        fields = ["id", "nombre", "direccion"]


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ["id", "restaurante", "nombre", "descripcion", "precio", "disponible"]
        read_only_fields = ["restaurante"]