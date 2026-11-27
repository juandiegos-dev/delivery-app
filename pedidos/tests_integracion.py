from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from accesos.models import Usuario
from catalogo.models import Restaurante, Producto
from pedidos.models import Pedido, IncidenciaPedido
from repartidores.models import PerfilRepartidor, PuntoRestaurante
from notificaciones.models import Notificacion


class IntegracionFinalTests(TestCase):
    def setUp(self):
        self.cliente = Usuario.objects.create_user(username="cliente_d", email="cd@example.test", password="Prueba123!", rol="cliente")
        self.dueno = Usuario.objects.create_user(username="dueno_d", email="dd@example.test", password="Prueba123!", rol="restaurante")
        self.rep = Usuario.objects.create_user(username="rep_d", email="rd@example.test", password="Prueba123!", rol="repartidor")
        self.restaurante = Restaurante.objects.create(dueno=self.dueno, nombre="Restaurante Prueba", direccion="Calle A")
        self.producto = Producto.objects.create(restaurante=self.restaurante, nombre="Pollo", precio=Decimal("19.00"))
        PuntoRestaurante.objects.create(restaurante=self.restaurante, latitud=-9.930, longitud=-76.240)
        PerfilRepartidor.objects.create(usuario=self.rep, latitud=-9.931, longitud=-76.241, disponible=True)

    def api(self, u):
        c = APIClient()
        c.force_authenticate(user=u)
        return c

    def test_creacion_listo_entrega_y_notificacion(self):
        datos = {"restaurante_id":self.restaurante.pk, "direccion_entrega":"Calle B",
                 "items":[{"producto_id":self.producto.pk, "cantidad":2}]}
        creado = self.api(self.cliente).post("/api/pedidos/", datos, format="json")
        self.assertEqual(creado.status_code, 201, creado.data)
        self.assertEqual(Decimal(creado.data["total"]), Decimal("43.00"))
        pid = creado.data["id"]
        for estado in ("ACEPTADO", "EN_PREPARACION", "LISTO"):
            r = self.api(self.dueno).patch(f"/api/pedidos/{pid}/estado/", {"estado":estado}, format="json")
            self.assertEqual(r.status_code, 200, r.data)
        ruta = f"/api/repartidores/pedidos/{pid}/"
        self.assertEqual(self.api(self.rep).post(ruta+"iniciar-reparto/", {}, format="json").status_code,200)
        entregado = self.api(self.rep).post(ruta+"confirmar-entrega/", {}, format="json")
        self.assertEqual(entregado.status_code,200,entregado.data)
        self.assertEqual(entregado.data["estado"],"ENTREGADO")
        self.assertTrue(Notificacion.objects.filter(pedido_id=pid).exists())