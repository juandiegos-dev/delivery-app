from decimal import Decimal

from rest_framework.test import APITestCase

from config.pruebas import crear_api, crear_restaurante_con_menu
from notificaciones.models import Notificacion
from pedidos.models import Pedido
from repartidores.models import Asignacion, PerfilRepartidor, PuntoRestaurante


class FlujoIntegralHito3Tests(APITestCase):
    def setUp(self):
        self.dueno, self.rid, self.ids = crear_restaurante_con_menu()
        self.cliente = crear_api("cliente")
        self.repartidor = crear_api("repartidor")
        PuntoRestaurante.objects.create(
            restaurante_id=self.rid, latitud=-9.930, longitud=-76.240
        )
        PerfilRepartidor.objects.create(
            usuario=self.repartidor.usuario, latitud=-9.931, longitud=-76.241, disponible=True
        )
        self.datos = {
            "restaurante_id": self.rid,
            "direccion_entrega": "Jr. Dos de Mayo 123, Huánuco",
            "items": [{"producto_id": self.ids[0], "cantidad": 2}],
        }

    def test_crear_cambiar_estado_asignar_y_notificar(self):
        creado = self.cliente.post("/api/pedidos/", self.datos, format="json")
        self.assertEqual(creado.status_code, 201, creado.data)
        pid = creado.data["id"]
        self.assertEqual(Pedido.objects.get(pk=pid).total, Decimal("56.00"))
        self.assertEqual(Notificacion.objects.filter(destinatario=self.dueno.usuario).count(), 1)
        for estado in ("ACEPTADO", "EN_PREPARACION", "LISTO"):
            r = self.dueno.patch(
                f"/api/pedidos/{pid}/estado/", {"estado": estado}, format="json"
            )
            self.assertEqual(r.status_code, 200, r.data)
        asignacion = Asignacion.objects.get(pedido_id=pid)
        self.assertEqual(asignacion.repartidor, self.repartidor.usuario)
        self.assertGreaterEqual(
            Notificacion.objects.filter(destinatario=self.cliente.usuario).count(), 4
        )
        self.assertEqual(
            self.cliente.get(f"/api/repartidores/pedidos/{pid}/asignacion/").status_code, 200
        )
        self.assertEqual(self.repartidor.get("/api/notificaciones/").status_code, 200)

    def test_tarifa_persiste_segun_demanda(self):
        for _ in range(5):
            Pedido.objects.create(
                cliente=self.cliente.usuario,
                restaurante_id=self.rid,
                direccion_entrega="Calle A",
            )
        respuesta = self.cliente.post("/api/pedidos/", self.datos, format="json")
        self.assertEqual(respuesta.status_code, 201, respuesta.data)
        self.assertEqual(Decimal(respuesta.data["costo_envio"]), Decimal("7.50"))
        self.assertEqual(Decimal(respuesta.data["total"]), Decimal("58.50"))

    def test_ubicacion_visible_solo_a_participantes(self):
        creado = self.cliente.post("/api/pedidos/", self.datos, format="json")
        pid = creado.data["id"]
        for estado in ("ACEPTADO", "EN_PREPARACION", "LISTO"):
            self.dueno.patch(f"/api/pedidos/{pid}/estado/", {"estado": estado}, format="json")
        self.assertEqual(
            self.cliente.get(f"/api/repartidores/pedidos/{pid}/ubicacion/").status_code, 200
        )
        ajeno = crear_api("cliente", username="ajeno_mapa")
        self.assertEqual(
            ajeno.get(f"/api/repartidores/pedidos/{pid}/ubicacion/").status_code, 404
        )