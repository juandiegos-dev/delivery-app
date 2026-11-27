from decimal import Decimal
from getpass import getpass
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from catalogo.models import Restaurante, Producto
from repartidores.models import PuntoRestaurante, PerfilRepartidor

Usuario = get_user_model()
with transaction.atomic():
    cuentas = {}
    for rol in ("cliente", "restaurante", "repartidor"):
        nombre = f"prueba_{rol}"
        u, nuevo = Usuario.objects.get_or_create(
            username=nombre,
            defaults={"email": nombre + "@delivery.test", "rol": rol})
        if u.rol != rol:
            raise ValueError("Cuenta existente con otro rol")
        if nuevo:
            clave = getpass(f"Contraseña local de {nombre}: ")
            validate_password(clave, u)
            u.set_password(clave)
            u.save()
        cuentas[rol] = u
    r, _ = Restaurante.objects.get_or_create(
        dueno=cuentas["restaurante"],
        defaults={"nombre": "Cocina de prueba", "direccion": "Huánuco"})
    Producto.objects.get_or_create(restaurante=r, nombre="Menú de prueba",
        defaults={"precio": Decimal("15.00"), "disponible": True})
    PuntoRestaurante.objects.get_or_create(restaurante=r,
        defaults={"latitud": -9.93, "longitud": -76.24})
    PerfilRepartidor.objects.get_or_create(usuario=cuentas["repartidor"],
        defaults={"latitud": -9.931, "longitud": -76.241, "disponible": True})
print("Datos locales preparados")
