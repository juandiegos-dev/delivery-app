from django.conf import settings
from django.db import models


class Pedido(models.Model):

    # Estados disponibles para un pedido
    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        ACEPTADO = "ACEPTADO", "Aceptado"
        RECHAZADO = "RECHAZADO", "Rechazado"
        EN_PREPARACION = "EN_PREPARACION", "En preparación"
        LISTO = "LISTO", "Listo"

    # Cliente que realiza el pedido
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pedidos"
    )

    # Restaurante que recibe el pedido
    restaurante = models.ForeignKey(
        "catalogo.Restaurante",
        on_delete=models.PROTECT,
        related_name="pedidos"
    )

    # Información de entrega
    direccion_entrega = models.CharField(
        max_length=255
    )

    observaciones = models.TextField(
        blank=True
    )

    # Estado actual del pedido
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE
    )

    # Información económica
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    costo_envio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # Fecha de creación
    fecha_pedido = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-fecha_pedido"]
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido #{self.pk}"


class DetallePedido(models.Model):

    # Pedido al que pertenece el detalle
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="detalles"
    )

    # Producto del catálogo
    producto = models.ForeignKey(
        "catalogo.Producto",
        on_delete=models.PROTECT,
        related_name="detalles_pedido"
    )

    # Información del producto al momento de comprarlo
    nombre_producto = models.CharField(
        max_length=150
    )

    cantidad = models.PositiveIntegerField()

    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        verbose_name = "Detalle de pedido"
        verbose_name_plural = "Detalles de pedido"

    def __str__(self):
        return f"{self.nombre_producto} - Pedido #{self.pedido_id}"