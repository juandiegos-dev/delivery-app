"""RF11: cancelación limitada a estados tempranos, con motivo y permisos."""

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

from pedidos.avisos import notificar_participantes
from pedidos.models import IncidenciaPedido, Pedido
from pedidos.services import Conflicto


@transaction.atomic
def cancelar(pedido_id, actor, motivo):
    pedido = get_object_or_404(
        Pedido.objects.select_for_update().select_related("restaurante"),
        pk=pedido_id
    )

    if actor.pk not in (
        pedido.cliente_id,
        pedido.restaurante.dueno_id
    ):
        raise PermissionDenied("No participa en este pedido")

    if pedido.estado not in (
        Pedido.Estado.PENDIENTE,
        Pedido.Estado.ACEPTADO
    ):
        raise Conflicto(
            "Solo se puede cancelar antes de iniciar la preparación"
        )

    pedido.estado = Pedido.Estado.CANCELADO
    pedido.save(update_fields=["estado"])

    IncidenciaPedido.objects.create(
        pedido=pedido,
        actor=actor,
        tipo=IncidenciaPedido.Tipo.CANCELACION,
        motivo=motivo
    )

    notificar_participantes(
        pedido,
        actor,
        f"Pedido #{pedido.pk} cancelado: {motivo}"
    )

    return pedido