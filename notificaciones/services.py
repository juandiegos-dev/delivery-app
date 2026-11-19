from notificaciones.models import Notificacion


def registrar(destinatario, pedido, tipo, mensaje):
    """Guarda una notificación consultable desde la API (bandeja interna)."""
    return Notificacion.objects.create(
        destinatario=destinatario,
        pedido=pedido,
        tipo=tipo,
        mensaje=mensaje,
    )