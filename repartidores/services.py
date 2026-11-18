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