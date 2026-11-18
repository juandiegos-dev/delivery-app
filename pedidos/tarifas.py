from decimal import Decimal

from django.conf import settings
from pedidos.models import Pedido


def calcular_tarifa_envio(restaurante):
    """RF09. Tarifa base según la cantidad de pedidos activos del restaurante.

    0-4 activos: S/ 5.00; 5-9: S/ 7.50; 10 o más: S/ 10.00.
    Se calcula al crear el pedido y se guarda como precio histórico.
    """
    activos = Pedido.objects.filter(
        restaurante=restaurante,
        estado__in=["PENDIENTE", "ACEPTADO", "EN_PREPARACION", "LISTO"],
    ).count()
    base = settings.COSTO_ENVIO_BASE
    if activos >= 10:
        factor = Decimal("2.00")
    elif activos >= 5:
        factor = Decimal("1.50")
    else:
        factor = Decimal("1.00")
    return (base * factor).quantize(Decimal("0.01"))