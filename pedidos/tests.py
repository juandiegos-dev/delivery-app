from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from catalogo.models import Restaurante, Producto
from pedidos.models import Pedido, DetallePedido


class PedidoTests(TestCase):

    def test_estados_disponibles(self):
        self.assertEqual(Pedido.Estado.PENDIENTE, "PENDIENTE")
        self.assertEqual(Pedido.Estado.ACEPTADO, "ACEPTADO")
        self.assertEqual(Pedido.Estado.RECHAZADO, "RECHAZADO")

    def test_estado_por_defecto(self):
        campo = Pedido._meta.get_field("estado")

        self.assertEqual(
            campo.get_default(),
            Pedido.Estado.PENDIENTE
        )

    def test_calculo_total_pedido(self):
        subtotal = Decimal("25.50")
        costo_envio = Decimal("5.00")

        total = subtotal + costo_envio

        self.assertEqual(total, Decimal("30.50"))

    def test_relaciones_modelo(self):
        campo_restaurante = Pedido._meta.get_field("restaurante")
        campo_producto = DetallePedido._meta.get_field("producto")

        self.assertEqual(
            campo_restaurante.related_model,
            Restaurante
        )

        self.assertEqual(
            campo_producto.related_model,
            Producto
        )