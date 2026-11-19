from decimal import Decimal

from django.test import TestCase

from accesos.models import Usuario
from catalogo.models import Restaurante
from pedidos.models import Pedido
from repartidores.models import Asignacion, PerfilRepartidor, PuntoRestaurante
from repartidores.services import asignar_mas_cercano, distancia_km


class AsignacionTests(TestCase):
    def setUp(self):
        self.dueno = Usuario.objects.create_user(
            username="dueno_asignacion", email="dueno_asig@example.com", password="clave123", rol="restaurante"
        )
        self.cliente = Usuario.objects.create_user(
            username="cliente_asignacion", email="cliente_asig@example.com", password="clave123", rol="cliente"
        )
        restaurante = Restaurante.objects.create(
            dueno=self.dueno, nombre="Prueba", direccion="Calle A"
        )
        PuntoRestaurante.objects.create(restaurante=restaurante, latitud=-9.9300, longitud=-76.2400)
        self.pedido = Pedido.objects.create(
            cliente=self.cliente, restaurante=restaurante, direccion_entrega="Calle B", estado="LISTO",
            subtotal=Decimal("10.00"), costo_envio=Decimal("5.00"), total=Decimal("15.00")
        )
        self.cercano = Usuario.objects.create_user(
            username="rep_cercano", email="rep_cercano@example.com", password="clave123", rol="repartidor"
        )
        self.lejano = Usuario.objects.create_user(
            username="rep_lejano", email="rep_lejano@example.com", password="clave123", rol="repartidor"
        )
        PerfilRepartidor.objects.create(usuario=self.cercano, latitud=-9.9305, longitud=-76.2402)
        PerfilRepartidor.objects.create(usuario=self.lejano, latitud=-9.9500, longitud=-76.2900)
