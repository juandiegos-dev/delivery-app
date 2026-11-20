from rest_framework import APITestCase
from config.pruebas import crear_api, crear_restaurante_con_menu
from repartidores.models import PerfilRepartidor, PuntoRestaurante

class UbicacionesAPITests(APITestCase):
    def setUp(self):
        self.dueno, self.rid, _ = crear_restaurante_con_menu()
        self.cliente = crear_api("cliente")
        self.repartidor = crear_api("repartidor")

    def test_repartidor_publica_su_posicion(self):
        r = self.repartidor.put(
            "/api/repartidores/mi-ubicacion/",
            {"latitud": -9.929, "longitud": -76.24, "disponible": True},
            format="json",
        )
        self.assertEqual(r.status_code, 200, r.data)
        self.assertTrue(PerfilRepartidor.objects.filter(usuario=self.repartidor.usuario).exists())
        self.assertEqual(self.repartidor.get("/api/repartidores/mi-ubicacion/").status_code, 200)
    def test_dueno_registra_gps_del_restaurante(self):
        r = self.dueno.put(
            f"/api/repartidores/restaurantes/{self.rid}/ubicacion/",
            {"latitud": -9.93, "longitud": -76.24}, format="json",
        )
        self.assertEqual(r.status_code, 200, r.data)
        self.assertTrue(PuntoRestaurante.objects.filter(restaurante_id=self.rid).exists())
    def test_cliente_no_puede_modificar_gps_del_restaurante(self):
        r = self.cliente.put(
            f"/api/repartidores/restaurantes/{self.rid}/ubicacion/",
            {"latitud": -9.93, "longitud": -76.24}, format="json",
        )
        self.assertEqual(r.status_code, 403)