from django.conf import settings
from rest_framework import serializers
from pedidos.models import DetallePedido, Pedido, IncidenciaPedido


class ItemPedidoSerializer(serializers.Serializer):
    producto_id = serializers.IntegerField(min_value=1)
    cantidad = serializers.IntegerField(min_value=1, max_value=settings.CANTIDAD_MAXIMA_POR_PRODUCTO)


class PedidoCrearSerializer(serializers.Serializer):
    restaurante_id = serializers.IntegerField(min_value=1)
    direccion_entrega = serializers.CharField(max_length=255, allow_blank=False)
    observaciones = serializers.CharField(required=False, allow_blank=True)
    items = ItemPedidoSerializer(many=True, allow_empty=False)


class CambioEstadoSerializer(serializers.Serializer):
    estado = serializers.ChoiceField(choices=Pedido.Estado.choices)


class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = ["producto", "nombre_producto", "cantidad", "precio_unitario", "subtotal"]


class IncidenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidenciaPedido
        fields = ["tipo", "motivo", "fecha"]


class PedidoSerializer(serializers.ModelSerializer):
    detalles = DetallePedidoSerializer(many=True, read_only=True)
    incidencias = IncidenciaSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = ["id", "cliente", "restaurante", "direccion_entrega", "observaciones",
                  "estado", "subtotal", "costo_envio", "total", "fecha_pedido",
                  "entregado_en", "detalles", "incidencias"]
        read_only_fields = fields