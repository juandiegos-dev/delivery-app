
from django.conf import settings
from rest_framework import serializers

from pedidos.models import DetallePedido, Pedido


class ItemPedidoSerializer(serializers.Serializer):
    producto_id = serializers.IntegerField()
    cantidad = serializers.IntegerField(
        min_value=1,
        max_value=settings.CANTIDAD_MAXIMA_POR_PRODUCTO
    )


class PedidoCrearSerializer(serializers.Serializer):
    restaurante_id = serializers.IntegerField()
    items = ItemPedidoSerializer(many=True, allow_empty=False)


class CambioEstadoSerializer(serializers.Serializer):
    estado = serializers.ChoiceField(choices=Pedido.Estado.choices)


class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = ["producto", "cantidad", "precio_unitario"]


class PedidoSerializer(serializers.ModelSerializer):
    detalles = DetallePedidoSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = [
            "id", "cliente", "restaurante", "estado", "subtotal",
            "costo_envio", "total", "fecha", "detalles"
        ]
