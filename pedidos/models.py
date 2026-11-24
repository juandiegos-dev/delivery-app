from django.conf import settings
from django.db import models


class Pedido(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        ACEPTADO = "ACEPTADO", "Aceptado"
        RECHAZADO = "RECHAZADO", "Rechazado"
        EN_PREPARACION = "EN_PREPARACION", "En preparación"
        LISTO = "LISTO", "Listo"
        EN_CAMINO = "EN_CAMINO", "En camino"
        ENTREGADO = "ENTREGADO", "Entregado"
        CANCELADO = "CANCELADO", "Cancelado"
        FALLIDO = "FALLIDO", "Fallido"

    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pedidos")
    restaurante = models.ForeignKey("catalogo.Restaurante", on_delete=models.PROTECT, related_name="pedidos")
    direccion_entrega = models.CharField(max_length=255)
    observaciones = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    entregado_en = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-fecha_pedido"]
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido #{self.pk}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey("catalogo.Producto", on_delete=models.PROTECT, related_name="detalles_pedido")
    nombre_producto = models.CharField(max_length=150)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Detalle de pedido"
        verbose_name_plural = "Detalles de pedido"

    def __str__(self):
        return f"{self.nombre_producto} - Pedido #{self.pedido_id}"


class IncidenciaPedido(models.Model):
    class Tipo(models.TextChoices):
        CANCELACION = "CANCELACION", "Cancelación"
        FALLO = "FALLO", "Pedido fallido"

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="incidencias")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="incidencias_reportadas")
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    motivo = models.CharField(max_length=300)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.tipo} - Pedido #{self.pedido_id}"