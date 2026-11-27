from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from accesos.models import Usuario
from catalogo.models import Restaurante
from pedidos.models import Pedido, IncidenciaPedido
from pedidos.tarifas import calcular_tarifa_envio
from notificaciones.models import Notificacion


class FallosTarifasTests(TestCase):
    def setUp(self):
        self.cliente = Usuario.objects.create_user(username="cliente_f", email="cf@example.test", password="Prueba123!", rol="cliente")
        self.dueno = Usuario.objects.create_user(username="dueno_f", email="df@example.test", password="Prueba123!", rol="restaurante")
        self.ajeno = Usuario.objects.create_user(username="ajeno_f", email="af@example.test", password="Prueba123!", rol="cliente")
        self.restaurante = Restaurante.objects.create(dueno=self.dueno, nombre="Restaurante Prueba F", direccion="Calle")
        self.pedido = Pedido.objects.create(cliente=self.cliente, restaurante=self.restaurante,
             direccion_entrega="Calle 2", estado="EN_PREPARACION")
        self.url = f"/api/pedidos/{self.pedido.pk}/fallido/"

    def api(self, usuario):
        c = APIClient()
        c.force_authenticate(user=usuario)
        return c

    def test_restaurante_registra_fallo_y_avisos(self):
        r = self.api(self.dueno).post(self.url,
              {"motivo": "No hay insumos suficientes para completar el pedido"}, format="json")
        self.assertEqual(r.status_code, 200, r.data)
        self.assertEqual(r.data["estado"], "FALLIDO")
        self.assertEqual(IncidenciaPedido.objects.filter(pedido=self.pedido, tipo="FALLO").count(), 1)
        self.assertTrue(Notificacion.objects.filter(destinatario=self.cliente, pedido=self.pedido).exists())

    def test_cliente_no_puede_reportar_fallo(self):
        r = self.api(self.cliente).post(self.url,
              {"motivo": "El cliente reporta fallo sin autorizacion"}, format="json")
        self.assertEqual(r.status_code, 404)

    def test_motivo_corto_rechazado(self):
        self.assertEqual(self.api(self.dueno).post(self.url, {"motivo": "no"}, format="json").status_code, 400)

    def test_estado_terminal_no_cuenta_para_tarifa(self):
        self.pedido.estado = "ENTREGADO"
        self.pedido.save(update_fields=["estado"])
        self.assertEqual(calcular_tarifa_envio(self.restaurante), Decimal("5.00"))

    def test_tarifa_cinco_activos_y_previo_cero(self):
        # 1 existente EN_PREPARACION + 4 nuevos PENDIENTE = 5 activos previos
        self.assertEqual(calcular_tarifa_envio(self.restaurante), Decimal("5.00"))
        for i in range(4):
            Pedido.objects.create(cliente=self.cliente, restaurante=self.restaurante, direccion_entrega=f"Calle {i}")
        self.assertEqual(calcular_tarifa_envio(self.restaurante), Decimal("7.50"))