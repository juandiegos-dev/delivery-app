"""Utilidades compartidas para notificaciones y liberación de repartidores."""
from django.contrib.auth import get_user_model
from notificaciones.models import Notificacion
from notificaciones.services import registrar
from repartidores.models import Asignacion, PerfilRepartidor


def notificar_participantes(pedido, actor, mensaje):
    participantes = {pedido.cliente_id, pedido.restaurante.dueno_id}
    asignacion = Asignacion.objects.filter(pedido=pedido).first()
    if asignacion:
        participantes.add(asignacion.repartidor_id)
    participantes.discard(actor.pk)
    for usuario in get_user_model().objects.filter(pk__in=participantes):
        registrar(destinatario=usuario, pedido=pedido,
                 tipo=Notificacion.Tipo.ESTADO, mensaje=mensaje[:240])


def liberar_repartidor(pedido):
    asignacion = Asignacion.objects.filter(pedido=pedido).first()
    if asignacion:
        PerfilRepartidor.objects.filter(usuario_id=asignacion.repartidor_id).update(disponible=True)