from decimal import Decimal
from django.conf import settings
from pedidos.models import Pedido


def calcular_tarifa_envio(restaurante):
    """Costo por pedidos activos PREVIOS del mismo restaurante. Precio congelado al comprar."""
    activos = Pedido.objects.filter(
        restaurante=restaurante,
        estado__in=["PENDIENTE", "ACEPTADO", "EN_PREPARACION", "LISTO", "EN_CAMINO"],
    ).count()
    base = settings.COSTO_ENVIO_BASE
    factor = Decimal("2.00") if activos >= 10 else Decimal("1.50") if activos >= 5 else Decimal("1.00")
    return (base * factor).quantize(Decimal("0.01"))