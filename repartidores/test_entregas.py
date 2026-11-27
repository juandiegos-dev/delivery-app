from django.test import TestCase
from rest_framework.test import APIClient
from accesos.models import Usuario
from catalogo.models import Restaurante
from pedidos.models import Pedido
from repartidores.models import Asignacion, PerfilRepartidor, PuntoRestaurante
from repartidores.services import asignar_mas_cercano


class EntregasTests(TestCase):
    def setUp(self):
        self.cliente = Usuario.objects.create_user(username="cliente_m", email="cm@example.test", password="Prueba123!", rol="cliente")
        self.dueno = Usuario.objects.create_user(username="dueno_m", email="dm@example.test", password="Prueba123!", rol="restaurante")
        self.cercano = Usuario.objects.create_user(username="cercano_m", email="cr@example.test", password="Prueba123!", rol="repartidor")
        self.lejano = Usuario.objects.create_user(username="lejano_m", email="lr@example.test", password="Prueba123!", rol="repartidor")
        self.restaurante = Restaurante.objects.create(dueno=self.dueno, nombre="Restaurante Prueba M", direccion="Calle")
        PuntoRestaurante.objects.create(restaurante=self.restaurante, latitud=-9.930, longitud=-76.240)
        PerfilRepartidor.objects.create(usuario=self.cercano, latitud=-9.931, longitud=-76.241, disponible=True)
        PerfilRepartidor.objects.create(usuario=self.lejano, latitud=-9.95, longitud=-76.29, disponible=True)
        self.pedido = Pedido.objects.create(cliente=self.cliente, restaurante=self.restaurante,
            direccion_entrega="Calle 2", estado="LISTO")

    def api(self, u):
        c = APIClient()
        c.force_authenticate(user=u)
        return c

    def test_asigna_cercano_y_lo_ocupa(self):
        asignacion = asignar_mas_cercano(self.pedido)
        self.assertEqual(asignacion.repartidor_id, self.cercano.pk)
        self.assertFalse(PerfilRepartidor.objects.get(usuario=self.cercano).disponible)

    def test_flujo_listo_en_camino_entregado(self):
        asignar_mas_cercano(self.pedido)
        ruta = f"/api/repartidores/pedidos/{self.pedido.pk}/"
        r = self.api(self.cercano).post(ruta + "iniciar-reparto/", {}, format="json")
        self.assertEqual(r.status_code, 200, r.data)
        self.assertEqual(r.data["estado"], "EN_CAMINO")
        r = self.api(self.cercano).post(ruta + "confirmar-entrega/", {}, format="json")
        self.assertEqual(r.status_code, 200, r.data)
        self.assertEqual(r.data["estado"], "ENTREGADO")
        self.assertIsNotNone(r.data["entregado_en"])
        self.assertTrue(PerfilRepartidor.objects.get(usuario=self.cercano).disponible)
        self.assertEqual(self.api(self.cercano).post(
            ruta + "confirmar-entrega/", {}, format="json").status_code, 409)

    def test_repartidor_no_asignado_recibe_404(self):
        asignar_mas_cercano(self.pedido)
        r = self.api(self.lejano).post(
            f"/api/repartidores/pedidos/{self.pedido.pk}/iniciar-reparto/", {}, format="json")
        self.assertEqual(r.status_code, 404)

    def test_no_puede_confirmar_antes_de_iniciar(self):
        asignar_mas_cercano(self.pedido)
        r = self.api(self.cercano).post(
            f"/api/repartidores/pedidos/{self.pedido.pk}/confirmar-entrega/", {}, format="json")
        self.assertEqual(r.status_code, 409)