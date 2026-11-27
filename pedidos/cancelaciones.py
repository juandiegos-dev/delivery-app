"""RF11: cancelación limitada a estados tempranos, con motivo y permisos."""

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

from notificaciones.services import registrar
from pedidos.models import IncidenciaPedido, Pedido
from pedidos.services import Conflicto


@transaction.atomic
def cancelar(pedido_id, actor, motivo):
    pedido = get_object_or_404(
        Pedido.objects.select_for_update().select_related("restaurante"),
        pk=pedido_id
    )

    # Verificar que el usuario sea cliente o dueño del restaurante.
    if actor.pk not in (
        pedido.cliente_id,
        pedido.restaurante.dueno_id
    ):
        raise PermissionDenied("No participa en este pedido")

    # Solo permitir cancelar pedidos pendientes o aceptados.
    if pedido.estado not in (
        Pedido.Estado.PENDIENTE,
        Pedido.Estado.ACEPTADO
    ):
        raise Conflicto(
            "Solo se puede cancelar antes de iniciar la preparación"
        )

    # Actualizar el estado del pedido.
    pedido.estado = Pedido.Estado.CANCELADO
    pedido.save(update_fields=["estado"])

    # Registrar la incidencia de cancelación.
    IncidenciaPedido.objects.create(
        pedido=pedido,
        actor=actor,
        tipo=IncidenciaPedido.Tipo.CANCELACION,
        motivo=motivo
    )

    # Notificar a la otra parte del pedido.
    destinatario = (
        pedido.restaurante.dueno
        if actor.pk == pedido.cliente_id
        else pedido.cliente
    )

    registrar(
        destinatario,
        pedido,
        "CANCELACION",
        f"Pedido #{pedido.pk} cancelado: {motivo}"
    )

    return pedido
