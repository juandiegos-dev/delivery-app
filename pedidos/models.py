from django.conf import settings
from django.db import models

from catalogo.models import Producto, Restaurante


class Pedido(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE"
        ACEPTADO = "ACEPTADO"
        RECHAZADO = "RECHAZADO"
        EN_PREPARACION = "EN_PREPARACION"
        LISTO = "LISTO"

    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="pedidos")
    restaurante = models.ForeignKey(Restaurante, on_delete=models.PROTECT, related_name="pedidos")
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
