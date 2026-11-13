from django.conf import settings
from django.db import models

class Pedido(models.Model):
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,
                                related_name="pedidos")
    
    direccion_entrega = models.CharField(max_length=255)
    observaciones = models.TextField(blank=True)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    costo_envio = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    total = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    fecha_pedido = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_pedido"]
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido #{self.pk}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido,on_delete=models.CASCADE,related_name="detalles")
    nombre_producto = models.CharField(max_length=150)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10,decimal_places=2)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2)

    class Meta:
        verbose_name = "Detalle de pedido"
        verbose_name_plural = "Detalles de pedido"

    def __str__(self):
        return f"{self.nombre_producto} - Pedido #{self.pedido_id}"
