from decimal import Decimal

from django.db import transaction
from rest_framework.exceptions import APIException, NotFound, ValidationError

from catalogo.models import Producto, Restaurante
from notificaciones.models import Notificacion
from notificaciones.services import registrar
from pedidos.models import DetallePedido, Pedido
from pedidos.tarifas import calcular_tarifa_envio
from repartidores.services import asignar_mas_cercano


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
        producto = Producto.objects.filter(
            pk=item["producto_id"], restaurante=restaurante
        ).first()
        if producto is None:
            raise ValidationError("El producto no pertenece a este restaurante")
        if not producto.disponible:
            raise ValidationError(f"El producto '{producto.nombre}' no está disponible")
        precio = producto.precio
        cantidad = item["cantidad"]
        detalles.append(DetallePedido(
            producto=producto,
            nombre_producto=producto.nombre,
            cantidad=cantidad,
            precio_unitario=precio,
            subtotal=precio * cantidad,
        ))
    return detalles


@transaction.atomic
def crear_pedido(cliente, datos):
    try:
        restaurante = Restaurante.objects.get(pk=datos["restaurante_id"])
    except Restaurante.DoesNotExist:
        raise NotFound("Restaurante no encontrado")

    detalles = _construir_detalles(restaurante, datos["items"])
    subtotal = sum((d.subtotal for d in detalles), Decimal("0.00"))
    envio = calcular_tarifa_envio(restaurante)
    pedido = Pedido.objects.create(
        cliente=cliente,
        restaurante=restaurante,
        direccion_entrega=datos["direccion_entrega"],
        observaciones=datos.get("observaciones", ""),
        subtotal=subtotal,
        costo_envio=envio,
        total=subtotal + envio,
    )
    for detalle in detalles:
        detalle.pedido = pedido
    DetallePedido.objects.bulk_create(detalles)
    registrar(
        destinatario=restaurante.dueno,
        pedido=pedido,
        tipo=Notificacion.Tipo.NUEVO_PEDIDO,
        mensaje=f"Nuevo pedido #{pedido.pk} pendiente de revisión",
    )
    return pedido


@transaction.atomic
def cambiar_estado(pedido, nuevo_estado):
    actual = Pedido.objects.select_for_update().get(pk=pedido.pk)
    if nuevo_estado not in TRANSICIONES.get(actual.estado, set()):
        raise Conflicto(f"No se puede pasar de {actual.estado} a {nuevo_estado}")

    actual.estado = nuevo_estado
    actual.save(update_fields=["estado"])
    registrar(
        destinatario=actual.cliente,
        pedido=actual,
        tipo=Notificacion.Tipo.ESTADO,
        mensaje=f"El pedido #{actual.pk} cambió a {nuevo_estado}",
    )

    if nuevo_estado == Pedido.Estado.LISTO:
        asignacion = asignar_mas_cercano(actual)
        if asignacion is not None:
            registrar(
                destinatario=asignacion.repartidor,
                pedido=actual,
                tipo=Notificacion.Tipo.ASIGNACION,
                mensaje=f"Se te asignó el pedido #{actual.pk}",
            )
            registrar(
                destinatario=actual.cliente,
                pedido=actual,
                tipo=Notificacion.Tipo.ASIGNACION,
                mensaje=f"Repartidor asignado al pedido #{actual.pk}",
            )
    return actual