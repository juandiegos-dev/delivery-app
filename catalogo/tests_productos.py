from decimal import Decimal

from rest_framework.test import APITestCase

from catalogo.models import Producto
from config.pruebas import crear_api, crear_restaurante_con_menu
from pedidos.models import DetallePedido, Pedido


class ProductosTests(APITestCase):
    def test_crear_producto(self):
        api, rid, _ = crear_restaurante_con_menu()
        r = api.post(f"/api/restaurantes/{rid}/productos/", {"nombre": "Chicha", "precio": "6.00"}, format="json")
        self.assertEqual(r.status_code, 201)

    def test_actualizar_y_consultar_producto(self):
        api, _, ids = crear_restaurante_con_menu()
        api.put(f"/api/productos/{ids[0]}/", {"nombre": "Pollo entero", "precio": "60.00"}, format="json")
        self.assertEqual(self.client.get(f"/api/productos/{ids[0]}/").data["nombre"], "Pollo entero")

    def test_marcar_producto_no_disponible(self):
        api, _, ids = crear_restaurante_con_menu()
        api.put(f"/api/productos/{ids[1]}/",
                {"nombre": "Gaseosa", "precio": "4.00", "disponible": False}, format="json")
        self.assertFalse(Producto.objects.get(pk=ids[1]).disponible)

    def test_eliminar_producto(self):
        api, _, ids = crear_restaurante_con_menu()
        self.assertEqual(api.delete(f"/api/productos/{ids[0]}/").status_code, 204)
        self.assertEqual(self.client.get(f"/api/productos/{ids[0]}/").status_code, 404)

    def test_no_se_elimina_un_producto_con_pedidos(self):
        api, rid, ids = crear_restaurante_con_menu()
        cliente = crear_api("cliente")
        pedido = Pedido.objects.create(
            cliente=cliente.usuario, restaurante_id=rid,
            subtotal=Decimal("25.50"), costo_envio=Decimal("5.00"), total=Decimal("30.50"),
        )
        DetallePedido.objects.create(
            pedido=pedido, producto_id=ids[0], cantidad=1, precio_unitario=Decimal("25.50")
        )
        self.assertEqual(api.delete(f"/api/productos/{ids[0]}/").status_code, 400)

    def test_producto_con_precio_negativo(self):
        api, rid, _ = crear_restaurante_con_menu()
        r = api.post(f"/api/restaurantes/{rid}/productos/", {"nombre": "Error", "precio": "-3"}, format="json")
        self.assertEqual(r.status_code, 400)

    def test_precio_en_el_limite_minimo(self):
        api, rid, _ = crear_restaurante_con_menu()
        url = f"/api/restaurantes/{rid}/productos/"
        ok = api.post(url, {"nombre": "Caramelo", "precio": "0.01"}, format="json")
        cero = api.post(url, {"nombre": "Gratis", "precio": "0"}, format="json")
        self.assertEqual((ok.status_code, cero.status_code), (201, 400))

    def test_cliente_no_puede_crear_productos(self):
        _, rid, _ = crear_restaurante_con_menu()
        cliente = crear_api("cliente")
        r = cliente.post(f"/api/restaurantes/{rid}/productos/", {"nombre": "X", "precio": "1"}, format="json")
        self.assertEqual(r.status_code, 403)

    def test_otro_restaurante_no_puede_editar_el_menu(self):
        _, _, ids = crear_restaurante_con_menu()
        otro = crear_api("restaurante", username="otro")
        r = otro.put(f"/api/productos/{ids[0]}/", {"nombre": "Hack", "precio": "1"}, format="json")
        self.assertEqual(r.status_code, 403)