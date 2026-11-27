from django.test import TestCase
from rest_framework.test import APIClient
from accesos.models import Usuario
from catalogo.models import Restaurante
from pedidos.models import Pedido
from repartidores.models import PerfilRepartidor, PuntoRestaurante, HistorialUbicacion
from repartidores.services import asignar_mas_cercano


class MapaSeguimientoTests(TestCase):
    def setUp(self):
        self.cliente = Usuario.objects.create_user(username="cliente_v", email="cv@example.test", password="Prueba123!", rol="cliente")
        self.ajeno = Usuario.objects.create_user(username="ajeno_v", email="av@example.test", password="Prueba123!", rol="cliente")
        self.dueno = Usuario.objects.create_user(username="dueno_v", email="dv@example.test", password="Prueba123!", rol="restaurante")
        self.rep = Usuario.objects.create_user(username="rep_v", email="rv@example.test", password="Prueba123!", rol="repartidor")
        self.restaurante = Restaurante.objects.create(dueno=self.dueno, nombre="Restaurante Prueba V", direccion="Calle")
        PuntoRestaurante.objects.create(restaurante=self.restaurante, latitud=-9.930, longitud=-76.240)
        PerfilRepartidor.objects.create(usuario=self.rep, latitud=-9.931, longitud=-76.241, disponible=True)
        self.pedido = Pedido.objects.create(cliente=self.cliente, restaurante=self.restaurante,
            direccion_entrega="Calle 2", estado="LISTO")
        asignar_mas_cercano(self.pedido)

    def api(self, u):
        c = APIClient()
        c.force_authenticate(user=u)
        return c

    def test_solo_participantes_ven_ruta(self):
        url = f"/api/repartidores/pedidos/{self.pedido.pk}/ruta/"
        self.assertEqual(self.api(self.cliente).get(url).status_code, 200)
        self.assertEqual(self.api(self.ajeno).get(url).status_code, 404)

    def test_historial_gps_repartidor_asignado(self):
        r = self.api(self.rep).put("/api/repartidores/mi-ubicacion/",
            {"latitud": -9.932, "longitud": -76.242}, format="json")
        self.assertEqual(r.status_code, 200, r.data)
        self.assertEqual(HistorialUbicacion.objects.count(), 1)

    def test_gps_invalido_400(self):
        r = self.api(self.rep).put("/api/repartidores/mi-ubicacion/",
            {"latitud": 95, "longitud": 190}, format="json")
        self.assertEqual(r.status_code, 400)

    def test_pagina_no_expone_datos_sin_token(self):
        respuesta = self.client.get(f"/seguimiento/{self.pedido.pk}/")
        self.assertEqual(respuesta.status_code, 200)
        self.assertNotContains(respuesta, "direccion_entrega", status_code=200)