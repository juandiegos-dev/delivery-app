from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied

from notificaciones.models import Notificacion
from notificaciones.services import registrar
from pedidos.models import Pedido
from pedidos.services import Conflicto
from repartidores.models import Asignacion, HistorialUbicacion, PerfilRepartidor


def _asignacion_repartidor(pedido, repartidor):
    asignacion = get_object_or_404(Asignacion, pedido=pedido)
    if asignacion.repartidor_id != repartidor.pk:
        raise PermissionDenied("Solo el repartidor asignado puede realizar la operación")
    return asignacion


@transaction.atomic
def iniciar_reparto(pedido_id, repartidor):
    pedido = get_object_or_404(Pedido.objects.select_for_update(), pk=pedido_id)
    asignacion = _asignacion_repartidor(pedido, repartidor)
    if pedido.estado != Pedido.Estado.LISTO:
        raise Conflicto("Solo se inicia reparto cuando el pedido está LISTO")
    pedido.estado = Pedido.Estado.EN_CAMINO
    pedido.save(update_fields=["estado"])
    perfil = PerfilRepartidor.objects.filter(usuario=repartidor).first()
    if perfil and perfil.latitud is not None and perfil.longitud is not None:
        HistorialUbicacion.objects.create(
            asignacion=asignacion, latitud=perfil.latitud, longitud=perfil.longitud
        )
    registrar(destinatario=pedido.cliente, pedido=pedido, tipo=Notificacion.Tipo.ESTADO,
             mensaje=f"El pedido #{pedido.pk} está EN_CAMINO")
    return pedido


@transaction.atomic
def confirmar_entrega(pedido_id, repartidor):
    pedido = get_object_or_404(Pedido.objects.select_for_update(), pk=pedido_id)
    _asignacion_repartidor(pedido, repartidor)
    if pedido.estado != Pedido.Estado.EN_CAMINO:
        raise Conflicto("Para confirmar entrega, el pedido debe estar EN_CAMINO")
    pedido.estado = Pedido.Estado.ENTREGADO
    pedido.entregado_en = timezone.now()
    pedido.save(update_fields=["estado", "entregado_en"])
    PerfilRepartidor.objects.filter(usuario=repartidor).update(disponible=True)
    for user in (pedido.cliente, pedido.restaurante.dueno):
        registrar(destinatario=user, pedido=pedido, tipo=Notificacion.Tipo.ESTADO,
                 mensaje=f"Pedido #{pedido.pk} ENTREGADO y confirmado")
    return pedido