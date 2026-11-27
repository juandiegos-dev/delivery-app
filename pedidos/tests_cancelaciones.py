
from django.test import TestCase
from rest_framework.test import APIClient
from accesos.models import Usuario
from catalogo.models import Restaurante
from pedidos.models import Pedido, IncidenciaPedido
from notificaciones.models import Notificacion


class CancelacionesTests(TestCase):

    def setUp(self):
        self.cliente = Usuario.objects.create_user(
            username="cliente_y",
            email="y@example.test",
            password="Prueba123!",
            rol="cliente"
        )

        self.ajeno = Usuario.objects.create_user(
            username="ajeno_y",
            email="a@example.test",
            password="Prueba123!",
            rol="cliente"
        )

        self.dueno = Usuario.objects.create_user(
            username="dueno_y",
            email="d@example.test",
            password="Prueba123!",
            rol="restaurante"
        )

        self.restaurante = Restaurante.objects.create(
            dueno=self.dueno,
            nombre="Restaurante Prueba",
            direccion="Calle"
        )

        self.pedido = Pedido.objects.create(
            cliente=self.cliente,
            restaurante=self.restaurante,
            direccion_entrega="Calle 2"
        )

        self.url = f"/api/pedidos/{self.pedido.pk}/cancelar/"

    def api(self, usuario):
        cliente = APIClient()
        cliente.force_authenticate(user=usuario)
        return cliente

    def test_cliente_cancela_pendiente(self):
        r = self.api(self.cliente).post(
            self.url,
            {"motivo": "Ya no necesito el pedido"},
            format="json"
        )

        self.assertEqual(r.status_code, 200, r.data)
        self.assertEqual(r.data["estado"], "CANCELADO")

        self.assertEqual(
            IncidenciaPedido.objects.filter(
                pedido=self.pedido,
                tipo="CANCELACION"
            ).count(),
            1
        )

        self.assertTrue(
            Notificacion.objects.filter(
                destinatario=self.dueno,
                pedido=self.pedido
            ).exists()
        )

    def test_cancelacion_desde_aceptado(self):
        self.pedido.estado = "ACEPTADO"
        self.pedido.save(update_fields=["estado"])

        r = self.api(self.dueno).post(
            self.url,
            {"motivo": "No podemos atender este pedido"},
            format="json"
        )

        self.assertEqual(r.status_code, 200, r.data)

    def test_cancelacion_tardia_409(self):
        self.pedido.estado = "EN_PREPARACION"
        self.pedido.save(update_fields=["estado"])

        r = self.api(self.cliente).post(
            self.url,
            {"motivo": "Quiero cancelar demasiado tarde"},
            format="json"
        )

        self.assertEqual(r.status_code, 409)

    def test_ajeno_404(self):
        r = self.api(self.ajeno).post(
            self.url,
            {"motivo": "Este pedido no es mio"},
            format="json"
        )

        self.assertEqual(r.status_code, 404)

    def test_motivo_corto_400(self):
        r = self.api(self.cliente).post(
            self.url,
            {"motivo": "No"},
            format="json"
        )

        self.assertEqual(r.status_code, 400)
