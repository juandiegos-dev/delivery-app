from decimal import Decimal

from rest_framework.test import APITestCase

from config.pruebas import crear_api, crear_restaurante_con_menu
from notificaciones.models import Notificacion
from notificaciones.services import registrar
from pedidos.models import Pedido
from pedidos.tarifas import calcular_tarifa_envio


class TarifaYNotificacionesTests(APITestCase):
    def setUp(self):
        self.dueno, self.rid, _ = crear_restaurante_con_menu()
        self.cliente = crear_api("cliente")
        self.otro_cliente = crear_api("cliente", username="otro_cliente")
        self.restaurante = self.dueno.usuario.restaurante

    def test_tarifa_aumenta_al_subir_demanda(self):
        self.assertEqual(calcular_tarifa_envio(self.restaurante), Decimal("5.00"))
        for _ in range(5):
            Pedido.objects.create(
                cliente=self.cliente.usuario,
                restaurante=self.restaurante,
                direccion_entrega="Calle A",
            )
        self.assertEqual(calcular_tarifa_envio(self.restaurante), Decimal("7.50"))
        for _ in range(5):
            Pedido.objects.create(
                cliente=self.cliente.usuario,
                restaurante=self.restaurante,
                direccion_entrega="Calle B",
            )
        self.assertEqual(calcular_tarifa_envio(self.restaurante), Decimal("10.00"))

    def test_bandeja_privada_de_notificaciones(self):
        pedido = Pedido.objects.create(
            cliente=self.cliente.usuario,
            restaurante=self.restaurante,
            direccion_entrega="Calle A",
        )
        registrar(self.cliente.usuario, pedido, "ESTADO", "Tu pedido fue aceptado")
        propio = self.cliente.get("/api/notificaciones/")
        ajeno = self.otro_cliente.get("/api/notificaciones/")
        self.assertEqual(propio.status_code, 200)
        self.assertEqual(len(propio.data), 1)
        self.assertEqual(len(ajeno.data), 0)

    def test_notificaciones_requieren_token(self):
        self.assertEqual(self.client.get("/api/notificaciones/").status_code, 401)