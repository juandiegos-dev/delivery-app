from django.conf import settings
from django.db import models


class Notificacion(models.Model):
    class Tipo(models.TextChoices):
        NUEVO_PEDIDO = "NUEVO_PEDIDO", "Nuevo pedido"
        ESTADO = "ESTADO", "Cambio de estado"
        ASIGNACION = "ASIGNACION", "Asignación de repartidor"

    destinatario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notificaciones"
    )
    pedido = models.ForeignKey(
        "pedidos.Pedido", on_delete=models.CASCADE, related_name="notificaciones"
    )
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    mensaje = models.CharField(max_length=240)
    leida = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha", "-id"]

    def __str__(self):
        return f"{self.tipo}: {self.destinatario_id}"