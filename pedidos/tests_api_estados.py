from rest_framework.test import APITestCase

from catalogo.models import Restaurante
from config.pruebas import crear_api, crear_restaurante_con_menu
from pedidos.models import Pedido


class EstadoPedidoAPITests(APITestCase):

    def setUp(self):
        self.dueno, rid, self.ids = crear_restaurante_con_menu()
        self.cliente = crear_api("cliente")
        self.pedido = Pedido.objects.create(
            cliente=self.cliente.usuario,
            restaurante_id=rid,
            direccion_entrega="Jr. Dos de Mayo 123",
        )
        self.url = f"/api/pedidos/{self.pedido.pk}/estado/"

    def test_flujo_aceptado_preparacion_listo(self):
        for estado in ("ACEPTADO", "EN_PREPARACION", "LISTO"):
            respuesta = self.dueno.patch(
                self.url, {"estado": estado}, format="json"
            )
            self.assertEqual(respuesta.status_code, 200, respuesta.data)
            self.assertEqual(respuesta.data["estado"], estado)

    def test_rechazo_pendiente(self):
        respuesta = self.dueno.patch(
            self.url, {"estado": "RECHAZADO"}, format="json"
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.data["estado"], "RECHAZADO")