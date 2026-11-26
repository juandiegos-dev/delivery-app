"""RF12: registrar fallos trazables, mantener integridad y liberar repartidor."""
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from pedidos.avisos import notificar_participantes, liberar_repartidor
from pedidos.models import IncidenciaPedido, Pedido
from pedidos.services import Conflicto
from repartidores.models import Asignacion


@transaction.atomic
def registrar_fallo(pedido_id, actor, motivo):
    pedido = get_object_or_404(
        Pedido.objects.select_for_update().select_related("restaurante"), pk=pedido_id
    )
    asignacion = Asignacion.objects.filter(pedido=pedido).first()
    autorizado = actor.pk == pedido.restaurante.dueno_id or (
        asignacion is not None and actor.pk == asignacion.repartidor_id
    )
    if not autorizado:
        raise PermissionDenied("Solo el restaurante o repartidor asignado puede reportar el fallo")
    if pedido.estado not in (
        Pedido.Estado.EN_PREPARACION, Pedido.Estado.LISTO, Pedido.Estado.EN_CAMINO
    ):
        raise Conflicto("El estado actual no permite registrar un pedido fallido")
    pedido.estado = Pedido.Estado.FALLIDO
    pedido.save(update_fields=["estado"])
    IncidenciaPedido.objects.create(pedido=pedido, actor=actor,
                                   tipo=IncidenciaPedido.Tipo.FALLO, motivo=motivo)
    liberar_repartidor(pedido)
    notificar_participantes(pedido, actor, f"Pedido #{pedido.pk} fallido: {motivo}")
    return pedido