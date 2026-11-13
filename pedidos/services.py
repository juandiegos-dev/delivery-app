
from decimal import Decimal

from django.conf import settings
from django.db import transaction
from rest_framework.exceptions import APIException, NotFound, ValidationError

from catalogo.models import Producto, Restaurante
from pedidos.models import DetallePedido, Pedido

TRANSICIONES = {
    Pedido.Estado.PENDIENTE: {Pedido.Estado.ACEPTADO, Pedido.Estado.RECHAZADO},
    Pedido.Estado.ACEPTADO: {Pedido.Estado.EN_PREPARACION},
    Pedido.Estado.EN_PREPARACION: {Pedido.Estado.LISTO},
    Pedido.Estado.RECHAZADO: set(),
    Pedido.Estado.LISTO: set(),
}


class Conflicto(APIException):
    status_code = 409
    default_detail = "La operación entra en conflicto con el estado actual"


def _construir_detalles(restaurante, items):
    detalles = []
    for item in items:
        producto = Producto.objects.filter(pk=item["producto_id"], restaurante=restaurante).first()
        if producto is None:
            raise ValidationError(f"El producto {item['producto_id']} no pertenece a este restaurante")
        if not producto.disponible:
            raise ValidationError(f"El producto '{producto.nombre}' no está disponible")
        detalles.append(DetallePedido(
            producto=producto, cantidad=item["cantidad"], precio_unitario=producto.precio
        ))
    return detalles


@transaction.atomic
def crear_pedido(cliente, datos):
    try:
        restaurante = Restaurante.objects.get(pk=datos["restaurante_id"])
    except Restaurante.DoesNotExist:
        raise NotFound("Restaurante no encontrado")
    detalles = _construir_detalles(restaurante, datos["items"])
    subtotal = sum((d.precio_unitario * d.cantidad for d in detalles), Decimal("0"))
    envio = settings.COSTO_ENVIO_BASE
    pedido = Pedido.objects.create(
        cliente=cliente, restaurante=restaurante,
        subtotal=subtotal, costo_envio=envio, total=subtotal + envio,
    )
    for detalle in detalles:
        detalle.pedido = pedido
    DetallePedido.objects.bulk_create(detalles)
    return pedido


def cambiar_estado(pedido, nuevo_estado):
    if nuevo_estado not in TRANSICIONES[pedido.estado]:
        raise Conflicto(f"No se puede pasar de {pedido.estado} a {nuevo_estado}")
    pedido.estado = nuevo_estado
    pedido.save(update_fields=["estado"])
    return pedido
