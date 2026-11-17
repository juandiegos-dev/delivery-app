from rest_framework.test import APITestCase

from catalogo.models import Producto
from config.pruebas import crear_api, crear_restaurante_con_menu


class CatalogoTests(APITestCase):
    def test_restaurante_aparece_en_el_listado(self):
        crear_restaurante_con_menu()
        nombres = [r["nombre"] for r in self.client.get("/api/restaurantes/").data]
        self.assertEqual(nombres, ["Pollería Huánuco"])

    def test_menu_solo_muestra_productos_disponibles(self):
        _, rid, ids = crear_restaurante_con_menu()
        Producto.objects.filter(pk=ids[1]).update(disponible=False)
        menu = self.client.get(f"/api/restaurantes/{rid}/menu/").data
        self.assertEqual([p["nombre"] for p in menu], ["Pollo a la brasa"])

    def test_menu_de_restaurante_inexistente(self):
        self.assertEqual(self.client.get("/api/restaurantes/999/menu/").status_code, 404)

    def test_cliente_no_puede_registrar_restaurante(self):
        cliente = crear_api("cliente")
        r = cliente.post("/api/restaurantes/", {"nombre": "Falso", "direccion": "Calle 123"}, format="json")
        self.assertEqual(r.status_code, 403)

    def test_restaurante_duplicado_es_rechazado(self):
        api = crear_api("restaurante")
        datos = {"nombre": "Cevichería Sol", "direccion": "Av. Universitaria 500"}
        self.assertEqual(api.post("/api/restaurantes/", datos, format="json").status_code, 201)
        self.assertEqual(api.post("/api/restaurantes/", datos, format="json").status_code, 400)

    def test_restaurante_con_nombre_vacio(self):
        api = crear_api("restaurante")
        r = api.post("/api/restaurantes/", {"nombre": "", "direccion": "Av. Universitaria 500"}, format="json")
        self.assertEqual(r.status_code, 400)