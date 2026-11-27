from rest_framework import serializers
from repartidores.models import Asignacion, PerfilRepartidor, PuntoRestaurante

class CoordenadasSerializer(serializers.Serializer):
    latitud = serializers.FloatField(min_value=-90, max_value=90)
    longitud = serializers.FloatField(min_value=-180, max_value=180)

class MiUbicacionSerializer(CoordenadasSerializer):
    disponible = serializers.BooleanField(required=False)

class PerfilRepartidorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilRepartidor
        fields = ["latitud", "longitud", "disponible", "actualizado_en"]
        read_only_fields = fields

class PuntoRestauranteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PuntoRestaurante
        fields = ["latitud", "longitud"]
        read_only_fields = fields

class AsignacionSerializer(serializers.ModelSerializer):
    repartidor_username = serializers.CharField(source="repartidor.username", read_only=True)

    class Meta:
        model = Asignacion
        fields = ["pedido", "repartidor", "repartidor_username", "distancia_km", "fecha_asignacion"]
        read_only_fields = fields