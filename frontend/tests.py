from django.test import SimpleTestCase
from django.urls import reverse


class RutasFrontendTests(SimpleTestCase):
    def test_inicio(self):
        respuesta = self.client.get(reverse("inicio"))
        self.assertContains(respuesta, "Delivery App")

    def test_login_y_registro(self):
        self.assertEqual(self.client.get(reverse("login")).status_code, 200)
        self.assertEqual(self.client.get(reverse("registro")).status_code, 200)

    def test_catalogo_y_seguimiento(self):
        self.assertEqual(self.client.get(reverse("restaurantes")).status_code, 200)
        self.assertEqual(self.client.get(reverse("seguimiento", args=[1])).status_code, 200)