from rest_framework.test import APITestCase

DATOS = {"username": "ana", "email": "ana@correo.com", "password": 
         "clave123", "rol": "cliente"}

class AccesoTests(APITestCase):
    def test_registro_exitoso(self):
        r = self.client.post("/api/auth/registro/", DATOS, format="json")
        self.assertEqual(r.status_code, 201)
        self.assertNotIn("password", r.data)

    def test_login_exitoso_devuelve_token(self):
        self.client.post("/api/auth/registro/", DATOS, format="json")
        r = self.client.post("/api/auth/login/", 
                             {"username": "ana", "password": "clave123"}, format="json")
        self.assertEqual(r.status_code, 200)
        self.assertIn("token", r.data)

    def test_registro_con_correo_duplicado(self):
        self.client.post("/api/auth/registro/", DATOS, format="json")
        r = self.client.post("/api/auth/registro/", {**DATOS, "username": "otra"}, format="json")
        self.assertEqual(r.status_code, 400)

    def test_registro_con_correo_invalido(self):
        r = self.client.post("/api/auth/registro/", {**DATOS, "email": "sin-arroba"}, format="json")
        self.assertEqual(r.status_code, 400)

    def test_login_con_clave_incorrecta(self):
        self.client.post("/api/auth/registro/", DATOS, format="json")
        r = self.client.post("/api/auth/login/", {"username": "ana", "password": "otra"}, format="json")
        self.assertEqual(r.status_code, 400)

    def test_password_en_el_limite_minimo(self):
        corta = self.client.post("/api/auth/registro/", {**DATOS, "password": "12345"}, format="json")
        valida = self.client.post("/api/auth/registro/", {**DATOS, "password": "123456"}, format="json")
        self.assertEqual((corta.status_code, valida.status_code), (400, 201))

    def test_ruta_protegida_sin_token(self):
        self.assertEqual(self.client.get("/api/auth/yo/").status_code, 401)