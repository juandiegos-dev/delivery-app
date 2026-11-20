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
    
    def test_distancia_cero(self):
        self.assertAlmostEqual(distancia_km(-9.93, -76.24, -9.93, -76.24), 0, places=5)

    def test_asigna_al_mas_cercano_y_bloquea_disponibilidad(self):
        asignacion = asignar_mas_cercano(self.pedido)
        self.assertEqual(asignacion.repartidor, self.cercano)
        self.assertTrue(Asignacion.objects.filter(pedido=self.pedido).exists())
        self.assertFalse(PerfilRepartidor.objects.get(usuario=self.cercano).disponible)
        self.assertEqual(asignar_mas_cercano(self.pedido).pk, asignacion.pk)

    def test_pedido_no_listo_no_se_asigna(self):
        self.pedido.estado = "PENDIENTE"
        self.pedido.save(update_fields=["estado"])
        self.assertIsNone(asignar_mas_cercano(self.pedido))