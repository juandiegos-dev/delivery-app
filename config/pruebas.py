from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from accesos.models import Usuario
from catalogo.models import Producto, Restaurante


def crear_api(rol, username=None):
    """Crea un usuario con ese rol y devuelve un cliente de API autenticado 
    (api.usuario es el usuario)."""

    nombre = username or rol
    usuario = Usuario.objects.create_user(
        username=nombre, email=f"{nombre}@correo.com", password="clave123", rol=rol)
    api = APIClient()
    api.credentials(HTTP_AUTHORIZATION=f"Token {Token.objects.create(user=usuario).key}")
    api.usuario = usuario
    return api


def crear_restaurante_con_menu():
    """Devuelve (api_dueno, restaurante_id, [id_producto_1, id_producto_2])."""

    api = crear_api("restaurante")
    restaurante = Restaurante.objects.create(
        dueno=api.usuario, nombre="Pollería Huánuco", direccion="Jr. Dos de Mayo 123")
    ids = [
        Producto.objects.create(restaurante=restaurante, nombre=nombre, precio=precio).id
        for nombre, precio in (("Pollo a la brasa", "25.50"), ("Gaseosa", "4.00"))
    ]
    return api, restaurante.id, ids