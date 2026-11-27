from decimal import Decimal
from math import asin, cos, radians, sin, sqrt

from django.db import transaction

from pedidos.models import Pedido
from repartidores.models import Asignacion, PerfilRepartidor, PuntoRestaurante


def distancia_km(lat_a, lon_a, lat_b, lon_b):
    """Distancia Haversine aproximada entre dos coordenadas GPS (km)."""
    a_lat, a_lon, b_lat, b_lon = map(radians, (lat_a, lon_a, lat_b, lon_b))
    da = b_lat - a_lat
    do = b_lon - a_lon
    h = sin(da / 2) ** 2 + cos(a_lat) * cos(b_lat) * sin(do / 2) ** 2
    return 2 * 6371.0 * asin(min(1.0, sqrt(h)))

@transaction.atomic
def asignar_mas_cercano(pedido):
    """Se invoca automáticamente cuando un pedido pasa a LISTO.

    Si no hay GPS o repartidor disponible, deja el pedido LISTO sin asignación;
    podrá reintentarse al actualizar ubicaciones o disponibilidad.
    """
    pedido = Pedido.objects.select_for_update().get(pk=pedido.pk)
    if pedido.estado != Pedido.Estado.LISTO:
        return None
    existente = Asignacion.objects.filter(pedido=pedido).first()
    if existente:
        return existente
    punto = PuntoRestaurante.objects.filter(restaurante=pedido.restaurante).first()
    if punto is None:
        return None
    perfiles = PerfilRepartidor.objects.filter(
        usuario__rol="repartidor", usuario__is_active=True,
        disponible=True, latitud__isnull=False, longitud__isnull=False,
    ).select_related("usuario")
    candidatos = sorted(
        ((distancia_km(punto.latitud, punto.longitud, p.latitud, p.longitud), p) for p in perfiles),
        key=lambda par: (par[0], par[1].pk),
    )
    if not candidatos:
        return None
    distancia, perfil = candidatos[0]
    asignacion = Asignacion.objects.create(
        pedido=pedido,
        repartidor=perfil.usuario,
        distancia_km=Decimal(str(distancia)).quantize(Decimal("0.01")),
    )
    perfil.disponible = False
    perfil.save(update_fields=["disponible", "actualizado_en"])
    return asignacion