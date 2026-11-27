from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def latitud():
    return [MinValueValidator(-90), MaxValueValidator(90)]


def longitud():
    return [MinValueValidator(-180), MaxValueValidator(180)]


class PuntoRestaurante(models.Model):
    restaurante = models.OneToOneField("catalogo.Restaurante", on_delete=models.CASCADE, related_name="punto_gps")
    latitud = models.FloatField(validators=latitud())
    longitud = models.FloatField(validators=longitud())

    def __str__(self):
        return f"GPS restaurante #{self.restaurante_id}"


class PerfilRepartidor(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil_repartidor")
    latitud = models.FloatField(null=True, blank=True, validators=latitud())
    longitud = models.FloatField(null=True, blank=True, validators=longitud())
    disponible = models.BooleanField(default=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Repartidor {self.usuario_id}"


class Asignacion(models.Model):
    pedido = models.OneToOneField("pedidos.Pedido", on_delete=models.CASCADE, related_name="asignacion")
    repartidor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="asignaciones")
    distancia_km = models.DecimalField(max_digits=8, decimal_places=2)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Asignación de pedido #{self.pedido_id}"


class HistorialUbicacion(models.Model):
    """Posiciones del repartidor asociadas a una asignación; nunca GPS de usuarios ajenos."""
    asignacion = models.ForeignKey(Asignacion, on_delete=models.CASCADE, related_name="trayecto")
    latitud = models.FloatField(validators=latitud())
    longitud = models.FloatField(validators=longitud())
    registrado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["registrado_en", "id"]

    def __str__(self):
        return f"Punto GPS - asignación #{self.asignacion_id}"