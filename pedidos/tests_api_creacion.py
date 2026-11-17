from decimal import Decimal
from rest_framework.test import APITestCase
from catalogo.models import Producto
from config.pruebas import crear_api, crear_restaurante_con_menu
from pedidos.models import Pedido

class CrearPedidoAPITests(APITestCase):
    def setUp(self):
        self.dueno, self.restaurante_id, self.ids = crear_restaurante_con_menu()
        self.cliente = crear_api("cliente")
        self.url = "/api/pedidos/"
        self.datos = {
            "restaurante_id": self.restaurante_id,
            "direccion_entrega": "Jr. Huallayco 123, Huánuco",
            "observaciones": "Sin ají",
            "items": [
                {"producto_id": self.ids[0], "cantidad": 2},
                {"producto_id": self.ids[1], "cantidad": 1},
            ],
        }

    def test_creacion_real_y_detalles(self):
        r = self.cliente.post(self.url, self.datos, format="json")
        self.assertEqual(r.status_code, 201, r.data)
        pedido = Pedido.objects.get(pk=r.data["id"])
        self.assertEqual(pedido.detalles.count(), 2)
        self.assertEqual(pedido.subtotal, Decimal("55.00"))
        self.assertEqual(pedido.costo_envio, Decimal("5.00"))
        self.assertEqual(pedido.total, Decimal("60.00"))
        self.assertEqual(pedido.detalles.first().subtotal > 0, True)
        self.assertIn("fecha_pedido", r.data)

    def test_sin_direccion_se_rechaza(self):
        datos = {k: v for k, v in self.datos.items() if k != "direccion_entrega"}
        self.assertEqual(self.cliente.post(self.url, datos, format="json").status_code, 400)

    def test_lista_vacia_se_rechaza(self):
        self.assertEqual(self.cliente.post(
            self.url, {**self.datos, "items": []}, format="json"
        ).status_code, 400)

    def test_producto_no_disponible_se_rechaza(self):
        Producto.objects.filter(pk=self.ids[0]).update(disponible=False)
        self.assertEqual(self.cliente.post(self.url, self.datos, format="json").status_code, 400)

    def test_restaurante_no_puede_comprar(self):
        self.assertEqual(self.dueno.post(self.url, self.datos, format="json").status_code, 403)

    def test_cantidad_maxima(self):
        datos = {**self.datos, "items": [{"producto_id": self.ids[0], "cantidad": 50}]}
        self.assertEqual(self.cliente.post(self.url, datos, format="json").status_code, 201)
        datos["items"][0]["cantidad"] = 51
        self.assertEqual(self.cliente.post(self.url, datos, format="json").status_code, 400)